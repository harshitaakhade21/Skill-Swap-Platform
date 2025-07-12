import streamlit as st
import pandas as pd
import json
import os

from sympy import public

#path to local JSON storage
DATA_FILE = "data/users.josn"

#Load existing users
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# save user to JSON
def save_user(user_data):
    users = load_users()
    users.append(user_data)
    with open(DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

st.set_page_config(page_title="Skill Swap Platform", layout="centered")
st.title("Skill Swap Platform")

st.sidebar.header("Create Your Profile")

name = st.sidebar.text_input("Name")
skills_offered = st.sidebar.text_input("Skills you offer (comma-separated)")
skills_wanted = st.sidebar.text_input("Skills you want (comma-separated)")
availability = st.sidebar.selectbox("Availability", ["Weekdays", "Weekends", "Evening", "Flexible"])
profile_photo = st.sidebar.checkbox("Make my profile public", value=True)

if st.sidebar.button("Submit Profile"):
    if name and skills_offered and skills_wanted:
        user_data = {
            "name": name,
            "skills_offered": [s.strip() for s in skills_offered.split(",")],
            "skills_wanted": [s.strip() for s in skills_wanted.split(",")],
            "availability": availability,
            "public": profile_photo
            
        }
        save_user(user_data)
        st.success("Profile submitted successfully!")
    else:
        st.warning("Please fill in all fields before submitting.")            
                         
    # Main Section: View Profiles
st.subheader("Browse Public Profiles by Skill")

search_skill = st.text_input("Search by skill (e.g., Python, Design)")
users = load_users()

# Filter by search
filtered_users = []
for user in users:
    if user["public"] and (
        search_skill.lower() in [s.lower() for s in user["skills_offered"]] or search_skill == ""):
        filtered_users.append(user)

if filtered_users:
    for user in filtered_users:
        st.markdown(f"""
        {user['name']}

        Offers:{', '.join(user['skills_offered'])}
        Wants:{', '.join(user['skills_wanted'])}
        Availability:{user['availability']}
""")
        st.divider()
else:
    st.info("No matching profiles found. Try another skill or create one!")

