from faker import Faker


def create_user_data():
    faker = Faker("pl_PL")
    return {"firstName": faker.first_name(), "lastName": faker.last_name(), "phone": faker.phone_number()}


def create_user_data_without_first_name():
    faker = Faker("pl_PL")
    return {"lastName": faker.last_name(), "phone": faker.phone_number()}


def create_user_data_without_last_name():
    faker = Faker("pl_PL")
    return {"firstName": faker.first_name(), "phone": faker.phone_number()}


def create_user_data_without_phone():
    faker = Faker("pl_PL")
    return {"firstName": faker.first_name(), "lastName": faker.last_name()}
