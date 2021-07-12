from faker import Faker
from src.database.repository import PositionRepository

faker = Faker()

for id in range(1, 100):
    user_id = id
    for position in range(5):
        x_axis = faker.random_number(digits=3)
        y_axis = faker.random_number(digits=3)
        date_time = faker.date_time()
        trajectory = faker.binary(length=32)

        position_repository = PositionRepository()
        position_inserted = position_repository.insert_position(
            x_axis=x_axis,
            y_axis=y_axis,
            date_time=date_time,
            trajectory=trajectory,
            user_id=user_id,
        )
