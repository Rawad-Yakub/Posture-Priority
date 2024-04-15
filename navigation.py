
import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    st.sidebar.markdown("")
    with st.sidebar:
        st.title("Welcome to Posture Priority")
        st.page_link("Home.py", label="Home")
        st.page_link("pages/Login.py", label="Login/Sign up")
        st.page_link("pages/model.py", label="Generate Exercises")    
        #if st.session_state["authentication_status"]: 
           
        st.button("Log out")
               # logout()

#def logout():