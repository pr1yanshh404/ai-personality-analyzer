import streamlit as st
import pandas as pd
import pickle
from openai import OpenAI
import matplotlib.pyplot as plt
from database import *

# ---------------- INIT DB ----------------
create_db()

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Personality Analyzer", layout="centered")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- OPENAI ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH ----------------
st.title("🔐 Login / Signup")

menu = ["Login", "Signup"]
choice = st.selectbox("Select", menu)

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if choice == "Signup":
    if st.button("Create Account"):
        add_user(username, password)
        st.success("Account created! Login now.")

elif choice == "Login":
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.user = username
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

# ---------------- MAIN APP ----------------
if st.session_state.user:

    st.title("🧠 AI Personality Analyzer")

    social = st.slider("Social Time", 0, 10)
    screen = st.slider("Screen Time", 0, 12)
    sleep = st.slider("Sleep", 0, 12)
    study = st.slider("Study", 0, 10)

    if st.button("Analyze"):

        input_data = pd.DataFrame([[social, screen, sleep, study]],
                                 columns=["social_time", "screen_time", "sleep_hours", "study_hours"])

        result = model.predict(input_data)[0]
        personality = "Extrovert 😎" if result == 1 else "Introvert 🧠"

        st.success(f"Prediction: {personality}")

        # Save to DB
        save_history(st.session_state.user, social, screen, sleep, study, personality)

        # Chart
        fig, ax = plt.subplots()
        ax.bar(["Social", "Screen", "Sleep", "Study"], [social, screen, sleep, study])
        st.pyplot(fig)

        # AI
        prompt = f"Analyze lifestyle: {social},{screen},{sleep},{study}"
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response.choices[0].message.content)

    # ---------------- HISTORY ----------------
    st.subheader("📜 Your History")
    history = get_history(st.session_state.user)

    if history:
        df = pd.DataFrame(history, columns=["User","Social","Screen","Sleep","Study","Result"])
        st.dataframe(df)

    if st.button("Logout"):
        st.session_state.user = None



