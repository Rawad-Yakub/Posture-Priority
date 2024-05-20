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
from dontcommit import my_config
from navigation import make_navbar, set_padding
##################################################
st.set_page_config(
    page_title="Login",
    page_icon="🚶",
    layout="wide",
    initial_sidebar_state='auto'
)
make_navbar()
set_padding()
#local_css("signup_style.css")  # Update file name here
hashed_passwords = Hasher(['abc', 'def']).generate()

username, password, s3_key, s3_secret, GPT_key = my_config()
fs = s3fs.S3FileSystem(anon=False, key=s3_key, secret=s3_secret)        ##init s3 filesystem

with fs.open('posturepriorityawsbucket/'+"config.yaml", 'rb') as file:
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
st.page_link("pages/Home.py", label="Home", icon="🏠")
    
name, authentication_status, username = authenticator.login()

if st.session_state["authentication_status"]:
    st.write(f'Welcome, *{st.session_state["name"]}*!')
    st.switch_page("pages/Home.py")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
  

st.page_link("pages/My Account.py", label="Reset Password?")
st.page_link("pages/Registration.py", label="Register an Account")