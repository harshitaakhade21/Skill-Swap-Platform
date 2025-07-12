import csv
import json

csv_file = "fake_users.csv"
json_file = "data/users.json"

users = []

with open(csv_file, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        users.append({
            "name": row["name"],
            "email": row["email"],
            "password": row["password"],
            "location": row["location"],
            "skills_offered": [s.strip() for s in row["skills_offered"].split(",")],
            "skills_wanted": [s.strip() for s in row["skills_wanted"].split(",")],
            "availability": row["availability"],
            "public": row["public"] == "True",
            "photo": ""
        })

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(users, f, indent=4)

