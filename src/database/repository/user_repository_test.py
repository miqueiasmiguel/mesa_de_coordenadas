from faker import Faker
from src.database.repository import UserRepository


faker = Faker()


def test_insert_select_and_delete_user():

    # Parametros da tabela users
    reg_number = faker.random_number(digits=10)
    name = faker.name()
    email = faker.email()
    password = faker.word()
    special = faker.boolean()

    user_repository = UserRepository()
    user_inserted = user_repository.insert_user(
        reg_number=reg_number,
        name=name,
        email=email,
        password=password,
        special=special,
    )
    print("user inserted: {}".format(user_inserted))
    user_selected = user_repository.select_user(reg_number=reg_number)
    print("user selected: {}".format(user_selected))
    user_repository.delete_user(reg_number=reg_number)
