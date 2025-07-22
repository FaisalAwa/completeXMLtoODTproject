# import streamlit as st
# from streamlit_lottie import st_lottie
# import requests
# import streamlit_authenticator as stauth
# import yaml
# from yaml.loader import SafeLoader
# from app import main as app_main
# import bcrypt

# # Set wide layout
# st.set_page_config(page_title="ODT to XML Processor", layout="wide")

# # --- LOTTIE ANIMATION LOADER ---
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# # Lottie animation URLs (you can change these to any Lottie you like)
# LOTTIE_LOGIN = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  # Modern login animation
# LOTTIE_USER = "https://assets2.lottiefiles.com/packages/lf20_ktwnwv5m.json"   # User creation animation

# # --- CONFIG and AUTHENTICATOR SETUP ---
# with open('config.yaml', 'r') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days']
# )

# # --- PAGE STATE MANAGEMENT ---
# if 'page' not in st.session_state:
#     st.session_state.page = 'login'

# def go_to_create_user():
#     st.session_state.page = 'create_user'

# def go_to_login():
#     st.session_state.page = 'login'

# # --- BEAUTIFUL LOGIN FORM ---
# def login_form():
#     st.markdown("""
#         <style>
#         .main-login-card {
#             background: #f8fafc;
#             border-radius: 18px;
#             box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
#             padding: 2.5rem 2rem 2rem 2rem;
#             max-width: 600px;
#             margin: 2rem auto 1rem auto;
#         }
#         .stButton>button {
#             background: linear-gradient(90deg, #4f8cff 0%, #235390 100%);
#             color: white;
#             border-radius: 8px;
#             font-weight: 600;
#             padding: 0.5rem 2rem;
#         }
#         .stTextInput>div>div>input {
#             background: #f1f5f9;
#             border-radius: 8px;
#         }
#         </style>
#     """, unsafe_allow_html=True)
    
#     with st.container():
#         st_lottie(load_lottieurl(LOTTIE_LOGIN), height=180, key="login-lottie")
#         st.markdown('<div class="main-login-card">', unsafe_allow_html=True)
#         st.header("Login")
#         authenticator.login()
#         st.markdown('</div>', unsafe_allow_html=True)
#         if st.session_state.get("authentication_status") is False:
#             st.error('Username/password is incorrect')
#         elif st.session_state.get("authentication_status") is None:
#             st.warning('Please enter your username and password')
#         st.button("Add New User", on_click=go_to_create_user)

# # --- BEAUTIFUL USER CREATION FORM ---
# def create_user_page():
#     st.markdown("""
#         <style>
#         .main-user-card {
#             background: #f8fafc;
#             border-radius: 18px;
#             box-shadow: 0 4px 24px 0 rgba(0,0,0,0.07);
#             padding: 2.5rem 2rem 2rem 2rem;
#             max-width: 650px;
#             margin: 2rem auto 1rem auto;
#         }
#         .stButton>button {
#             background: linear-gradient(90deg, #4f8cff 0%, #235390 100%);
#             color: white;
#             border-radius: 8px;
#             font-weight: 600;
#             padding: 0.5rem 2rem;
#         }
#         .stTextInput>div>div>input {
#             background: #f1f5f9;
#             border-radius: 8px;
#         }
#         </style>
#     """, unsafe_allow_html=True)
#     st_lottie(load_lottieurl(LOTTIE_USER), height=180, key="user-lottie")
#     st.markdown('<div class="main-user-card">', unsafe_allow_html=True)
#     st.header("Create New User")
#     st.write("This action requires admin privileges.")
#     with st.form("new_user_form", clear_on_submit=False):
#         st.markdown("##### Admin Credentials")
#         admin_username_input = st.text_input("Your Admin Username").strip()
#         admin_password_input = st.text_input("Your Admin Password", type="password")
#         st.markdown("---")
#         st.markdown("##### New User Details")
#         new_username = st.text_input("New Username").strip()
#         new_first_name = st.text_input("First Name").strip()
#         new_last_name = st.text_input("Last Name").strip()
#         new_email = st.text_input("Email").strip()
#         new_password = st.text_input("New Password", type="password")
#         submitted = st.form_submit_button("Create User")
#         if submitted:
#             is_admin_valid = False
#             # Case-insensitive admin user lookup
#             found_admin_key = None
#             for key in config['credentials']['usernames']:
#                 if key.lower() == admin_username_input.lower():
#                     found_admin_key = key
#                     break
#             admin_data = config['credentials']['usernames'].get(found_admin_key)
#             if admin_data:
#                 if 'admin' in admin_data.get('roles', []):
#                     hashed_pw_from_config = admin_data['password']
#                     if bcrypt.checkpw(admin_password_input.encode(), hashed_pw_from_config.encode()):
#                         is_admin_valid = True
#                     else:
#                         st.error("Incorrect admin password.")
#                 else:
#                     st.error(f"User '{admin_username_input}' does not have admin privileges.")
#             else:
#                 st.error(f"Admin user '{admin_username_input}' not found.")
#             if is_admin_valid:
#                 if new_username and new_password and new_email:
#                     if new_username in config['credentials']['usernames']:
#                         st.error(f"Username '{new_username}' already exists.")
#                     else:
#                         temp_creds = {'usernames': {new_username: {'password': new_password}}}
#                         hashed_creds = stauth.Hasher.hash_passwords(temp_creds)
#                         hashed_password = hashed_creds['usernames'][new_username]['password']
#                         config["credentials"]["usernames"][new_username] = {
#                             "email": new_email, "failed_login_attempts": 0,
#                             "first_name": new_first_name, "last_name": new_last_name,
#                             "logged_in": False, "password": hashed_password,
#                             "roles": ["viewer"]
#                         }
#                         with open('config.yaml', 'w') as file:
#                             yaml.dump(config, file, default_flow_style=False)
#                         st.success(f"User '{new_username}' created successfully!")
#                         st.info("Click 'Back to Login' to continue.")
#                 else:
#                     st.error("Please fill out all fields for the new user.")
#     st.markdown('</div>', unsafe_allow_html=True)
#     st.button("Back to Login", on_click=go_to_login)

# # --- PAGE ROUTING ---
# if st.session_state.get('authentication_status'):
#     authenticator.logout()
#     st.write(f'Welcome *{st.session_state["name"]}*')
#     app_main()
# else:
#     if st.session_state.page == 'login':
#         login_form()
#     elif st.session_state.page == 'create_user':
#         create_user_page()






import streamlit as st
from streamlit_lottie import st_lottie
import requests
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from app import main as app_main
import bcrypt

# Set wide layout
st.set_page_config(page_title="ODT to XML Processor", layout="wide")

# --- LOTTIE ANIMATION LOADER ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animation URLs (you can change these to any Lottie you like)
LOTTIE_LOGIN = "https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json"  # Modern login animation
LOTTIE_USER = "https://assets2.lottiefiles.com/packages/lf20_ktwnwv5m.json"   # User creation animation

# --- CONFIG and AUTHENTICATOR SETUP ---
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- PAGE STATE MANAGEMENT ---
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def go_to_create_user():
    st.session_state.page = 'create_user'

def go_to_login():
    st.session_state.page = 'login'

# --- BEAUTIFUL LOGIN FORM ---
def login_form():
    st.markdown("""
        <style>
        .main-login-card {
            background: linear-gradient(145deg, #ffffff, #f5f7fa);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            padding: 2.5rem 2.5rem;
            max-width: 550px;
            margin: 2rem auto 1.5rem auto;
            border: 1px solid rgba(200, 200, 200, 0.2);
        }
        .stButton>button {
            background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
            color: white;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 2.5rem;
            width: 100%;
            border: none;
            margin-top: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(71, 118, 230, 0.3);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 14px rgba(71, 118, 230, 0.4);
        }
        .stTextInput>div>div>input {
            background: #f8fafc;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            padding: 10px 15px;
            font-size: 16px;
            transition: all 0.2s;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        }
        .stTextInput>div>div>input:focus {
            border-color: #4776E6;
            box-shadow: 0 0 0 3px rgba(71, 118, 230, 0.2);
        }
        .login-header {
            color: #2d3748;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .login-instructions {
            color: #718096;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st_lottie(load_lottieurl(LOTTIE_LOGIN), height=180, key="login-lottie")
        st.markdown('<div class="main-login-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-header">Welcome Back</h2>', unsafe_allow_html=True)
        st.markdown('<p class="login-instructions">Please sign in to continue</p>', unsafe_allow_html=True)
        authenticator.login()
        st.markdown('</div>', unsafe_allow_html=True)
        if st.session_state.get("authentication_status") is False:
            st.error('Username/password is incorrect')
        elif st.session_state.get("authentication_status") is None:
            st.warning('Please enter your username and password')
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.button("Add New User", on_click=go_to_create_user)

# --- BEAUTIFUL USER CREATION FORM ---
def create_user_page():
    st.markdown("""
        <style>
        .main-user-card {
            background: linear-gradient(145deg, #ffffff, #f5f7fa);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            padding: 2.5rem 2.5rem;
            max-width: 650px;
            margin: 2rem auto 1.5rem auto;
            border: 1px solid rgba(200, 200, 200, 0.2);
        }
        .stButton>button {
            background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
            color: white;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 2.5rem;
            width: 100%;
            border: none;
            margin-top: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(71, 118, 230, 0.3);
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 14px rgba(71, 118, 230, 0.4);
        }
        .stTextInput>div>div>input {
            background: #f8fafc;
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            padding: 10px 15px;
            font-size: 16px;
            transition: all 0.2s;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        }
        .stTextInput>div>div>input:focus {
            border-color: #4776E6;
            box-shadow: 0 0 0 3px rgba(71, 118, 230, 0.2);
        }
        .user-create-header {
            color: #2d3748;
            font-weight: 700;
            margin-bottom: 1rem;
            text-align: center;
        }
        .section-divider {
            margin: 1.5rem 0;
            border-top: 1px solid #e2e8f0;
        }
        .section-header {
            color: #4776E6;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .stForm > div {
            background-color: transparent !important;
            border: none !important;
        }
        .form-submit-btn {
            margin-top: 1.5rem;
        }
        .form-instructions {
            color: #718096;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st_lottie(load_lottieurl(LOTTIE_USER), height=180, key="user-lottie")
    st.markdown('<div class="main-user-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="user-create-header">Create New User</h2>', unsafe_allow_html=True)
    st.markdown('<p class="form-instructions">This action requires admin privileges.</p>', unsafe_allow_html=True)
    
    with st.form("new_user_form", clear_on_submit=False):
        st.markdown('<h4 class="section-header">Admin Credentials</h4>', unsafe_allow_html=True)
        admin_username_input = st.text_input("Your Admin Username").strip()
        admin_password_input = st.text_input("Your Admin Password", type="password")
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<h4 class="section-header">New User Details</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            new_username = st.text_input("Username").strip()
            new_first_name = st.text_input("First Name").strip()
        with col2:
            new_email = st.text_input("Email").strip()
            new_last_name = st.text_input("Last Name").strip()
            
        new_password = st.text_input("Password", type="password")
        
        st.markdown('<div class="form-submit-btn">', unsafe_allow_html=True)
        submitted = st.form_submit_button("Create User")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted:
            is_admin_valid = False
            # Case-insensitive admin user lookup
            found_admin_key = None
            for key in config['credentials']['usernames']:
                if key.lower() == admin_username_input.lower():
                    found_admin_key = key
                    break
            admin_data = config['credentials']['usernames'].get(found_admin_key)
            if admin_data:
                if 'admin' in admin_data.get('roles', []):
                    hashed_pw_from_config = admin_data['password']
                    if bcrypt.checkpw(admin_password_input.encode(), hashed_pw_from_config.encode()):
                        is_admin_valid = True
                    else:
                        st.error("Incorrect admin password.")
                else:
                    st.error(f"User '{admin_username_input}' does not have admin privileges.")
            else:
                st.error(f"Admin user '{admin_username_input}' not found.")
            if is_admin_valid:
                if new_username and new_password and new_email:
                    if new_username in config['credentials']['usernames']:
                        st.error(f"Username '{new_username}' already exists.")
                    else:
                        temp_creds = {'usernames': {new_username: {'password': new_password}}}
                        hashed_creds = stauth.Hasher.hash_passwords(temp_creds)
                        hashed_password = hashed_creds['usernames'][new_username]['password']
                        config["credentials"]["usernames"][new_username] = {
                            "email": new_email, "failed_login_attempts": 0,
                            "first_name": new_first_name, "last_name": new_last_name,
                            "logged_in": False, "password": hashed_password,
                            "roles": ["viewer"]
                        }
                        with open('config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                        st.success(f"User '{new_username}' created successfully!")
                        st.info("Click 'Back to Login' to continue.")
                else:
                    st.error("Please fill out all fields for the new user.")
            
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("Back to Login", on_click=go_to_login)

# --- PAGE ROUTING ---
if st.session_state.get('authentication_status'):
    authenticator.logout()
    st.write(f'Welcome *{st.session_state["name"]}*')
    app_main()
else:
    if st.session_state.page == 'login':
        login_form()
    elif st.session_state.page == 'create_user':
        create_user_page()
