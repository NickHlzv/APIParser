import requests
import json
import logging

#  Set logging module API.py

loggerAPI = logging.getLogger(__name__)
loggerAPI.setLevel(logging.INFO)
handlerAPI = logging.FileHandler(f"{__name__}.log", encoding='utf-8')
handlerAPI.setFormatter(logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))
loggerAPI.addHandler(handlerAPI)

#  Set base params
baseURL = "https://api-ru.iiko.services/api/"
orgMethodURL = baseURL + "api/1/organizations"
defaultHeaders = {
    "Content-Type": "application/json"
}


class APITrnRequest:
    GlobalApikey = None
    def __init__(self, apikey, url=orgMethodURL, headers=None, data=None):
        if not apikey:
            loggerAPI.exception("Apikey is missing. It's required.")
            raise ValueError("Apikey is missing. It's required.")
        self.URL = url
        self.headers = defaultHeaders.copy() if not headers else headers
        self.data = json.dumps({} if not data else data)
        self.apiKey = apikey
        self.authorized = False
        if APITrnRequest.GlobalApikey != self.apiKey:
            APITrnRequest.GlobalApikey = self.apiKey
            self.authorized = self.authorize()



    def authorize(self):
        auth_url = "https://api-ru.iiko.services/api/1/access_token"
        auth_headers = {"Content-Type": "application/json"}
        auth_json = json.dumps({"apiLogin": self.apiKey})
        try:
            auth_request = requests.post(auth_url, headers=auth_headers, data=auth_json)
        except requests.exceptions.HTTPError as err_h:
            loggerAPI.exception(f"Auth http error: {err_h}\n{auth_url}\n{auth_json}")
            return False
        except requests.exceptions.RequestException as expt:
            loggerAPI.exception(f"Auth error: {expt}\n{auth_url}\n{json.loads(auth_json)}")
            return False
        else:
            if auth_request.status_code:
                if auth_request.status_code == 200:
                    self.headers["Authorization"] = f"Bearer {auth_request.json()["token"]}"
                    loggerAPI.info(f"Apikey: {self.apiKey} has got auth token:\n{self.headers["Authorization"]}")
                    return True
                else:
                    loggerAPI.error(f"Auth error:\n{auth_request.json()}, headers and auth session cleared")
                    self.headers = defaultHeaders.copy()
                    return False
            else:
                loggerAPI.error("Unexpected error (authorization method complete but hasn't any result)")
                return False


    def post(self):
        if 'Authorization' not in self.headers:
            loggerAPI.info("Bearer token is missing. Try to authorize")
            self.authorize()
        try:
            post_request = requests.post(self.URL, headers=self.headers, data=self.data)
            loggerAPI.info(f"Request\n{self.URL}\nJSON\n{json.loads(self.data)}")
        except requests.exceptions.HTTPError as err_h:
            loggerAPI.exception(f"Request Http Error: {err_h}\n{self.URL}\nJSON\n{self.data}")
            return "Error", f"Http Error: {err_h}"
        except requests.exceptions.RequestException as expt:
            loggerAPI.exception(f"Request error: {expt}\n{self.URL}\nJSON\n{self.data}")
            return "Error", f"Error: {expt}"
        else:
            if post_request.status_code:
                if post_request.status_code == 200:
                    response = json.dumps(post_request.json(), indent=4, ensure_ascii=False)
                    loggerAPI.info(f"Success request. Response:\n{response}")
                    return post_request.status_code, response
                if post_request.status_code == 401:
                    loggerAPI.info(f"Bearer token is missing or expired. Try to authorize and will send request again."
                                   f" (Unauthorized post request)")
                    self.authorized = self.authorize()
                    if self.authorized:
                        self.post()
                    else:
                        loggerAPI.error("Authorization failed. Invalid auth request")
                        return "Error", "Authorization failed. Invalid auth request"
                else:
                    response = json.dumps(post_request.json(), indent=4, ensure_ascii=False)
                    loggerAPI.error(f"Response code:{post_request.status_code}\n{response}")
                    return post_request.status_code, response
            else:
                loggerAPI.error("Unexpected error (request complete but hasn't any result)")
                return "Error", "Unexpected error\n"








