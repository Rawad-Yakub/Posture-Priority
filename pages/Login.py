import streamlit as st ##1.12.0 originally

import streamlit_authenticator as stauth                                ##user auth. in YAML
from streamlit_authenticator.utilities.hasher import Hasher


import numpy as np                                       
import pandas as pd

import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import s3fs
from st_files_connection import FilesConnection

import yaml
from yaml.loader import SafeLoader

##################################################

st.set_page_config(
    page_title="Login",
    page_icon="🚶",
    layout="centered",
    initial_sidebar_state='auto'
)

##################################################

# Define CSS styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#local_css("signup_style.css")  # Update file name here

# Header
##st.markdown("<h1 class='header'>Posture Priority - Sign Up</h1>", unsafe_allow_html=True)

# Form
##with st.form("signup_form"):
##    # Input fields
##    username = st.text_input("Username")
##    email = st.text_input("Email")
##    fname = st.text_input("First name")
##    password = st.text_input("Password", type="password")
##    confirm_password = st.text_input("Confirm Password", type="password")

    # Submit button
##    submit_button = st.form_submit_button("Sign Up")

# Display error messages if passwords don't match
##if password != confirm_password:
##    st.error("Passwords do not match!")

# Display success message upon successful sign-up
##if submit_button:
##    st.success("You have successfully signed up!")

# Link to login page
##st.markdown("Already have an account? [Login here](login)")

###

hashed_passwords = Hasher(['abc', 'def']).generate()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login()

if st.session_state["authentication_status"]:
    st.subheader("Log in or sign up to get started")
    st.page_link("Home.py", label="Home", icon="🏠")
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    loggedIn = True
    currUser = st.session_state["username"]
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


##reg doesnt save password, have to fix
##considering putting config.yaml into s3 
##also manually doing registration widget and writing directly to yaml
##maybe jus implement password chnanger, use abc as default password
try:
    email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user()
    if email_of_registered_user:
        config['credentials']['usernames'][username_of_registered_user] = {
                'email': email_of_registered_user,
                'logged_in': False,                                             # Assuming new users are not logged in by default
                'name': name_of_registered_user,
                ##'password': 'abc'                                 # You should hash and store the password securely
            }
        activeDates = {
            "upload_dates": currDate
        }
        #post_id = collection.insert_one(post).inserted_id
        #activeDates = fs.open("posturepriorityawsbucket/"+currUser, mode='rb')
        st.success('User registered successfully')
        with open('config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

except Exception as e:
    st.error(e)



if st.session_state["authentication_status"]:
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
            
    except Exception as e:
        st.error(e)