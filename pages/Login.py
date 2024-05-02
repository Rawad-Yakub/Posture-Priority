import streamlit as st ##1.12.0 originally
import streamlit_authenticator as stauth                                ##user auth. in YAML
from streamlit_authenticator.utilities.hasher import Hasher
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

# Define CSS styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#local_css("signup_style.css")  # Update file name here
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

##################################################
st.subheader("Log in or sign up to get started!")
st.page_link("Home.py", label="Home", icon="🏠")
    
name, authentication_status, username = authenticator.login()

if st.session_state["authentication_status"]:
    st.write(f'Welcome, *{st.session_state["name"]}*!')
    st.switch_page("Home.py")
    #authenticator.logout()
    #currUser = st.session_state["username"]
    
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    
    
#       @Registration Widget
######################################
if not st.session_state["authentication_status"]:
    if st.button("Sign up"):
        try:
            (email_of_registered_user, username_of_registered_user, name_of_registered_user) = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    
st.page_link("pages/My Account.py", label="Reset Password?")