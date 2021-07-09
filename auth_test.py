import backoff
import pytest
import requests
import unittest

from faker import Faker
from hamcrest import *
from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth


class BasicAuth(unittest.TestCase):

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def setUp(self):
        global api_key
        api_key = requests.post(
            "https://qa-interview-api.migo.money/token",
            headers={HttpHeaders.ACCEPT: "application/json"},
            auth=HTTPBasicAuth("egg", "f00BarbAz!")  # this should be hidden in the env variables os.environ[variable]
        ).json()["key"]

    @staticmethod
    def setup_client():
        faker = Faker()
        data = {
            "firstName": faker.name().split()[0],
            "lastName": faker.name().split()[1],
            "phone": "123456798"
        }
        print(data)
        client_id = requests.post("https://qa-interview-api.migo.money/clients",
                                  headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key}).json()["id"]
        yield client_id
        requests.delete(f"https://qa-interview-api.migo.money/client/{client_id}")

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_01_fetch_clients(self):
        clients = requests.get("https://qa-interview-api.migo.money/clients",
                               headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        print(clients.json()["clients"])
        assert_that(clients.status_code, equal_to(200))
        assert_that(len(clients.json()["clients"]), greater_than_or_equal_to(0))

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_02_get_client(self, setup_client):
        client = requests.get(f"https://qa-interview-api.migo.money/client/{setup_client}")
        print(client.json()[0])


if __name__ == '__main__':
    unittest.main()
