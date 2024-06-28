import streamlit as st

# Reading credentials from secrets.toml
credentials = st.secrets["credentials"]


def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        login()
    else:
        # Redirect to Home page
        st.query_params.update(page="Home")
        st.rerun()


def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == credentials["username"] and password == credentials["password"]:
            st.session_state.authenticated = True
            st.success("Login successful!")
            # Redirect to Home page
            st.query_params.update(page="Home")
            st.rerun()
        else:
            st.error("Invalid username or password")


if __name__ == "__main__":
    main()
