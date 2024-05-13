import streamlit as st ##1.12.0 originally
import streamlit_authenticator as stauth                                ##user auth. in YAML
from streamlit_authenticator.utilities.hasher import Hasher
import s3fs
from st_files_connection import FilesConnection
import yaml
from yaml.loader import SafeLoader
from dontcommit import my_config

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

#       @Registration Widget
######################################
try:
    (email_of_registered_user, username_of_registered_user, name_of_registered_user) = authenticator.register_user(pre_authorization=False)
    if email_of_registered_user:
        #config['credentials']['usernames'][username_of_registered_user] = {
        #    'email': email_of_registered_user,
        #    'logged_in': False,                                             # Assuming new users are not logged in by default
        #    'name': name_of_registered_user,
        #    }
        st.success('User registered successfully')
        print("Registration")
        with fs.open('posturepriorityawsbucket/config.yaml', 'w') as file:
            print("Writing...")
            #WriteConfig.write(config)
            yaml.dump(config, file, default_flow_style=False)
            print("Written")
            st.switch_page("pages/Login.py")
                    
except Exception as e:
            st.error(e)