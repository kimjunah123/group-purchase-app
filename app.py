import streamlit as st
import json
import os

# File to store sign-ups
SIGNUPS_FILE = "signups.txt"

# Load sign-ups from file
if os.path.exists(SIGNUPS_FILE):
    with open(SIGNUPS_FILE, "r") as file:
        signups = json.load(file)
else:
    signups = {}

# Streamlit UI
st.title("📦 Group Purchase Tracker")
st.write("Join the group purchase and unlock an exclusive discount!")

# User Input: Choose a Product
product = st.selectbox("Select a Product:", ["Product A", "Product B", "Product C"])

# Set group purchase goal
GOAL = 5

# Initialize sign-ups for selected product
if product not in signups:
    signups[product] = []

# Show progress bar
st.progress(len(signups[product]) / GOAL)
st.write(f"👥 {len(signups[product])} out of {GOAL} people have joined for {product}.")

# User Input: Enter Username
username = st.text_input("Enter your name:")

# Join the purchase
if st.button("🚀 Join the Purchase"):
    if username and username not in signups[product]:
        signups[product].append(username)
        with open(SIGNUPS_FILE, "w") as file:
            json.dump(signups, file)  # Save updated sign-ups
        st.success(f"🎉 {username}, you have joined {product}!")
        st.rerun()
    elif username in signups[product]:
        st.warning("⚠ You have already joined!")
    else:
        st.error("❌ Please enter your name.")

# Show Completion Message
if len(signups[product]) >= GOAL:
    st.balloons()
    st.success(f"🎊 Group purchase for {product} unlocked!")
