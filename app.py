import streamlit as st
import pandas as pd
import json
import os

from sympy import public

#path to local JSON storage
DATA_FILE = "data/users.josn"

SWAP_FILE = "data/swaps.json"

def load_swaps():
    if os.path.exists(SWAP_FILE):
        with open(SWAP_FILE, "r") as file:
            return json.load(file)
    return []

def save_swaps(swaps):
    with open(SWAP_FILE, "w") as file:
        json.dump(swaps, file, indent=4)

def send_swap_request(from_user, to_user, skill):
    swaps = load_swaps()
    request = {
        "from": from_user,
        "to": to_user,
        "skill": skill,
        "status": "pending"
    }
    swaps.append(request)
    save_swaps(swaps)

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

st.subheader("My Swap Requests")

swaps = load_swaps()

# Outgoing requests
outgoing = [s for s in swaps if s["from"] == name]
if outgoing:
    for req in outgoing:
        st.markdown(f"You requested **{req['skill']}** from **{req['to']}** – *Status: {req['status']}*")
else:
    st.info("No outgoing swap requests.")

st.subheader("Incoming Swap Requests")

incoming = [s for s in swaps if s["to"] == name and s["status"] == "pending"]

if incoming:
    for i, req in enumerate(incoming):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{req['from']}** wants to swap for **{req['skill']}**")

        with col2:
            accept = st.button(f"Accept {i}", key=f"accept_{i}")
            reject = st.button(f"Reject {i}", key=f"reject_{i}")

        if accept:
            req["status"] = "accepted"
            save_swaps(swaps)
            st.success(f"Accepted request from {req['from']}!")

        if reject:
            req["status"] = "rejected"
            save_swaps(swaps)
            st.warning(f"Rejected request from {req['from']}.")
else:
    st.info("No incoming requests right now.")

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
    # Skip button if you're viewing your own profile
    if user["name"] != name:
        if st.button(f"Send Swap Request to {user['name']} for {search_skill}", key=user['name']):
            send_swap_request(name, user["name"], search_skill)
            st.success(f"Swap request sent to {user['name']}!")

        st.divider()
else:
    st.info("No matching profiles found. Try another skill or create one!")

