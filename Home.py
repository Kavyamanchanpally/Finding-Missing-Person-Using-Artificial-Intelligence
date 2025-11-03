import yaml
import base64
import streamlit as st
from yaml import SafeLoader
import streamlit_authenticator as stauth
from pages.helper import db_queries


# ✅ Background image setup
def add_bg_from_local(image_file):
    with open(image_file, "rb") as img:
        encoded_string = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ✅ Initialize session state
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None
if "user" not in st.session_state:
    st.session_state["user"] = None


# ✅ Load YAML config properly
with open(r"login_config.yml") as file:
    config = yaml.load(file, Loader=SafeLoader)


# ✅ Setup authenticator
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)


# ✅ Login page
authenticator.login(location="main")

if st.session_state["authentication_status"]:
    authenticator.logout("Logout", "sidebar")

    username = st.session_state["username"]
    user_info = config["credentials"]["usernames"][username]
    st.session_state["user"] = user_info["name"]

    st.markdown(f"### Welcome, {user_info['name']} 👋")

    # Optional extra info (if exists in YAML)
    st.write(f"**Email:** {user_info.get('email', 'N/A')}")
    st.write(f"**Role:** {user_info.get('role', 'N/A')}")
    st.write("---")

    found_cases = db_queries.get_registered_cases_count(user_info["name"], "F")
    not_found_cases = db_queries.get_registered_cases_count(user_info["name"], "NF")

    col1, col2 = st.columns(2)
    col1.metric("Found Cases", len(found_cases))
    col2.metric("Not Found Cases", len(not_found_cases))

elif st.session_state["authentication_status"] == False:
    st.error("Incorrect username or password ❌")

else:
    st.warning("Please enter your username and password")
