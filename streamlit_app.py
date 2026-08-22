import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image
from crop_disease import disease_detection   # 👈 add this

# ================================
# Page Config
# ================================
st.set_page_config(page_title="AI Crop Assistant", layout="wide")

st.title("🌾 AI Crop Yield, Disease & Farmer Assistant")

# ================================
# Load ML Files
# ================================
model, feature_columns = joblib.load("best_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")
median_values = joblib.load("median_values.pkl")

# ================================
# Sidebar
# ================================
menu = st.sidebar.selectbox(
    "Select Feature",
    ["Yield Prediction", "Disease Detection", "Chatbot"]
)

# ================================
# YIELD PREDICTION
# ================================
if menu == "Yield Prediction":

    st.header("📊 Crop Yield Prediction")

    crop = st.selectbox("Crop", label_encoders["Crop"].classes_)
    state = st.selectbox("State", label_encoders["State"].classes_)
    season = st.selectbox("Season", label_encoders["Season"].classes_)

    year = st.number_input("Crop Year", 1990, 2050, 2024)

    rain = st.number_input(
        "Annual Rainfall (mm)",
        0.0, 10000.0,
        float(median_values["Annual_Rainfall"])
    )

    fert_default = min(float(median_values["Fertilizer"]), 5000.0)
    fert = st.number_input("Fertilizer Use (kg/ha)", 0.0, 5000.0, fert_default)

    pest_default = min(float(median_values["Pesticide"]), 5000.0)
    pest = st.number_input("Pesticide Use (kg/ha)", 0.0, 5000.0, pest_default)

    if st.button("🌱 Predict Yield"):
        c = label_encoders["Crop"].transform([crop])[0]
        s = label_encoders["State"].transform([state])[0]
        se = label_encoders["Season"].transform([season])[0]

        input_data = np.array([[c, s, se, year, rain, fert, pest]])
        prediction = model.predict(input_data)

        st.success(f"🌾 Predicted Yield: {prediction[0]:.2f} tons per hectare")

# ================================
# DISEASE DETECTION
# ================================
elif menu == "Disease Detection":

    disease_detection()   # 👈 call function

# ================================
# CHATBOT
# ================================
elif menu == "Chatbot":

    st.header("🤖 Farmer AI Chatbot")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    language = st.selectbox("Language", ["English", "Telugu"])

    user_msg = st.text_input("Ask about crops, fertilizer, disease, yield")

    def bot_reply(msg):
        msg = msg.lower()

        if language == "English":

            if "rice" in msg:
                return "Rice grows well in Kharif season with good rainfall."
            elif "disease" in msg:
                return "Common diseases: Leaf blight, rust, blast."
            elif "fertilizer" in msg:
                return "Use Urea for nitrogen, DAP for phosphorus."
            else:
                return "Ask about crop, fertilizer or disease."

        else:

            if "rice" in msg or "vari" in msg:
                return "వరి పంట ఖరీఫ్ సీజన్ లో బాగా పెరుగుతుంది."
            elif "disease" in msg:
                return "సాధారణ వ్యాధులు: లీఫ్ బ్లైట్, రస్ట్, బ్లాస్ట్."
            elif "fertilizer" in msg:
                return "నైట్రోజన్ కోసం యూరియా వాడండి."
            else:
                return "పంట లేదా వ్యాధి గురించి అడగండి."

    if st.button("Send"):
        if user_msg:
            reply = bot_reply(user_msg)
            st.session_state.chat.append(("You", user_msg))
            st.session_state.chat.append(("Bot", reply))

    for speaker, msg in st.session_state.chat:
        st.write(f"{speaker}: {msg}")