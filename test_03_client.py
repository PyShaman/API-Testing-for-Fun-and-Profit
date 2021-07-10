import backoff
import requests
import unittest

from helpers.client_data import *
from hamcrest import *
from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth

URL = "https://qa-interview-api.migo.money"
CLEANUP = []


class ClientTests(unittest.TestCase):

    @classmethod
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def setUpClass(cls):
        global api_key
        api_key = requests.post(f"{URL}/token",
                                headers={HttpHeaders.ACCEPT: "application/json"},
                                auth=HTTPBasicAuth("egg", "f00BarbAz!")
                                ).json()["key"]

    @classmethod
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def tearDownClass(cls):
        for client_id in CLEANUP:
            requests.delete(f"{URL}/client/{client_id}",
                            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_01_get_client_response_200(self):
        client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        create_client_data = create_client.json()
        client_id = create_client.json()["id"]
        returned_client = requests.get(f"{URL}/client/{client_id}",
                                       headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        returned_client_data = returned_client.json()
        assert_that(returned_client.status_code, equal_to(200))
        assert_that(returned_client_data, has_entries(create_client_data))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_02_get_client_invalid_api_key_response_403(self):
        client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        returned_client = requests.get(f"{URL}/client/{client_id}",
                                       headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid_api_key"})
        returned_client_data = returned_client.json()
        assert_that(returned_client.status_code, equal_to(403))
        assert_that(returned_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_03_get_client_missing_api_key_response_403(self):
        client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        returned_client = requests.get(f"{URL}/client/{client_id}",
                                       headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": ""})
        returned_client_data = returned_client.json()
        assert_that(returned_client.status_code, equal_to(403))
        assert_that(returned_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_04_put_client_response_200(self):
        client_data = create_user_data()
        updated_client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        updated_client = requests.put(f"{URL}/client/{client_id}",
                                      json=updated_client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(200))
        assert_that(updated_client_data, not_(equal_to(has_entries(client_data))))
        assert_that(updated_client_data["id"], equal_to(client_id))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_05_put_client_response_invalid_400(self):
        client_data = create_user_data()
        updated_partial_client_data = {}
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        updated_client = requests.put(f"{URL}/client/{client_id}",
                                      json=updated_partial_client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("invalid request"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_06_put_client_response_without_first_name_400(self):
        client_data = create_user_data()
        updated_partial_client_data = create_user_data()
        del updated_partial_client_data["firstName"]
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        updated_client = requests.put(f"{URL}/client/{client_id}",
                                      json=updated_partial_client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("firstName is required"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_07_put_client_response_without_last_name_400(self):
        client_data = create_user_data()
        updated_partial_client_data = create_user_data()
        del updated_partial_client_data["lastName"]
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        updated_client = requests.put(f"{URL}/client/{client_id}",
                                      json=updated_partial_client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("lastName is required"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_08_put_client_response_without_phone_400(self):
        client_data = create_user_data()
        updated_partial_client_data = create_user_data()
        del updated_partial_client_data["phone"]
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        updated_client = requests.put(f"{URL}/client/{client_id}",
                                      json=updated_partial_client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("phone is required"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_09_put_client_invalid_api_key_response_403(self):
        client_data = create_user_data()
        updated_client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        updated_client = requests.put(f"{URL}/client/{client_id}",
                                      json=updated_client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid_api_key"})
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(403))
        assert_that(updated_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_10_put_client_missing_api_key_response_403(self):
        client_data = create_user_data()
        updated_client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        updated_client = requests.put(f"{URL}/client/{client_id}",
                                      json=updated_client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": ""})
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(403))
        assert_that(updated_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_11_delete_client_response_200(self):
        client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        deleted_client = requests.delete(f"{URL}/client/{client_id}",
                                         headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(200))
        assert_that(deleted_client_data["message"], equal_to("client deleted"))

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_12_delete_client_invalid_api_key_response_403(self):
        client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        deleted_client = requests.delete(f"{URL}/client/{client_id}",
                                         headers={HttpHeaders.ACCEPT: "application/json",
                                                  "X-API-KEY": "invalid_api_key"})
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(403))
        assert_that(deleted_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_13_delete_client_missing_api_key_response_403(self):
        client_data = create_user_data()
        create_client = requests.post(f"{URL}/client",
                                      json=client_data,
                                      headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        client_id = create_client.json()["id"]
        deleted_client = requests.delete(f"{URL}/client/{client_id}",
                                         headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": ""})
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(403))
        assert_that(deleted_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def test_13_delete_client_response_404(self):
        deleted_client = requests.delete(f"{URL}/client/777",
                                         headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key})
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(404))
        assert_that(deleted_client_data["message"], equal_to("client not found"))


if __name__ == '__main__':
    unittest.main()
