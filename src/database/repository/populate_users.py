from faker import Faker
from src.database.repository import UserRepository

faker = Faker()

for reg in range(1, 100):
    reg_number = reg
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
