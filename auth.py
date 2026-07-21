import streamlit as st


def check_login():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    return st.session_state.authenticated



def login_page():


    st.markdown(
    """
    <style>

    .stApp {
        background:#f1f5f9;
    }


    .login-box {

        background:white;

        padding:40px;

        border-radius:15px;

        box-shadow:
        0 5px 20px rgba(0,0,0,.15);

        max-width:450px;

        margin:auto;

    }


    </style>
    """,
    unsafe_allow_html=True
    )



    st.markdown(
    """

    <div class="login-box">

    <h1 style="text-align:center;color:#003366">

    🏥 BILIK GERAKAN

    </h1>


    <p style="text-align:center">

    Epidemiological Surveillance System

    </p>


    </div>

    """,
    unsafe_allow_html=True
    )


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("LOGIN"):


        users = st.secrets["users"]


        if username in users:


            if password == users[username]:


                st.session_state.authenticated=True

                st.session_state.username=username


                st.session_state.role=(

                    st.secrets["roles"]

                    .get(

                    username,

                    "Viewer"

                    )

                )


                st.success(
                    "Login berjaya"
                )


                st.rerun()


            else:

                st.error(
                    "Password salah"
                )


        else:

            st.error(
                "User tidak wujud"
            )





def logout():


    if st.button("🚪 Logout"):


        st.session_state.authenticated=False

        st.session_state.username=None

        st.session_state.role=None


        st.rerun()
