import streamlit as st
import yaml
from yaml.loader import SafeLoader
import bcrypt

def get_auth_config():
    """Get authentication configuration from either config.yaml or streamlit secrets."""
    try:
        # First try to load from config.yaml (local development)
        with open('config.yaml', 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)
    except FileNotFoundError:
        # Fall back to streamlit secrets (cloud deployment)
        # Create config structure from secrets
        config = {
            'cookie': {
                'expiry_days': 0,  # Matching your config.yaml
                'key': 'cE8wQm9KNh47Zt1x',  # Using your exact key
                'name': 'my_auth_cookie'  # Using your exact cookie name
            },
            'credentials': {
                'usernames': {
                    'faisalawan': {  # Using your existing username
                        'email': 'faisal@example.com',
                        'failed_login_attempts': 0,
                        'first_name': 'Faisal',
                        'last_name': 'Awan',
                        'logged_in': False,  # Reset to false on app start
                        'password': '$2b$12$0PREek4djv9e4J9DSME4hOZZYaV3Z4jDcDEVw4qcnME15VUVzG6RC',  # Your hashed password
                        'roles': ['admin']
                    }
                }
            },
            'preauthorized': {'emails': []}
        }
        
        # If credentials are in streamlit secrets, override with those
        if 'credentials' in st.secrets:
            config = {
                'cookie': st.secrets.get('cookie', config['cookie']),
                'credentials': st.secrets['credentials'],
                'preauthorized': st.secrets.get('preauthorized', {'emails': []})
            }
    
    return config