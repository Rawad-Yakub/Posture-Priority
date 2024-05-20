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
    page_title="Reset Password",
    page_icon="🚶",
    layout="wide",
    initial_sidebar_state='auto'
)
make_navbar()
set_padding()
##################################################
username, password, s3_key, s3_secret, GPT_key = my_config()
fs = s3fs.S3FileSystem(anon=False, key=s3_key, secret=s3_secret)        ##init s3 filesystem

with fs.open('posturepriorityawsbucket/config.yaml', 'rb') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.title("My Account")

#Password Modify Widget
if st.session_state["authentication_status"]:
    st.header(st.session_state["username"])
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)
    authenticator.logout()
    st.switch_page("pages/Home.py")
else:
    st.header("You're not logged in!")
    st.page_link("pages/Login.py", label="Log in, sign up, or...", icon="💾")
    
st.page_link("pages/Home.py", label="Return to Home!", icon="🏠")
