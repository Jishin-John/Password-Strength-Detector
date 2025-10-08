import streamlit as st
import pandas as pd
import joblib
import math

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

# Predict password strength
def predict_strength(pwd):
    features = extract_features(pwd)
    df = pd.DataFrame([features])
    result = model.predict(df)[0]
    return ["Weak", "Medium", "Strong"][result]

# Estimate crack time
def estimate_crack_time(pwd):
    length = len(pwd)
    has_lower = any(c.islower() for c in pwd)
    has_upper = any(c.isupper() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(not c.isalnum() for c in pwd)

    charset_size = 0
    if has_lower: charset_size += 26
    if has_upper: charset_size += 26
    if has_digit: charset_size += 10
    if has_special: charset_size += 32

    total_combinations = charset_size ** length
    guesses_per_second = 1_000_000_000  # 1 billion
    seconds = total_combinations / guesses_per_second

    return convert_seconds(seconds)

# Convert time to readable format
def convert_seconds(seconds):
    if seconds < 1:
        return "less than 1 second"
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    years = days / 365

    if years > 1000:
        return "∞ (virtually uncrackable)"
    elif years >= 1:
        return f"{years:.2f} years"
    elif days >= 1:
        return f"{days:.2f} days"
    elif hours >= 1:
        return f"{hours:.2f} hours"
    elif minutes >= 1:
        return f"{minutes:.2f} minutes"
    else:
        return f"{seconds:.2f} seconds"

# --- Streamlit UI ---
st.set_page_config(page_title="Password Strength Detector")
st.title("😎Password Strength Detector")
st.markdown("Enter a password to see how secure it is:")

password = st.text_input("🔑 Your Password")

if password:
    strength = predict_strength(password)
    crack_time = estimate_crack_time(password)

    st.markdown(f"🛡️ Password Strength: **{strength}**")
    st.markdown(f"⏱️ Estimated Time to Crack by Brute Force Method: **{crack_time}**")

