import unittest

from crud.crud_methods import CrudMethods
from helpers.client_data import *
from hamcrest import assert_that, equal_to, has_entries, not_

CLEANUP = []


class ClientTests(unittest.TestCase):
    cm = CrudMethods()
    
    @classmethod
    def setUpClass(cls):
        global api_key
        api_key = cls.cm.return_api_key()

    @classmethod
    def tearDownClass(cls):
        for client_id in CLEANUP:
            cls.cm._delete("/client", client_id, api_key)

    def test_01_get_client_response_200(self):
        client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        create_client_data = create_client.json()
        client_id = create_client.json()["id"]
        returned_client = self.cm._read(f"/client/{client_id}", api_key)
        returned_client_data = returned_client.json()
        assert_that(returned_client.status_code, equal_to(200))
        assert_that(returned_client_data, has_entries(create_client_data))
        CLEANUP.append(client_id)

    def test_02_get_client_invalid_api_key_response_403(self):
        client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        returned_client = self.cm._read(f"/client/{client_id}", "invalid_api_key")
        returned_client_data = returned_client.json()
        assert_that(returned_client.status_code, equal_to(403))
        assert_that(returned_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    def test_03_get_client_missing_api_key_response_403(self):
        client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        returned_client = self.cm._read(f"/client/{client_id}", "")
        returned_client_data = returned_client.json()
        assert_that(returned_client.status_code, equal_to(403))
        assert_that(returned_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    def test_04_put_client_response_200(self):
        client_data = create_user_data()
        updated_client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        updated_client = self.cm._update(f"/client", client_id, updated_client_data, api_key)
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(200))
        assert_that(updated_client_data, not_(equal_to(has_entries(client_data))))
        assert_that(updated_client_data["id"], equal_to(client_id))
        CLEANUP.append(client_id)

    def test_05_put_client_response_invalid_400(self):
        client_data = create_user_data()
        updated_empty_client_data = {}
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        updated_client = self.cm._update(f"/client", client_id, updated_empty_client_data, api_key)
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("invalid request"))
        CLEANUP.append(client_id)

    def test_06_put_client_response_without_first_name_400(self):
        client_data = create_user_data()
        updated_partial_client_data = create_user_data()
        del updated_partial_client_data["firstName"]
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        updated_client = self.cm._update(f"/client", client_id, updated_partial_client_data, api_key)
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("firstName is required"))
        CLEANUP.append(client_id)

    def test_07_put_client_response_without_last_name_400(self):
        client_data = create_user_data()
        updated_partial_client_data = create_user_data()
        del updated_partial_client_data["lastName"]
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        updated_client = self.cm._update(f"/client", client_id, updated_partial_client_data, api_key)
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("lastName is required"))
        CLEANUP.append(client_id)

    def test_08_put_client_response_without_phone_400(self):
        client_data = create_user_data()
        updated_partial_client_data = create_user_data()
        del updated_partial_client_data["phone"]
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        updated_client = self.cm._update(f"/client", client_id, updated_partial_client_data, api_key)
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(400))
        assert_that(updated_client_data["message"], equal_to("phone is required"))
        CLEANUP.append(client_id)

    def test_09_put_client_invalid_api_key_response_403(self):
        client_data = create_user_data()
        updated_client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        updated_client = self.cm._update(f"/client", client_id, updated_client_data, "invalid_api_kay")
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(403))
        assert_that(updated_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    def test_10_put_client_missing_api_key_response_403(self):
        client_data = create_user_data()
        updated_client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        updated_client = self.cm._update(f"/client", client_id, updated_client_data, "")
        updated_client_data = updated_client.json()
        assert_that(updated_client.status_code, equal_to(403))
        assert_that(updated_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    def test_11_delete_client_response_200(self):
        client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        deleted_client = self.cm._delete("/client", client_id, api_key)
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(200))
        assert_that(deleted_client_data["message"], equal_to("client deleted"))

    def test_12_delete_client_invalid_api_key_response_403(self):
        client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        deleted_client = self.cm._delete("/client", client_id, "invalid_api_key")
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(403))
        assert_that(deleted_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    def test_13_delete_client_missing_api_key_response_403(self):
        client_data = create_user_data()
        create_client = self.cm._create("/client", client_data, api_key)
        client_id = create_client.json()["id"]
        deleted_client = self.cm._delete("/client", client_id, "")
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(403))
        assert_that(deleted_client_data["message"], equal_to("invalid or missing api key"))
        CLEANUP.append(client_id)

    def test_13_delete_client_response_404(self):
        deleted_client = self.cm._delete("/client", "777", api_key)
        deleted_client_data = deleted_client.json()
        assert_that(deleted_client.status_code, equal_to(404))
        assert_that(deleted_client_data["message"], equal_to("client not found"))


if __name__ == '__main__':
    unittest.main()
