from faker import Faker
from datetime import timedelta
from src.database.repository import SessionRepository


faker = Faker()


def test_insert_and_delete_session():

    login_time = faker.date_time()
    login_time_str = login_time.strftime("%Y-%m-%d %H:%M:%S")
    logout_time = login_time + timedelta(hours=2)
    logout_time_str = logout_time.strftime("%Y-%m-%d %H:%M:%S")
    user_reg = faker.random_number(digits=10)

    session_repository = SessionRepository()
    session_inserted = session_repository.insert_session(
        login_time=login_time_str, logout_time=logout_time_str, user_reg=user_reg
    )
    print(session_inserted)
    id = session_inserted[0]
    session_repository.delete_session(id=id)
