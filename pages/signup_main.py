import streamlit as st

# Define CSS styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("signup_style.css")  # Update file name here

# Header
st.markdown("<h1 class='header'>Posture Priority - Sign Up</h1>", unsafe_allow_html=True)

# Form
with st.form("signup_form"):
    # Input fields
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    # Submit button
    submit_button = st.form_submit_button("Sign Up")

# Display error messages if passwords don't match
if password != confirm_password:
    st.error("Passwords do not match!")

# Display success message upon successful sign-up
if submit_button:
    st.success("You have successfully signed up!")

# Link to login page
st.markdown("Already have an account? [Login here](login)")
