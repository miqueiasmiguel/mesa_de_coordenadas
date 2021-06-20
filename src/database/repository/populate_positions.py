from faker import Faker
from src.database.repository import PositionRepository

faker = Faker()

for reg in range(1, 100):
    user_reg = reg
    for position in range(5):
        x_axis = faker.random_number(digits=3)
        y_axis = faker.random_number(digits=3)
        date_time = faker.date_time()
        trajectory = faker.csv(
            data_columns=("{{random_number}}", "{{random_number}}"),
            num_rows=10,
            include_row_ids=False,
        )
        state = faker.random_element(elements=("ini", "int", "fin"))
        velocity = faker.pyfloat(
            left_digits=2, right_digits=2, positive=True, min_value=1, max_value=15
        )

        position_repository = PositionRepository()
        position_inserted = position_repository.insert_position(
            x_axis=x_axis,
            y_axis=y_axis,
            date_time=date_time,
            trajectory=trajectory,
            state=state,
            velocity=velocity,
            user_reg=user_reg,
        )
