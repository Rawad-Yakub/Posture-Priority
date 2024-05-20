
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
from navigation import get_current_page_name, make_sidebar

import streamlit as st
from mycomponent import mycomponent


make_navbar()
def main():
    logo_text = "<i>Posture</i> <strong>Priority</strong>"
    nav_links = {
        "Home":"Home.py",
        "test":"test.py",
        "Generate Exercises": "pages/model.py",
        "Calendar": "pages/calendar.py",
        "My Account": "pages/model.py",
    }   
    selected_value = mycomponent(logo=logo_text, nav_links=nav_links)
# Call the component, passing the logo text and nav links
    
    if get_current_page_name() != selected_value:
        st.write("wrong")
# Display the value returned by the component
    st.write("You pressed a button with value:", selected_value)
    st.write(get_current_page_name())

if __name__ == "__main__":
    main()