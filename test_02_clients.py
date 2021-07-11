import unittest

from crud.crud_methods import CrudMethods
from hamcrest import assert_that, equal_to


class ClientsTests(unittest.TestCase):
    cm = CrudMethods()

    @classmethod
    def setUpClass(cls):
        global api_key
        api_key = cls.cm.return_api_key()

    def test_01_get_clients_response_200(self):
        clients = self.cm._read("/clients", api_key)
        assert_that(clients.status_code, equal_to(200))

    def test_02_get_clients_invalid_api_key_response_403(self):
        clients = self.cm._read("/clients", "invalid_api_key")
        assert_that(clients.status_code, equal_to(403))
        assert_that(clients.json()["message"], equal_to("invalid or missing api key"))

    def test_03_get_clients_missing_api_key_response_403(self):
        clients = self.cm._read("/clients", "")
        assert_that(clients.status_code, equal_to(403))
        assert_that(clients.json()["message"], equal_to("invalid or missing api key"))


if __name__ == '__main__':
    unittest.main()
