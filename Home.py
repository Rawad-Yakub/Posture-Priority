##Some useful things for the future:
## st.write_stream for outputting text generated by OpenAI
import streamlit as st ##1.12.0 originally
import datetime
from datetime import date
import os
from streamlit_calendar import calendar
#from streamlit_image_coordinates import streamlit_image_coordinates     ##manually select points for posture evaluation
#from streamlit_image_comparison import image_comparison                 ##compare two postures
#from streamlit_plotly_events import plotly_events                       ##interactively view data on graphs
import streamlit_authenticator as stauth                                ##user auth. in YAML
import numpy as np
import matplotlib.pyplot as plt           ##new
from openai import OpenAI
import plotly.express as px                                             
import pandas as pd
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import s3fs
from st_files_connection import FilesConnection
import yaml
from yaml.loader import SafeLoader
from dontcommit import my_config
from Utilities import process_image, draw_landmarks, extract_landmark_coordinates, visualize_landmark_coordinates, findAngle, EvalImage

st.set_page_config(
    page_title="Posture Priority",
    page_icon="🚶",
    layout="centered",
    initial_sidebar_state='auto'
)
CURR_DATE = str(date.today())
st.title('Posture Priority')
st.subheader("Today is " + CURR_DATE[6:])
################################################################################################
username, password, s3_key, s3_secret, GPT_key = my_config()

@st.cache_resource()
def init_connection():
    uri = "mongodb+srv://"+ username + ":" + password + "@capstonedbv1.wzzhaed.mongodb.net/?retryWrites=true&w=majority&appName=CapstoneDBv1"# Create new client and connect to the server
    return uri

client = MongoClient(init_connection(), server_api=ServerApi('1')) 
 
try: # Send a ping to confirm a successful connection 
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    st.write("Connection to database failed. Invalid credentials")

db = client.test_database
collection = db['test_PP']
fs = s3fs.S3FileSystem(anon=False, key=s3_key, secret=s3_secret)        ##init s3 filesystem
GPT_Client = OpenAI(api_key=GPT_key)
##################################################
#this is gonna be in cloud or db for end product 
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if st.session_state["authentication_status"]:
    st.write(f'Welcome, *{st.session_state["name"]}*!')
    currUser = st.session_state["username"]
    st.page_link("pages/My Account.py", label="Manage Account", icon="🏠")
    
    uploaded_file = st.file_uploader("Upload a photo?")
    if uploaded_file is not None:
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        s3 = s3fs.S3FileSystem(anon=False)                                 ##uses default credentials
        if st.session_state["authentication_status"]:
            if st.button("Upload this photo?"):
                with fs.open('posturepriorityawsbucket/'+currUser+'_'+CURR_DATE, 'wb') as f: ##insert photo to s3 cloud
                    f.write(image)

                    post = {
                        "username": currUser,
                        "photo": 'posturepriorityawsbucket/'+currUser+'_'+CURR_DATE,
                        "date": CURR_DATE
                    }
                    collection.insert_one(post) ##.inserted_id   
                    st.write("Photo uploaded")
                    print('posturepriorityawsbucket/'+currUser+'_'+CURR_DATE+" uploaded to database")
                    
        # Detect landmarks and draw on the image
        EvalImage(image)
        
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

    #st.write(str(answer))

###############################################################################
    st.subheader("Or, view an existing photo")
    ##Find photos for month    
    d = str(st.date_input("Select a date"))
    st.write("Viewing: " + d)
    
    #Checking uploaded days
    uploaded_days_list = ""
    CurrYearmonth = d[:8] # YYYY-MM-"0D"
    CurrDay = 1           #  D,       ^
    ZeroConst = str("0")  #  0,      ^
    while CurrDay < 10:
        PrevPosted = collection.find_one({"username": currUser, "date": CurrYearmonth+ZeroConst+str(CurrDay)})
        if PrevPosted:
            uploaded_days_list =  uploaded_days_list+ str(CurrDay) + ", "
        CurrDay += 1
    
    while CurrDay < 32:
        PrevPosted = collection.find_one({"username": currUser, "date": CurrYearmonth+str(CurrDay)})
        if PrevPosted:
            uploaded_days_list = uploaded_days_list + str(CurrDay) + ", "
        CurrDay += 1
    
    if uploaded_days_list == "":
        st.write("Nothing was uploaded this month")
    else:
        st.write("Dates uploaded for current month: " + uploaded_days_list)
      
    
    photo_posted = collection.find_one({"username": currUser, "date": d,})
    collection.find()

    if photo_posted:
        st.write("A photo was uploaded on this day")
        view_photo = fs.open("posturepriorityawsbucket/" + currUser + '_' + d, mode='rb').read()
        #st.image(view_photo)
        image = np.array(bytearray(view_photo), dtype=np.uint8)
        EvalImage(image)
    else:
        st.write("No photo was uploaded on this day")
else:
    st.header("Try below!")
    
    uploaded_file = st.file_uploader("Upload a photo?")
    if uploaded_file is not None:
        image = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)     
        EvalImage(image)
        
    st.page_link("pages/Login.py", label="Log in or sign up", icon="💾")
