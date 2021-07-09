import backoff
import requests
import unittest

from helpers.client_data import *
from hamcrest import *
from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth

URL = "https://qa-interview-api.migo.money"
CLEANUP = []


class ClientsTests(unittest.TestCase):

    @classmethod
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def setUpClass(cls):
        global api_key
        api_key = requests.post(f"{URL}/token",
                                headers={HttpHeaders.ACCEPT: "application/json"},
                                auth=HTTPBasicAuth("egg", "f00BarbAz!")
                                ).json()["key"]

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_01_get_clients_response_200(self):
        clients = requests.get(f"{URL}/clients",
                               headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        assert_that(clients.status_code, equal_to(200))

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_02_get_clients_invalid_api_key_response_403(self):
        clients = requests.get(f"{URL}/clients",
                               headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid_api_key"})
        assert_that(clients.status_code, equal_to(403))
        assert_that(clients.json()["message"], equal_to("invalid or missing api key"))

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_03_get_clients_missing_api_key_response_403(self):
        clients = requests.get(f"{URL}/clients",
                               headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": ""})
        assert_that(clients.status_code, equal_to(403))
        assert_that(clients.json()["message"], equal_to("invalid or missing api key"))


if __name__ == '__main__':
    unittest.main()
