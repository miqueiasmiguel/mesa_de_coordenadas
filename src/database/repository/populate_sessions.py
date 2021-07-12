from datetime import timedelta
from faker import Faker
from src.database.repository import SessionRepository


faker = Faker()

for id in range(1, 100):
    login_time = faker.date_time()
    login_time_str = login_time.strftime("%Y-%m-%d %H:%M:%S")
    logout_time = login_time + timedelta(hours=2)
    logout_time_str = logout_time.strftime("%Y-%m-%d %H:%M:%S")
    user_id = id

    session_repository = SessionRepository()
    session_inserted = session_repository.insert_session(
        login_time=login_time_str, logout_time=logout_time_str, user_id=user_id
    )
