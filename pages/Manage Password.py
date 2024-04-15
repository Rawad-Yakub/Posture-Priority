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
from dontcommit import gmail_conf
import smtplib


##################################################
st.set_page_config(
    page_title="Reset Password",
    page_icon="🚶",
    layout="centered",
    initial_sidebar_state='auto'
)
##################################################

#hashed_passwords = Hasher(['abc', 'def']).generate()
PPemail, PPpassword = gmail_conf()

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = PPemail
smtp_password = PPpassword

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.subheader("Reset Password")
st.page_link("Home.py", label="Home", icon="🏠")
    
#       @Password Reset Widget

try: 
    (username_of_forgotten_password, email_of_forgotten_password, new_random_password) = authenticator.forgot_password()
    if username_of_forgotten_password:
        st.success('New password sent securely')
        to_email = email_of_forgotten_password
        subject = 'Posture Priority Password Reset'
        body = 'Your new password is: ' + new_random_password
        message = f'Subject: {subject}\n\n{body}'

        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(smtp_username, to_email, message)
    elif not username_of_forgotten_password:
        st.error('Username not found')
except Exception as e:
    st.error(e)
    
    
if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)
        except Exception as e:
            st.error(e)
            
            


    