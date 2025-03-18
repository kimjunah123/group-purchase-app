import streamlit as st
import json
import os

# File to store sign-ups
SIGNUPS_FILE = "signups.txt"

# Debug: Check if the file exists and its content
if os.path.exists(SIGNUPS_FILE):
    st.sidebar.write("✅ signups.txt exists")
    with open(SIGNUPS_FILE, "r") as file:
        file_content = file.read()
        st.sidebar.write(f"📂 File Content:\n{file_content}")  # Show file content in the sidebar

# Ensure the file exists and contains valid JSON
if not os.path.exists(SIGNUPS_FILE) or os.stat(SIGNUPS_FILE).st_size == 0:
    st.sidebar.write("⚠ signups.txt is empty. Initializing it...")
    with open(SIGNUPS_FILE, "w") as file:
        json.dump({}, file)  # Initialize as an empty dictionary

# Load sign-ups safely
try:
    with open(SIGNUPS_FILE, "r") as file:
        signups = json.load(file)
    st.sidebar.write("✅ JSON Loaded Successfully")
except json.JSONDecodeError:
    st.sidebar.write("❌ JSONDecodeError: Resetting signups.txt")
    signups = {}  # Reset if there's an error in reading
    with open(SIGNUPS_FILE, "w") as file:
        json.dump(signups, file)

# Streamlit UI
st.title("📦 Group Purchase Tracker")
st.write("Join the group purchase and unlock an exclusive discount!")

# User Input: Enter Name and Email
username = st.text_input("Enter your name:")
email = st.text_input("Enter your email:")

# User Input: Choose Products and Quantity
products = {"Collagen Glowshot": 300, "Aqua Bank": 500, "Aqua Rich Double Up C": 500}
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

# ---- ADMIN PANEL ---- #
st.sidebar.title("🔑 Admin Panel")
if st.sidebar.checkbox("Show Sign-Up Data"):
    all_entries = []
    
    # Flatten data for display
    for product, entries in signups.items():
        for entry in entries:
            all_entries.append({
                "Product": product,
                "Name": entry["name"],
                "Email": entry["email"],
                "Quantity": entry["quantity"]
            })

    if all_entries:
        df = pd.DataFrame(all_entries)
        st.sidebar.write(df)

        # Download as CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button(
            label="📥 Download Sign-Up Data",
            data=csv,
            file_name="group_purchase_signups.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.write("No sign-ups yet.")
