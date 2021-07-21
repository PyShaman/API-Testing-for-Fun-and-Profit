import backoff
import requests
import unittest

from hamcrest import *
from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth

URL = "https://this_should_be_url.com"
USER = "this_should_be_login"  # os.environ["USER"]
PASSWORD = "this_should_be_password"  # os.environ["PASSWORD"]


class BasicAuthTests(unittest.TestCase):

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=10)
    def test_01_get_api_key_response_200(self):
        api_key = requests.post(f"{URL}/token",
                                headers={HttpHeaders.ACCEPT: "application/json"},
                                auth=HTTPBasicAuth(USER, "f00BarbAz!".capitalize()))
        api_key_data = api_key.json()
        assert_that(api_key.status_code, equal_to(200))
        assert_that(api_key_data["key"], not_none())

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=10)
    def test_02_get_api_key_invalid_username_response_400(self):
        api_key = requests.post(f"{URL}/token",
                                headers={HttpHeaders.ACCEPT: "application/json"},
                                auth=HTTPBasicAuth("invalid", PASSWORD))
        api_key_data = api_key.json()
        assert_that(api_key.status_code, equal_to(400))
        assert_that(api_key_data["message"], equal_to("invalid username or password"))

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=10)
    def test_03_get_api_key_invalid_password_response_400(self):
        api_key = requests.post(f"{URL}/token",
                                headers={HttpHeaders.ACCEPT: "application/json"},
                                auth=HTTPBasicAuth(USER, "invalid"))
        api_key_data = api_key.json()
        assert_that(api_key.status_code, equal_to(400))
        assert_that(api_key_data["message"], equal_to("invalid username or password"))


if __name__ == '__main__':
    unittest.main()
