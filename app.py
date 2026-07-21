# ==========================================================
# BILIK GERAKAN
# Authentication Module
# ==========================================================


import streamlit as st
import hashlib



# ==========================================================
# PASSWORD HASH FUNCTION
# ==========================================================


def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()



# ==========================================================
# LOGIN PAGE CSS
# ==========================================================


def login_style():


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

        0px 5px 20px rgba(0,0,0,0.15);


        max-width:450px;


        margin:auto;


    }




    .login-title {


        color:#003366;


        text-align:center;


        font-size:32px;


        font-weight:bold;


    }



    .login-subtitle {


        color:#64748b;


        text-align:center;


    }



    div.stButton > button {


        width:100%;


        background:#005b96;


        color:white;


        height:45px;


        border-radius:8px;


        font-weight:bold;


    }



    div.stButton > button:hover {


        background:#003366;


        color:white;


    }


    </style>


    """,

    unsafe_allow_html=True

    )





# ==========================================================
# CHECK LOGIN STATUS
# ==========================================================



def check_login():


    if "authenticated" not in st.session_state:


        st.session_state.authenticated=False



    return st.session_state.authenticated





# ==========================================================
# LOGIN FUNCTION
# ==========================================================



def login_page():



    login_style()



    st.markdown(

    """

    <div class="login-box">


    <div class="login-title">

    🏥 BILIK GERAKAN

    </div>



    <div class="login-subtitle">

    Epidemiological Surveillance System

    <br>

    Government Monitoring Portal

    </div>


    </div>


    """,

    unsafe_allow_html=True

    )



    st.write("")



    username=st.text_input(

        "Username"

    )


    password=st.text_input(

        "Password",

        type="password"

    )



    login=st.button(

        "LOGIN"

    )




    if login:



        users=st.secrets["users"]



        if username in users:


            stored_password=users[username]


            if password == stored_password:



                st.session_state.authenticated=True


                st.session_state.username=username



                if "roles" in st.secrets:


                    st.session_state.role=(

                        st.secrets["roles"]

                        .get(

                        username,

                        "Viewer"

                        )

                    )


                else:

                    st.session_state.role="Viewer"



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

                "User tidak dijumpai"

            )





# ==========================================================
# LOGOUT
# ==========================================================


def logout():


    if st.button(

        "🚪 Logout"

    ):


        st.session_state.authenticated=False


        st.session_state.username=None


        st.session_state.role=None


        st.rerun()
