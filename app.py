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

# User Input: Enter Name and Email
username = st.text_input("Enter your name:")
email = st.text_input("Enter your email:")

# User Input: Choose Products and Quantity
products = {"Product A": 5, "Product B": 10, "Product C": 15}
selected_products = st.multiselect("Select Products:", list(products.keys()))
product_quantities = {product: st.number_input(f"Quantity for {product}", min_value=1, max_value=100, value=1) for product in selected_products}

# Initialize sign-ups for selected products
for product in selected_products:
    if product not in signups:
        signups[product] = []

# Show progress bars based on total product quantity
for product in selected_products:
    total_quantity = sum(item["quantity"] for item in signups[product]) if signups[product] else 0
    goal = products[product]  # Goal is now based on product quantity
    st.progress(total_quantity / goal)
    st.write(f"📦 {total_quantity} out of {goal} units have been purchased for {product}.")

# Join the purchase
if st.button("🚀 Join the Purchase"):
    if username and email and selected_products:
        for product, quantity in product_quantities.items():
            signups[product].append({"name": username, "email": email, "quantity": quantity})
        with open(SIGNUPS_FILE, "w") as file:
            json.dump(signups, file)  # Save updated sign-ups
        st.success(f"🎉 {username}, you have joined the purchase for {', '.join(selected_products)}!")
        st.rerun()
    else:
        st.error("❌ Please enter your name, email, and select at least one product.")

# Show Completion Message
for product in selected_products:
    total_quantity = sum(item["quantity"] for item in signups[product]) if signups[product] else 0
    goal = products[product]
    if total_quantity >= goal:
        st.balloons()
        st.success(f"🎊 Group purchase for {product} unlocked!")
