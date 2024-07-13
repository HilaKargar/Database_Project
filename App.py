import streamlit as st
import requests

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Login", "Sign Up", "Places", "Bus stops", "Favorites"])

FLASK_API_URL = "http://localhost:5000"

if page == "Login":
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(FLASK_API_URL + "/login", json={"user": username, "password": password})
        if res.status_code == 201:
            st.success("Successfully logged in")
        else:
            st.error("Login failed")

elif page == "Sign Up":
    st.title("Sign up page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        res = requests.post(FLASK_API_URL + "/signup", json={"user": username, "password": password})
        if res.status_code == 201:
            st.success("Successfully signed up")
        else:
            st.error("Sign up failed")

elif page == "Places":
    st.title("Places")
    category = st.selectbox("Category", ["All", "Catering", "Commercial", "Accommodation", "Entertainment"])
    if st.button("Get Places"):
        res = requests.get(FLASK_API_URL + "/places", json={"category": category})
        if res.status_code == 200:
            places = res.json()
            st.write("Response from server:")
            st.json(places)  # Print out the JSON response for debugging
            for place in places:
                st.write(f"Name: {place['name']}, Type: {place['type']}, Street: {place['street']}")
        else:
            st.error("Failed to fetch places")

# Note: Ensure the Streamlit script is running in a separate terminal or process from your Flask app.