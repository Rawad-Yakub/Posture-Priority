import streamlit as st ##1.12.0 originally
import datetime
from datetime import date
import os
import streamlit_authenticator as stauth                                ##user auth. in YAML
import numpy as np
import matplotlib.pyplot as plt           ##new
import plotly.express as px                                             
import pandas as pd
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
##from pymongo_get_database import get_database
import s3fs
from st_files_connection import FilesConnection

import yaml
from yaml.loader import SafeLoader
from dontcommit import my_config

from navigation import make_navbar, set_padding

st.set_page_config(
    page_title="Posture Priority",
    page_icon="🚶",
    layout="wide",
    initial_sidebar_state='auto'
)
make_navbar()
set_padding()
CURR_DATE = str(date.today())
 
username, password, s3_key, s3_secret, gpt_key = my_config() 

@st.cache_resource()
def init_connection():
    uri = "mongodb+srv://"+ username + ":" + password + "@capstonedbv1.wzzhaed.mongodb.net/?retryWrites=true&w=majority&appName=CapstoneDBv1"# Create a new client and connect to the server
    return uri

#def connect_database():
global fs, client, collection, db, authenticator, config
client = MongoClient(init_connection(), server_api=ServerApi('1')) 
db = client.test_database
collection = db['test_PP']
fs = s3fs.S3FileSystem(anon=False, key=s3_key, secret=s3_secret)        ##init s3 filesystem
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

##temp vars for class or similar
dailyPhotoUploadPrompt = True
def page_display():

    if st.session_state["authentication_status"]: #logged in
        ##authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*' + "\n Today is " + CURR_DATE)
        loggedIn = True
        currUser = st.session_state["username"]
    else: #not logged in
        st.subheader("Welcome to Posture Priority!")
        with st.container():  
            l_col, r_col = st.columns(2)
            with l_col: 
                st.markdown("""
                    We here at Posture Priority use machine learning and AI to 
                    help generate the best exercises talyored to you personally.
                    You can start today by signing up or loging in today!.
                """)
                st.page_link("pages/Login.py", label="Login\Signup in here", icon="💾")
            with r_col:
                st.image("images\home_page_slouch.webp")

# Main Streamlit app logic
if __name__ == "__main__":
    with open('styles\homepage.html','r') as f: 
        html_data = f.read()

    st.markdown(html_data, unsafe_allow_html=True)
    