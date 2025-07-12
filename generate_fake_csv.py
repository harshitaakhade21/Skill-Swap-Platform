import csv
from faker import Faker
import random

fake = Faker()

skills_pool = [
    "Python", "Java", "C++", "JavaScript", "Excel", "Public Speaking",
    "Data Analysis", "Graphic Design", "SEO", "Writing", "Photography"
]

availability_options = ["Weekdays", "Weekends", "Evenings", "Anytime"]

with open("fake_users.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=[
        "name", "email", "password", "location",
        "skills_offered", "skills_wanted", "availability", "public"
    ])
    writer.writeheader()

    for _ in range(20):
        offered = random.sample(skills_pool, k=2)
        wanted = random.sample([s for s in skills_pool if s not in offered], k=2)

        writer.writerow({
            "name": fake.name(),
            "email": fake.email(),
            "password": "1234",
            "location": fake.city(),
            "skills_offered": ", ".join(offered),
            "skills_wanted": ", ".join(wanted),
            "availability": random.choice(availability_options),
            "public": True
        })
