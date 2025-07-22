"""
Main entry point for Streamlit deployment.
This file should be the one referenced when deploying to Streamlit Cloud.
"""
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from auth import login_form, create_user_page
from app import main as app_main

# Configure page
st.set_page_config(page_title="ODT to XML Processor", layout="wide")

# --- SESSION STATE SETUP ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- LOAD CONFIG ---
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

# --- AUTHENTICATOR SETUP ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- PAGE ROUTING ---
if st.session_state.get('authentication_status'):
    # User is authenticated
    # Place logout button in sidebar
    st.sidebar.write(f"Welcome, *{st.session_state['name']}*")
    if authenticator.logout('Logout', 'sidebar'):
        st.session_state['authentication_status'] = None
        st.session_state['name'] = None
        st.session_state['username'] = None
        st.experimental_rerun()
    
    # Run the main application
    app_main()
else:
    # User is not authenticated
    if st.session_state.page == 'login':
        login_form()
    elif st.session_state.page == 'create_user':
        create_user_page()