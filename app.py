import streamlit as st
import json
import os
from datetime import datetime

# ===== File Paths =====
USER_FILE = "data/users.json"
SWAP_FILE = "data/swap.json"
FEEDBACK_FILE = "data/feedback.json"
MESSAGE_FILE = "data/messages.json"

# ===== Utility Functions =====
def load_json(file_path):
    return json.load(open(file_path)) if os.path.exists(file_path) else []

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_users(): return load_json(USER_FILE)
def save_users(users): save_json(USER_FILE, users)

def load_swaps(): return load_json(SWAP_FILE)
def save_swaps(data): save_json(SWAP_FILE, data)

def load_feedback(): return load_json(FEEDBACK_FILE)
def save_feedback(data): save_json(FEEDBACK_FILE, load_feedback() + [data])

def load_messages(): return load_json(MESSAGE_FILE)
def save_messages(data): save_json(MESSAGE_FILE, data)

def get_pending_incoming_requests(username, swaps):
    return [req for req in swaps if req["to"] == username and req["status"] == "pending"]

# ===== Login Logic =====
def login_user(email, password):
    users = load_users()
    for user in users:
        if user.get("email") == email and user.get("password") == password:
            return user
    return None

# ===== Auth Setup =====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = {}

# ===== Login Page =====
if not st.session_state.logged_in:
    st.title("Skill Swap Platform Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid email or password")
    st.markdown("ℹ️ Your account must be pre-created in `users.json`.")

# ===== Main App =====
else:
    user = st.session_state.user
    name = user["name"]
    swaps = load_swaps()
    users = load_users()
    feedbacks = load_feedback()
    messages = load_messages()

    pending_incoming = get_pending_incoming_requests(name, swaps)
    notification_count = len(pending_incoming)

    st.sidebar.title(f"👤 Welcome, {name}")
    st.sidebar.markdown(f"🔔 You have **{notification_count}** pending request(s)")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = {}
        st.rerun()

    st.title("🔄 Skill Swap Platform")

    tabs = st.tabs([
        "🌍 Browse Profiles", "📤 My Requests", "📥 Incoming", 
        "✅ Swap History", "💬 Messages", "📝 Feedback", "⚙️ Profile"
    ])

    # ===== Tab 0: Browse Profiles =====
    with tabs[0]:
        st.subheader("Browse Public Profiles by Skill")
        search_skill = st.text_input("Search skill (e.g., Python, Excel)")
        filtered_users = [
            u for u in users if u.get("public") and u.get("name") != name and (
                search_skill.lower() in [s.lower() for s in u.get("skills_offered", [])] or search_skill == ""
            )
        ]
        for u in filtered_users:
            with st.expander(f"{u['name']} — Offers: {', '.join(u['skills_offered'])}"):
                st.markdown(f"- Wants: {', '.join(u['skills_wanted'])}")
                st.markdown(f"- Availability: {u['availability']}")
                if st.button(f"Send Request to {u['name']}", key=f"request_{u['email']}"):
                    swaps.append({
                        "from": name,
                        "to": u["name"],
                        "skill": search_skill or "any",
                        "status": "pending"
                    })
                    save_swaps(swaps)
                    st.success(f"Request sent to {u['name']}!")

    # ===== Tab 1: My Requests =====
    with tabs[1]:
        st.subheader("📤 My Swap Requests")
        outgoing = [s for s in swaps if s["from"] == name]
        if outgoing:
            for i, req in enumerate(outgoing):
                with st.expander(f"To: {req['to']} | Skill: {req['skill']} | Status: {req['status']}"):
                    if req["status"] == "pending":
                        if st.button("Delete", key=f"delete_{i}"):
                            swaps.remove(req)
                            save_swaps(swaps)
                            st.warning(f"Deleted request to {req['to']}")
                    if req["status"] == "accepted":
                        fb = st.text_input("Leave feedback", key=f"fb_{i}")
                        if st.button("Submit Feedback", key=f"submit_fb_{i}"):
                            save_feedback({
                                "from": name,
                                "to": req["to"],
                                "skill": req["skill"],
                                "message": fb
                            })
                            st.success("Feedback submitted!")
        else:
            st.info("No outgoing requests.")

    # ===== Tab 2: Incoming Requests =====
    with tabs[2]:
        st.subheader("📥 Incoming Swap Requests")
        incoming = [s for s in swaps if s["to"] == name and s["status"] == "pending"]
        if incoming:
            for i, req in enumerate(incoming):
                with st.expander(f"From: {req['from']} | Skill: {req['skill']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Accept", key=f"accept_{i}"):
                            req["status"] = "accepted"
                            save_swaps(swaps)
                            st.success(f"Accepted request from {req['from']}")
                    with col2:
                        if st.button("Reject", key=f"reject_{i}"):
                            req["status"] = "rejected"
                            save_swaps(swaps)
                            st.warning(f"Rejected request from {req['from']}")
        else:
            st.info("No incoming requests.")

    # ===== Tab 3: Swap History =====
    with tabs[3]:
        st.subheader("✅ Accepted / Rejected Swap History")
        history = [
            s for s in swaps if (s["from"] == name or s["to"] == name)
            and s["status"] in ["accepted", "rejected"]
        ]
        if history:
            for h in history:
                st.markdown(f"- **{h['from']} ➡️ {h['to']}** | Skill: *{h['skill']}* | Status: `{h['status'].upper()}`")
        else:
            st.info("No accepted or rejected swaps yet.")

    # ===== Tab 4: Messaging =====
    with tabs[4]:
        st.subheader("💬 Message Inbox")
        inbox = [m for m in messages if m["to"] == name]
        if inbox:
            for msg in reversed(inbox):
                st.markdown(f"**From {msg['from']}** at {msg['timestamp']}:\n> {msg['message']}")
        else:
            st.info("No messages received yet.")

        st.subheader("✉️ Send a Message")
        recipient = st.selectbox("Send To", [u["name"] for u in users if u["name"] != name])
        message = st.text_area("Your Message")
        if st.button("Send Message"):
            messages.append({
                "from": name,
                "to": recipient,
                "message": message,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_messages(messages)
            st.success(f"Message sent to {recipient}!")

    # ===== Tab 5: Feedback Given =====
    with tabs[5]:
        st.subheader("📝 Feedback Given")
        my_feedback = [f for f in feedbacks if f["from"] == name]
        if my_feedback:
            for f in my_feedback:
                st.markdown(f"- To **{f['to']}** on *{f['skill']}*: “{f['message']}”")
        else:
            st.info("You haven’t submitted any feedback yet.")

    # ===== Tab 6: My Profile =====
    with tabs[6]:
        st.subheader("⚙️ My Profile")
        col1, col2 = st.columns(2)
        with col1:
            name_input = st.text_input("Name", user.get("name", ""))
            skills_offered = st.text_input("Skills Offered (comma-separated)", ", ".join(user.get("skills_offered", [])))
        with col2:
            location = st.text_input("Location", user.get("location", ""))
            skills_wanted = st.text_input("Skills Wanted (comma-separated)", ", ".join(user.get("skills_wanted", [])))

        availability = st.selectbox(
            "Availability",
            ["Weekdays", "Weekends", "Evenings", "Anytime"],
            index=["Weekdays", "Weekends", "Evenings", "Anytime"].index(user.get("availability", "Weekdays"))
        )

        is_public = st.checkbox("Make Profile Public", value=user.get("public", False))

        profile_photo = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])
        if profile_photo:
            os.makedirs("profile_photos", exist_ok=True)
            photo_path = f"profile_photos/{user['email']}.jpg"
            with open(photo_path, "wb") as f:
                f.write(profile_photo.getbuffer())
            user["photo"] = photo_path
            st.image(photo_path, width=150)

        if st.button("Save Profile"):
            user["name"] = name_input
            user["location"] = location
            user["availability"] = availability
            user["skills_offered"] = [s.strip() for s in skills_offered.split(",") if s.strip()]
            user["skills_wanted"] = [s.strip() for s in skills_wanted.split(",") if s.strip()]
            user["public"] = is_public
            for u in users:
                if u["email"] == user["email"]:
                    u.update(user)
            save_users(users)
            st.success("Profile updated successfully!")

        st.markdown("### Your Profile Preview")
        photo_path = user.get("photo")
        if photo_path and os.path.exists(photo_path):
            st.image(photo_path, width=100)
        else:
            st.markdown("_No profile photo uploaded._")

        st.markdown(f"**Name:** {user['name']}")
        st.markdown(f"**Location:** {user['location']}")
        st.markdown(f"**Availability:** {user['availability']}")
        st.markdown(f"**Skills Offered:** {', '.join(user['skills_offered'])}")
        st.markdown(f"**Skills Wanted:** {', '.join(user['skills_wanted'])}")



