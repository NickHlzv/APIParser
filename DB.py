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
            self.status = f"Connected to MongoDB successfully. Config{cfg}"
        except pymongo.errors.AutoReconnect:  # pragma: no cover
                loggerDB.exception('Connection to MongoDB failed, retrying')
                time.sleep(5)

    def key_is_exists(self, apikey):
        return bool(self.keysCollection.find_one({"apikey": apikey}))

    def jsons_is_exists(self, apikey, url):
        return bool(self.jsonCollection.find_one({"apikey": apikey, "url": url}))

    def hints_is_exists(self, apikey, url):
        return bool(self.hintsCollection.find_one({"apikey": apikey, "url": url}))

    def insert_key(self, name, key):
        if self.key_is_exists(key):
            self.keysCollection.update_one({"key": key},{"name": name})
            loggerDB.info(f"Updated name {name} on key {key}")
            return "Ключ существует. Данные обновлены"
        else:
            test_request: APITrnRequest = APITrnRequest(key)
            if test_request.authorize():
                self.keysCollection.insert_one({"name": name, "key": key})
                loggerDB.info(f"API authorize is ok, and key:{key} was inserted with name {name}")
                return "Ключ добавлен"
            else:
                loggerDB.error(f"API authorize is failed, key:{key} was not inserted")
                return "Ключ не авторизовался и не будет добавлен"








