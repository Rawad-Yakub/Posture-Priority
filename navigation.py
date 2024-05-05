
import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


logged_in= True

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
    st.markdown("""
         <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Website with Banner and Nav Bar</title>
          <style>
            /* CSS styles for the navigation bar */
            .navbar {
              background-color: black; /* Background color */
              color: white; /* Text color */
              overflow: hidden; /* Ensure elements inside the navbar stay within it */
              border-bottom: 2px solid white; /* Bold border at the bottom */
              border-top-left-radius: 20px; /* Rounded top-left corner */
              border-top-right-radius: 20px; /* Rounded top-right corner */
              display: flex; /* Use flexbox */
              justify-content: left; /* Align items on each end */
              align-items: center; /* Center items vertically */
              padding: 10px 20px; /* Padding */
        
            }

            /* Logo styles */
            .logo {
              color: white; /* Text color */
              font-size: 24px; /* Font size */
              border = 2px solid white;
              padding: 10px 20px;
            }

            /* Links inside the navbar */
            .navbar a {
              color: white; /* Text color */
              text-decoration: none; /* Remove underline from links */
              padding: 10px 20px; /* Padding */
            }

            /* Change color on hover */
            .navbar a:hover {
              background-color: #ddd; /* Background color on hover */
              color: black; /* Text color on hover */
            }
          </style>
        </head>
        <body>

      

        <!-- Navigation bar -->
        <div class="navbar">
          <div class="logo"><i>Posture</i> <strong>Priority</strong></div>
          <a href="Home" target="_self">Home</a>
          <a href="model" target="_self">Generate Exercises</a>
          <a href= "calendar" target="_self">Calendar</a>
          <a href="Login" target="_self">My Account</a>
        </div>

        </html>""", unsafe_allow_html=True)
    #st.sidebar.markdown("")
    #with st.sidebar:
       # st.title("Welcome to Posture Priority")
        #st.page_link("Home.py", label="Home")
        #st.page_link("pages/Login.py", label="Login/Sign up")
        #st.page_link("pages/model.py", label="Generate Exercises")    
        #if st.session_state["authentication_status"]: 
           
        #st.button("Log out")
               # logout()

#def logout():