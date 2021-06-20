from faker import Faker
from datetime import timedelta
from src.database.repository import SessionRepository


faker = Faker()

for reg in range(1, 100):
    login_time = faker.date_time()
    login_time_str = login_time.strftime("%Y-%m-%d %H:%M:%S")
    logout_time = login_time + timedelta(hours=2)
    logout_time_str = logout_time.strftime("%Y-%m-%d %H:%M:%S")
    user_reg = reg

    session_repository = SessionRepository()
    session_inserted = session_repository.insert_session(
        login_time=login_time_str, logout_time=logout_time_str, user_reg=user_reg
    )
