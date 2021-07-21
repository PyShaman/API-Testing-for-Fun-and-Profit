import backoff
import requests

from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth

URL = "https://this_should_be_url.com"
USER = "this_should_be_login"  # os.environ["USER"]
PASSWORD = "this_should_be_password"  # os.environ["PASSWORD"]


class CrudMethods:

    def __init__(self):
        pass

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def return_api_key(self):
        return requests.post(f"{URL}/token",
                             headers={HttpHeaders.ACCEPT: "application/json"},
                             auth=HTTPBasicAuth(USER, PASSWORD)).json()["key"]

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def _create(self, endpoint, client_data, api_key):
        return requests.post(f"{URL}{endpoint}",
                             json=client_data,
                             headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def _read(self, endpoint, api_key):
        return requests.get(f"{URL}{endpoint}",
                            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def _update(self, endpoint, cid, data, api_key):
        return requests.put(f"{URL}{endpoint}/{cid}",
                            json=data,
                            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def _delete(self, endpoint, cid, api_key):
        return requests.delete(f"{URL}{endpoint}/{cid}",
                               headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
