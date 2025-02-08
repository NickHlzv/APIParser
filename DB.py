import pymongo
import json
import logging
import pymongo.errors
import time
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
            self.dbClient = super().__init__(*args, **kwargs)
            self.parserDB = self.dbClient["parserDB"]
            self.keysCollection = self.parserDB["apikeys"]
            self.jsonsCollection = self.parserDB["jsons"]
            self.hintsCollection = self.parserDB["hints"]
            self.status = f"Connected to MongoDB successfully. Config: {cfg}"
            loggerDB.info(self.status)
        except pymongo.errors.AutoReconnect:  # pragma: no cover
                self.status = "Connection to MongoDB failed. Try to reconnect"
                loggerDB.exception(self.status)
                time.sleep(5)

    def key_is_exists(self, apikey):
        return bool(self.keysCollection.find_one({"key": apikey}))

    def jsons_is_exists(self, apikey, url):
        return bool(self.jsonCollection.find_one({"key": apikey, "url": url}))

    def hints_is_exists(self, apikey, url):
        return bool(self.hintsCollection.find_one({"key": apikey, "url": url}))

    def insert_key(self, name, key):
        if self.key_is_exists(key):
            self.keysCollection.update_one({"key": key},{"$set":{"name": name}})
            loggerDB.info(f"Updated name {name} on key {key}")
            return "Ключ существует. Данные обновлены"
        else:
            test_request: APITrnRequest = APITrnRequest(key)
            if test_request.authorize():
                self.keysCollection.insert_one({"name": name, "key": key})
                loggerDB.info(f"API authorize is ok, and key:{key} was saved with name {name}")
                return "Ключ добавлен"
            else:
                loggerDB.error(f"API authorize is failed, key:{key} was not inserted")
                return "Ключ не авторизовался и не добавлен"

    def load_keys(self):
        keys_dict = {}
        for doc in self.keysCollection.find():
            keys_dict[doc["key"]] = doc["name"]
        loggerDB.info(f"API keys loaded from DB\n: {keys_dict}")
        return keys_dict

    def insert_json(self, apikey, url, json_data):
        try:
            json_converted = json.dumps(json_data, ensure_ascii=False, indent=4)
            if self.jsons_is_exists(apikey, url):
                self.jsonsCollection.update_one({"key": apikey, "url": url}, {'$set': {"json": json_converted}})
                loggerDB.info(f"Updated json for {apikey} | {url} into DB data\n {json_converted}")
            else:
                self.jsonsCollection.insert_one({"key": apikey, "url": url, "json": json_converted})
                loggerDB.info(f"Save json for {apikey} | {url} into DB data\n {json_converted}")
        except json.decoder.JSONDecodeError or TypeError:
             loggerDB.error("Failed to decode json data, data not saved into DB")

    def load_json(self, apikey, url):
        if self.jsons_is_exists(apikey, url):
            json_output = self.jsonsCollection.find_one({"key": apikey, "url": url})["json"]
            loggerDB.info(f"json was loaded from DB for {apikey} | {url} data\n {json_output}")
            return json_output
        else:
            loggerDB.info(f"Wasn't find json data, load empty json body")
            return "{\n\n}"





