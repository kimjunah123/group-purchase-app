import streamlit as st
import time

# Group purchase goal
GOAL = 5

# Simulate a database storage with session state
if "signups" not in st.session_state:
    st.session_state.signups = 0

# Streamlit UI
st.title("📦 Group Purchase Tracker")
st.write("Join the group purchase and unlock an exclusive discount!")

# Display progress bar
st.progress(st.session_state.signups / GOAL)
st.write(f"👥 {st.session_state.signups} out of {GOAL} people have joined.")

# Button to sign up
if st.button("🚀 Join the Purchase"):
    if st.session_state.signups < GOAL:
        st.session_state.signups += 1
        st.success("🎉 You have joined the purchase!")
        time.sleep(2)
        st.experimental_rerun()
    else:
        st.warning("✅ Purchase goal reached! Check your email for the deal.")

# Show completion message if goal is reached
if st.session_state.signups >= GOAL:
    st.balloons()
    st.success("🎊 Group purchase unlocked!")
