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
    def __init__(self, apikey, url=orgMethodURL, headers=None, data=None):
        if not apikey:
            loggerAPI.exception("Apikey is missing. It's required.")
            raise ValueError("Apikey is missing. It's required.")
        self.URL = url
        self.headers = defaultHeaders if not headers else headers
        self.data = {} if not data else data
        self.response = None
        self.apiKey = apikey


    def authorize(self):
        auth_url = "https://api-ru.iiko.services/api/1/access_token"
        auth_headers = {"Content-Type": "application/json"}
        auth_json = {"apiLogin": self.apiKey}
        try:
            auth_request = requests.post(auth_url, headers=auth_headers, data=auth_json)
            auth_request.raise_for_status()
        except requests.exceptions.HTTPError as err_h:
            loggerAPI.exception(f"Auth http error: {err_h}\n{auth_url}\n{auth_json}")
            return f"Auth Http Error: {err_h}"
        except requests.exceptions.RequestException as expt:
            loggerAPI.exception(f"Auth error: {expt}\n{auth_url}\n{auth_json}")
            return f"Auth error: {expt}"
        else:
            if auth_request.status_code:
                if auth_request.status_code == 200:
                    self.headers["Authorization"] = f"Bearer {auth_request.json()["token"]}"
                    loggerAPI.info(f"Apikey: {self.apiKey} has got auth token:\n{self.headers["Authorization"]}")
                    return f"{auth_request.json()["token"]}"
                else:
                    loggerAPI.error(f"Auth error:\n{auth_request.json()}")
                    return f"Auth error: {auth_request.json()}"
            else:
                loggerAPI.error("Unexpected error (authorization method complete but hasn't any result)")
                return "Unexpected error (authorization method complete but hasn't any result)"


    def post(self):
        if 'Authorization' not in self.headers:
            loggerAPI.info("Bearer token is missing. Try to authorize")
            self.authorize()
        try:
            post_request = requests.post(self.URL, headers=self.headers, data=self.data)
            post_request.raise_for_status()
            loggerAPI.info(f"Request\n{self.URL}\nJSON\n{self.data}")
        except requests.exceptions.HTTPError as err_h:
            loggerAPI.exception(f"Request Http Error: {err_h}\n{self.URL}\nJSON\n{self.data}")
            return "Error", f"Http Error: {err_h}"
        except requests.exceptions.RequestException as expt:
            loggerAPI.exception(f"Request error: {expt}\n{self.URL}\nJSON\n{self.data}")
            return "Error", f"Error: {expt}"
        else:
            if post_request.status_code:
                if post_request.status_code == 200:
                    loggerAPI.info(f"Success request. Response:\n{self.response}")
                    return post_request.status_code, self.response
                if post_request.status_code == 401:
                    loggerAPI.info(f"Bearer token is missing or expired. Try to authorize and will send request again."
                                   f" (Unauthorized post request)")
                    self.authorize()
                    self.post()
                else:
                    loggerAPI.error(f"Response code:{post_request.status_code}\n{self.response}")
                    return post_request.status_code, self.response
            else:
                loggerAPI.error("Unexpected error (request complete but hasn't any result)")
                return "Error", "Unexpected error"








