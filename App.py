import streamlit as st
import requests

FLASK_API_URL = "http://localhost:5000"

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "liked_places" not in st.session_state:
    st.session_state.liked_places = set()
if "places" not in st.session_state:
    st.session_state.places = []
if "bus_routes" not in st.session_state:
    st.session_state.bus_routes = []


def login(username, password):
    res = requests.post(FLASK_API_URL + "/login", json={"username": username, "password": password})
    if res.status_code == 200:
        data = res.json()
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.user_id = data.get("user_id")
        st.session_state.liked_places = set(data.get("liked_places", []))
        st.success("Successfully logged in")
        st.experimental_rerun()
    else:
        st.error("Login failed")


def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = ""
    st.session_state.liked_places.clear()
    st.session_state.places = []
    st.success("Successfully logged out")
    st.experimental_rerun()


def like_place(user_id, place_id):
    res = requests.post(FLASK_API_URL + "/like", json={"user_id": user_id, "place_id": place_id})
    if res.status_code == 201:
        st.session_state.liked_places.add(place_id)
    else:
        st.error("Failed to like place")


def unlike_place(user_id, place_id):
    res = requests.post(FLASK_API_URL + "/unlike", json={"user_id": user_id, "place_id": place_id})
    if res.status_code == 200:
        st.session_state.liked_places.remove(place_id)
    else:
        st.error("Failed to unlike place")


st.sidebar.title("Navigation")
if st.session_state.logged_in:
    if st.sidebar.button("Sign Out"):
        logout()
    st.sidebar.write(f"Logged in as {st.session_state.username}")
    page = st.sidebar.radio("Select Page", ["Places", "Bus stops", "Favorites"])
else:
    page = st.sidebar.radio("Select Page", ["Login", "Sign Up"])

if page == "Login":
    if not st.session_state.logged_in:
        st.title("Login Page")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                login(username, password)

elif page == "Sign Up":
    if not st.session_state.logged_in:
        st.title("Sign up page")
        with st.form("signup_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Register")
            if submitted:
                res = requests.post(FLASK_API_URL + "/signup", json={"username": username, "password": password})
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
            st.session_state.places = res.json()
        else:
            st.error("Failed to fetch places")

    for place in st.session_state.places:
        st.write(f"Name: {place['name']}")
        st.write(f"Address: {place['street']}")
        st.write(f"Category: {place['type']}")
        if st.session_state.logged_in:
            liked = place['id'] in st.session_state.liked_places
            with st.form(key=f"like_form_{place['id']}"):
                if liked:
                    if st.form_submit_button("Unlike"):
                        unlike_place(st.session_state.user_id, place['id'])
                        st.experimental_rerun()
                else:
                    if st.form_submit_button("Like"):
                        like_place(st.session_state.user_id, place['id'])
                        st.experimental_rerun()
        st.write("---")

elif page == "Favorites":
    if st.session_state.logged_in:
        st.title("Favorites")
        res = requests.get(FLASK_API_URL + "/favorites", json={"user_id": st.session_state.user_id})
        if res.status_code == 200:
            favorites = res.json()
            for place in favorites:
                st.write(f"Name: {place['name']}")
                st.write(f"Address: {place['street']}")
                st.write(f"Category: {place['type']}")
                with st.form(key=f"unlike_form_{place['id']}"):
                    if st.form_submit_button("Unlike"):
                        unlike_place(st.session_state.user_id, place['id'])
                        st.experimental_rerun()
                st.write("---")
        else:
            st.error("Failed to fetch favorites")

elif page == "Bus stops":
    st.title("Bus Routes")
    if st.button("Get Bus Routes"):
        res = requests.get(FLASK_API_URL + "/bus_routes")
        if res.status_code == 200:
            st.session_state.bus_routes = res.json()
        else:
            st.error("Failed to fetch bus routes")

    for route in st.session_state.bus_routes:
        st.write(f"Route ID: {route['Route_id']}")
        st.write(f"Trip Headsign: {route['Trip_headsign']}")
        st.write("---")

# Note: Ensure the Streamlit script is running in a separate terminal or process from your Flask app.