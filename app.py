import streamlit as st
import pickle
import pandas as pd
from openai import OpenAI

# ------------------ CONFIG ------------------
st.set_page_config(page_title="AI Personality Analyzer", layout="centered")

# ------------------ LOAD MODEL ------------------
model = pickle.load(open("model.pkl", "rb"))

# ------------------ OPENAI ------------------
client = OpenAI()

# ------------------ CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
    color:#00e6ff;
    margin-bottom:10px;
}
.subtitle {
    text-align:center;
    color:#ccc;
    margin-bottom:30px;
}
.chat-box {
    background:#1c1c1c;
    padding:15px;
    border-radius:10px;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown("<div class='title'>🧠 AI Personality Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Predict personality using AI + lifestyle insights 🚀</div>", unsafe_allow_html=True)

# ------------------ INPUT ------------------
social = st.slider("📱 Social Time (hours/day)", 0, 10)
screen = st.slider("💻 Screen Time (hours/day)", 0, 12)
sleep = st.slider("😴 Sleep (hours/day)", 0, 12)
study = st.slider("📚 Study Hours", 0, 10)

# ------------------ PREDICT ------------------
if st.button("🚀 Predict Personality"):

    input_data = pd.DataFrame([[social, screen, sleep, study]],
                              columns=["social_time", "screen_time", "sleep_hours", "study_hours"])

    result = model.predict(input_data)[0]

    if result == 0:
        personality = "Introvert"
    else:
        personality = "Extrovert"

    st.success(f"🎯 Prediction: {personality}")

    # ------------------ AI SUGGESTIONS ------------------
    with st.spinner("🤖 Generating AI suggestions..."):

        prompt = f"""
        User personality is {personality}.
        Social time: {social}
        Screen time: {screen}
        Sleep: {sleep}
        Study: {study}

        Give personalized self-improvement tips in short bullet points.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        ai_text = response.choices[0].message.content

    st.markdown("### 🤖 AI Suggestions")
    st.write(ai_text)

# ------------------ CHATBOT ------------------
st.markdown("## 💬 Ask AI about your personality")

user_input = st.text_input("Type your question...")

if user_input:
    with st.spinner("Thinking..."):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a personality coach AI."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content

    st.markdown("### 🤖 AI Reply")
    st.write(reply)