from faker import Faker
from datetime import timedelta

faker = Faker()

date_time = faker.date_time_this_month()
date_time_srt = date_time.strftime("%Y-%m-%d %H:%M:%S")
print(date_time)
print(date_time_srt)

new_date_time = date_time + timedelta(hours=2)

print(new_date_time)
