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
    page_title="Reset Password",
    page_icon="🚶",
    layout="wide",
    initial_sidebar_state='auto'
)
make_sidebar()
##################################################

#hashed_passwords = Hasher(['abc', 'def']).generate()

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.page_link("Home.py", label="Home", icon="🏠")
    
#       @Password Modify Widget
if st.session_state["authentication_status"]:
    st.title(st.session_state["username"])
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)
