##Some useful things for the future:
## st.write_stream for outputting text generated by OpenAI
##
##
import streamlit as st ##1.12.0 originally
import datetime
from datetime import date
import os

from streamlit_image_coordinates import streamlit_image_coordinates     ##manually select points for posture evaluation
#from streamlit_image_comparison import image_comparison                 ##compare two postures
#from streamlit_plotly_events import plotly_events                       ##interactively view data on graphs
import streamlit_authenticator as stauth                                ##user auth. in YAML

import numpy as np
import matplotlib.pyplot as plt           ##new
#from openai import OpenAI

import plotly.express as px                                             
import pandas as pd
from PIL import Image
import mediapipe as mp
import math as m
import cv2

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
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
make_navbar()
set_padding()
CURR_DATE = str(date.today())
 
username, password, s3_key, s3_secret = my_config() #commented ', GPT_key' out to test
#fs, client, collection, db, authenticator, config = None, None, None, None, None, None #variables for server connection

@st.cache_resource()
def init_connection():
    uri = "mongodb+srv://"+ username + ":" + password + "@capstonedbv1.wzzhaed.mongodb.net/?retryWrites=true&w=majority&appName=CapstoneDBv1"# Create a new client and connect to the server
    return uri

#def connect_database():
global fs, client, collection, db, authenticator, config
client = MongoClient(init_connection(), server_api=ServerApi('1')) 

# Send a ping to confirm a successful connection  
#try:
#    client.admin.command('ping', maxTimeMS=4000)
#    print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
#    print(e)
#    #st.write("Connection to database failed. Invalid credentials")

db = client.test_database
collection = db['test_PP']

fs = s3fs.S3FileSystem(anon=False, key=s3_key, secret=s3_secret)        ##init s3 filesystem
#openai.api_key = GPT_key                                                ##init openai
#GPT_Client = OpenAI(api_key=GPT_key)
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
#this is gonna be in cloud or db for end product v


##temp vars for class or similar
dailyPhotoUploadPrompt = True
def page_display():

    if st.session_state["authentication_status"]: #logged in
        ##authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*' + "\n Today is " + CURR_DATE)
        loggedIn = True
        currUser = st.session_state["username"]
        ##activeDates = fs.open("posturepriorityawsbucket/"+currUser, mode='rb').read()

        #Generate a response from ChatGPT using the question chat message
        #question = "What are some exercises or stretches to improve " + my_Posture + "?"
        #st.write(question)
        #response = GPT_Client.chat.completions.create(model = "gpt-3.5-turbo",
        #messages = [
        #    {"role": "user", "content": question}
        #],
        #max_tokens=100,
        #temperature=0.9,
        #frequency_penalty=0.5,
        #presence_penalty=0.5)

        #Extract the answer from the response
        #answer = response.choices[0].message.content

        # Print the returned output from the LLM model
        #st.write(str(answer))

        if dailyPhotoUploadPrompt:
            uploaded_file = st.file_uploader("Upload a photo for today(png or jpg file)", type=['png', 'jpg'])
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                st.image(bytes_data)

                s3 = s3fs.S3FileSystem(anon=False)                                              ##uses default credentials
                if st.button("Upload this photo?"):
                    with fs.open('posturepriorityawsbucket/'+currUser+'_'+CURR_DATE, 'wb') as f: ##insert photo to s3 cloud
                        f.write(bytes_data)

                    post = {
                        "username": currUser,
                        "photo": 'posturepriorityawsbucket/'+currUser+'_'+CURR_DATE,
                        "date": CURR_DATE
                    }
                    collection.insert_one(post) ##.inserted_id                                  ##insert post to db
                    dailyPhotoUploadPrompt = False

        st.header("Or, view an existing photo")
        
        ## jank
        d = str(st.date_input("Select a date"))
        st.write(d)
        photo_posted = collection.find_one({"username": currUser, "date": d,})

        if photo_posted:
            st.write("A photo was uploaded on this day")
            #temp = str(currUser + '_'+d)
            view_photo = fs.open("posturepriorityawsbucket/" + currUser + '_' + d, mode='rb').read()
            #st.image(temp)
            st.image(view_photo)
            ##streamlit_image_coordinates(fs.open("posturepriorityawsbucket/"+currUser+'_'+d, mode='rb'))

        else:
            st.write("No photo was uploaded on this day")
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
        

#st.image(fs.open("posturepriorityawsbucket/abc123.png", mode='rb').read())

#### MODEL I THINK ###
# Initialize MediaPipe modules


# Main Streamlit app logic
if __name__ == "__main__":
    ##st.page_link()
    # Page title and header
    with open('styles\homepage.html','r') as f: 
        html_data = f.read()

    st.markdown(html_data, unsafe_allow_html=True)
    #connect_database()
    # File upload section
    #uploaded_file = st.file_uploader("Upload a photo for (png or jpg file)", type=['png', 'jpg', 'heic', 'webp', 'avif'])
    