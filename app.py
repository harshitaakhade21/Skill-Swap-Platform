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

name = 