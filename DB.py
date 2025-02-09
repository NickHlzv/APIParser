import pymongo
import json
import logging
import pymongo.errors
import time

from pymongo import MongoClient

from API import APITrnRequest

# Set DataBase logger
loggerDB = logging.getLogger(__name__)
loggerDB.setLevel(logging.INFO)
handlerDB = logging.FileHandler(f"{__name__}.log", encoding='utf-8')
handlerDB.setFormatter(logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))
loggerDB.addHandler(handlerDB)


# Init start DB connection data
cfgCreation = False
try:
    cfg = json.load(open("config.json", "r"))
    loggerDB.info(f"Config loaded: {cfg}")
except FileNotFoundError:
    with open("config.json", "w") as file:
        loggerDB.error(f"Config file not found. Trying to create it.")
        json.dump({"DBSrvConnection": "mongodb://localhost:27017/"}, file)
        cfgCreation = True
        if cfgCreation:
            cfg = json.load(open("config.json", "r"))
            loggerDB.info(f"Config loaded: {cfg}")
        else:
            cfg = {"DBSrvConnection": "mongodb://localhost:27017/"}
            loggerDB.info(f"Can't create config file. Use default connection on mongodb://localhost:27017/")


class MongoDB(pymongo.MongoClient):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(cfg['DBSrvConnection'], *args, **kwargs)
            self.dbClient = MongoClient(cfg['DBSrvConnection'])
            self.parser = self.dbClient["parserDB"]
            self.keysCollection = self.parser["apikeys"]
            self.jsonsCollection = self.parser["jsons"]
            self.hintsCollection = self.parser["hints"]
            self.status = f"Connected to MongoDB successfully. Config: {cfg}"
            loggerDB.info(self.status)
        except pymongo.errors.AutoReconnect:  # pragma: no cover
                self.status = "Connection to MongoDB failed. Try to reconnect"
                loggerDB.exception(self.status)
                time.sleep(5)

    def key_is_exists(self, apikey):
        if "apikeys" in self.dbClient["parserDB"].list_collection_names():
            return bool(self.dbClient["parserDB"]["apikeys"].find_one({"key": apikey}))
        else: return False

    def json_is_exists(self, apikey, url):
        if "jsons" in self.dbClient["parserDB"].list_collection_names():
            return bool(self.dbClient["parserDB"]["jsons"].find_one({"key": apikey, "url": url}))
        else: return False

    def hint_is_exists(self, apikey, url):
        if "hints" in self.dbClient["parserDB"].list_collection_names():
            return bool(self.dbClient["parserDB"]["hints"].find_one({"key": apikey, "url": url}))
        else: return False

    def insert_key(self, name, key):
        if self.key_is_exists(key):
            self.keysCollection.update_one({"key": key},{"$set":{"name": name}})
            loggerDB.info(f"Updated name {name} on key {key}")
            return True, "Ключ существует. Данные обновлены"
        else:
            test_request: APITrnRequest = APITrnRequest(key)
            if test_request.authorize():
                self.keysCollection.insert_one({"name": name, "key": key})
                loggerDB.info(f"API authorize is ok, and key:{key} was saved with name {name}")
                return True, "Ключ добавлен"
            else:
                loggerDB.error(f"API authorize is failed, key:{key} was not inserted")
                return False, "Ключ не авторизовался и не добавлен"

    def load_keys(self):
        keys_dict = {}
        for doc in self.keysCollection.find().sort("name", pymongo.ASCENDING):
            keys_dict[doc["key"]] = doc["name"]
        loggerDB.info(f"API keys loaded from DB\n: {keys_dict}")
        return keys_dict

    def insert_json(self, apikey, url, json_data):
        try:
            json_converted = str(json.loads(json_data.replace("'", '"')))
            if self.json_is_exists(apikey, url):
                self.jsonsCollection.update_one({"key": apikey, "url": url}, {'$set': {"json": json_converted}})
                loggerDB.info(f"Updated json for {apikey} | {url} into DB data\n {json_converted}")
            else:
                self.jsonsCollection.insert_one({"key": apikey, "url": url, "json": json_converted})
                loggerDB.info(f"Save json for {apikey} | {url} into DB data\n {json_converted}")
        except json.decoder.JSONDecodeError or TypeError:
             loggerDB.error("Failed to decode json data, data not saved into DB")

    def load_json(self, apikey, url):
        if self.json_is_exists(apikey, url):
            json_output = self.parserDB["jsons"].find_one({"key": apikey, "url": url})["json"]
            loggerDB.info(f"json was loaded from DB for {apikey} | {url} data\n {json_output}")
            return json_output
        else:
            loggerDB.info(f"Wasn't find json data, load standard empty json body")
            return '{\n"organizationIds": [\n\n]\n}'

    def load_hint(self, apikey, url):
        if self.hint_is_exists(apikey, url):
            hint_output = self.hintsCollection.find_one({"key": apikey, "url": url})["hint"]
            loggerDB.info(f"Hint was loaded from DB for {apikey} | {url} data\n {hint_output}")
            return hint_output
        else:
            loggerDB.info(f"Wasn't find hint data, nothing to load")
            return "Подсказки появятся, когда будете делать запросы. \nОни будут создаваться из запросов и сохраняться в базу"

    def insert_hint(self, apikey, url):
        __hintUrl = url
        __organizationsHint = ("Выполните пустой запрос. \nМожно использовать дополнительно атрибуты:"
                               "\n 'returnAdditionalInfo': true - отобразить доп. инфо"
                               "\n 'includeDisabled': true - показать отключенные организации")
        __extMenuHint = "Выполните пустой запрос"
        __defaultHint = "Выполните запрос организации"
        __deliveryStatusHint = ("Для задание времени используйте атрибуты\n "
                                "'deliveryDateFrom': '2019-08-24 14:15:22.123'\n 'deliveryDateTo': '2019-08-24 14:15:22.123'\n"
                                "Используйте организации\n\n")
        if __hintUrl == "https://api-ru.iiko.services/api/1/organizations":
            if not self.hint_is_exists(apikey, url):
                self.hintsCollection.insert_one({"key": apikey, "url": url, "hint": __organizationsHint})
                loggerDB.info(f"Default Organization Hint for {apikey} and {url} was saved into DB")
        elif __hintUrl == "https://api-ru.iiko.services/api/2/menu":
            if not self.hint_is_exists(apikey, url):
                self.hintsCollection.insert_one({"key": apikey, "url": url, "hint": __extMenuHint})
                loggerDB.info(f"Default extMenuHint for {apikey} and {url} was saved into DB")
        elif __hintUrl == "https://api-ru.iiko.services/api/2/menu/by_id":
            v2_menu_request = APITrnRequest(apikey, url='https://api-ru.iiko.services/api/2/menu')
            if not self.hint_is_exists(apikey, url):
                if v2_menu_request.authorize():
                    _, hint_data = v2_menu_request.post()
                    self.hintsCollection.insert_one({"key": apikey, "url": url, "hint":"Используйте id меню и ценовые категории\n\n"+hint_data})
                    loggerDB.info(f"Json Hint nomenclature v2 menu for {apikey} and {url} was requested and saved into DB")
                else:
                    loggerDB.error(f"Can't load json hint for {apikey} and {url}, try to repeat this request")

            else:
                if v2_menu_request.authorize():
                    _, hint_data = v2_menu_request.post()
                    self.hintsCollection.update_one({"key": apikey, "url": url},
                                                    {"$set": {"hint":"Используйте id меню и ценовые категории\n\n"+hint_data}})
                    loggerDB.info(f"Json Hint nomenclature v2 menu for {apikey} and {url} was requested and updated into DB")
                else:
                    loggerDB.info(f"Can't authorize menu request. Hint doesn't updated")
        elif __hintUrl == "https://api-ru.iiko.services/api/1/deliveries/by_delivery_date_and_status":
            v2_menu_request = APITrnRequest(apikey, url='https://api-ru.iiko.services/api/1/organizations')
            if not self.hint_is_exists(apikey, url):
                if v2_menu_request.authorize():
                    _, hint_data = v2_menu_request.post()
                    self.hintsCollection.insert_one({"key": apikey, "url": url, "hint":__deliveryStatusHint+hint_data})
                    loggerDB.info(f"Json Hint nomenclature v2 menu for {apikey} and {url} was requested and saved into DB")
                else:
                    loggerDB.error(f"Can't load json hint for {apikey} and {url}, try to repeat this request")
            else:
                if v2_menu_request.authorize():
                    _, hint_data = v2_menu_request.post()
                    self.hintsCollection.update_one({"key": apikey, "url": url},
                                                    {"$set": {"hint":__deliveryStatusHint+hint_data}})
                    loggerDB.info(f"Json Hint nomenclature v2 menu for {apikey} and {url} was requested and updated into DB")
                else:
                    loggerDB.info(f"Can't authorize organizations request. Hint doesn't updated")
        else:
            v2_menu_request = APITrnRequest(apikey, url='https://api-ru.iiko.services/api/1/organizations')
            if not self.hint_is_exists(apikey, url):
                if v2_menu_request.authorize():
                    _, hint_data = v2_menu_request.post()
                    self.hintsCollection.insert_one({"key": apikey, "url": url, "hint":"Используйте организации\n\n" + hint_data})
                    loggerDB.info(f"Json hint load from json for {apikey} and {url} was requested and saved into DB")
                else:
                    loggerDB.error(f"Can't load json hint for {apikey} and {url}, try to repeat this request")
            else:
                if v2_menu_request.authorize():
                    _, hint_data = v2_menu_request.post()
                    self.hintsCollection.update_one({"key": apikey, "url": url},
                                                    {"$set": {"hint":"Используйте организации\n\n" + hint_data}})
                    loggerDB.info(f"Json hint load from json for {apikey} and {url} was requested and updated into DB")
                else:
                    loggerDB.info(f"Can't authorize organizations request. Hint doesn't updated")









