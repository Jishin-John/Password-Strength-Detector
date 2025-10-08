import streamlit as st
import pandas as pd
import joblib

# Load the model
model = joblib.load("password_strength_model.pkl")

# Feature extraction
def extract_features(pwd):
    return {
        "length": len(pwd),
        "digits": sum(c.isdigit() for c in pwd),
        "upper": sum(c.isupper() for c in pwd),
        "lower": sum(c.islower() for c in pwd),
        "special": sum(not c.isalnum() for c in pwd)
    }

def predict_strength(pwd):
    features = extract_features(pwd)
    df = pd.DataFrame([features])
    result = model.predict(df)[0]
    return ["Weak", "Medium", "Strong"][result]

# Streamlit UI
st.set_page_config(page_title="Password Strength Detector")
st.title("🔐 Password Strength Detector")
st.markdown("Enter a password to see how secure it is:")

password = st.text_input("🔑 Your Password")

if password:
    strength = predict_strength(password)
    st.markdown(f"🛡️ Password Strength: **{strength}**")
