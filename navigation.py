
import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from components import navbar

#script that returns curret page name 
#formats it as Home.py or /pages/'page name'
def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
      raise RuntimeError("Couldn't get script context")
    page = get_pages("")[ctx.page_script_hash]["page_name"]
    if page == "Home": #home has a different directory
      return page + ".py"
    else:
      return "pages\\" + page + ".py"
    return 

def set_padding():
      st.markdown("""
        <style>
               .block-container {
                    padding-top: 3rem;
                    padding-bottom: 0rem;
                    padding-left: 10rem;
                    padding-right: 10rem;
                }
        </style>
        """, unsafe_allow_html=True)

def make_navbar():
    #makes the padding on screen smaller


    logo_text = "<i>Posture</i> <strong>Priority</strong>"
    #shows Login intead of My Account if not logged in
    if st.session_state["authentication_status"]:
      nav_links = {#dict with page name displayed and page path
          "Home":"Home.py",
          "Generate Exercises": "pages/model.py",
          "Calendar": "pages/calendar.py",
          "My Account": "pages/My Account.py",
      }
    else: 
      nav_links = {
          "Home":"Home.py",
          "Generate Exercises": "pages/model.py",
          "Calendar": "pages/calendar.py",
          "Login/Sign up": "pages/Login.py",
      }
    #when the page button is pressed, navbar returns page path
    selected_page = navbar(logo=logo_text, nav_links=nav_links, body_color= "black")
    #switches pages if it differs from current page
    if selected_page != None and selected_page != get_current_page_name():
      st.switch_page(selected_page)
    #if st.session_state["authentication_status"]:
    
           # logout(