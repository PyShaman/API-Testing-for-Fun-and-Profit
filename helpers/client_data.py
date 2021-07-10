from faker import Faker


def create_user_data():
    faker = Faker("pl_PL")
    return {"firstName": faker.first_name(), "lastName": faker.last_name(), "phone": faker.phone_number()}
