import streamlit as st
import pandas as pd
import json
import os

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
availability = st.sidebar.text_input("Availability", ["weekdays", "weekends","Evening", "Flexible"])
profile_photo = st.sidebar.checkbox("Make my profile public", value=True)

