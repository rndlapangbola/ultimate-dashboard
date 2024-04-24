import streamlit as st

def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/1_Home.py", label="Home")
    st.sidebar.page_link("pages/2_Season_Statistics.py", label="Statistics")
    st.sidebar.page_link("pages/3_Log_Out.py", label="Log Out")

def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.switch_page("app.py")

def home_menu():
    # Show a navigation menu for unauthenticated users
    st.switch_page("pages/1_Home.py")

def menu():
    return authenticated_menu()

def out_menu():
    return unauthenticated_menu()
