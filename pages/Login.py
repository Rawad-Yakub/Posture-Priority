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
from navigation import make_navbar

##################################################
st.set_page_config(
    page_title="Login",
    page_icon="🚶",
    layout="centered",
    initial_sidebar_state='auto'
)

make_navbar()
# Define CSS styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#local_css("signup_style.css")  # Update file name here
hashed_passwords = Hasher(['abc', 'def']).generate()

username, password, s3_key, s3_secret = my_config() #removed GPT_Key
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
    
  
st.page_link("pages/My Account.py", label="Reset Password?")
st.page_link("pages/Registration.py", label="Register an Account")