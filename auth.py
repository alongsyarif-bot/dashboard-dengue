# ==========================================================
# BILIK GERAKAN
# Authentication Module
# Government Surveillance System
# ==========================================================


import streamlit as st



# ==========================================================
# LOGIN PAGE STYLE
# ==========================================================


def login_style():

    st.markdown(

    """

    <style>


    /* ==============================
       PAGE BACKGROUND
    ===============================*/


    .stApp {

        background:#eef3f8;

    }




    /* ==============================
       REMOVE TOP SPACE
    ===============================*/


    .block-container {

        padding-top:3rem;

    }




    /* ==============================
       LOGIN CARD
    ===============================*/


    .login-box {


        background:white;


        padding:45px;


        border-radius:18px;


        box-shadow:

        0px 10px 35px rgba(0,0,0,0.12);



        border-top:

        6px solid #005b96;



        text-align:center;


    }





    /* ==============================
       TITLE
    ===============================*/


    .login-title {


        color:#003366;


        font-size:34px;


        font-weight:800;


        margin-bottom:10px;


    }





    .login-subtitle {


        color:#475569;


        font-size:15px;


        line-height:1.6;


    }





    .online-status {


        color:#00a651;


        font-weight:bold;


    }





    /* ==============================
       INPUT LABEL
    ===============================*/


    label {


        color:#334155 !important;


        font-weight:600 !important;


    }





    /* ==============================
       INPUT BOX
    ===============================*/


    input {


        background:white !important;


        color:#111827 !important;


        border:

        1px solid #cbd5e1 !important;



        border-radius:8px !important;


    }





    input:focus {


        border:

        2px solid #005b96 !important;


    }





    /* ==============================
       LOGIN BUTTON
    ===============================*/


    div.stButton > button {


        width:100%;


        height:45px;


        background:#005b96;


        color:white;


        border-radius:8px;


        border:none;


        font-size:16px;


        font-weight:bold;


    }





    div.stButton > button:hover {


        background:#003366;


        color:white;


    }





    /* ==============================
       ALERT
    ===============================*/


    .stAlert {


        border-radius:10px;

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
# LOGIN PAGE
# ==========================================================


def login_page():


    login_style()



    left,center,right = st.columns(

        [1,2,1]

    )



    with center:



        st.markdown(

        """

        <div class="login-box">


        <div class="login-title">

        🏥 BILIK GERAKAN

        </div>



        <div class="login-subtitle">


        <b>

        Epidemiological Surveillance System

        </b>


        <br>


        Government Monitoring Portal


        <br><br>


        <span class="online-status">

        🟢 System Online

        </span>


        </div>


        </div>


        """,

        unsafe_allow_html=True

        )



        st.write("")



        username = st.text_input(

            "Username",

            placeholder="Masukkan username"

        )



        password = st.text_input(

            "Password",

            type="password",

            placeholder="Masukkan password"

        )



        st.write("")



        login = st.button(

            "LOGIN"

        )




        if login:


            authenticate_user(

                username,

                password

            )





# ==========================================================
# USER AUTHENTICATION
# ==========================================================


def authenticate_user(

    username,

    password

):



    try:


        users = st.secrets["users"]


    except:


        st.error(

            "User database tidak dijumpai. Sila semak secrets.toml"

        )

        return





    if username in users:



        correct_password = users[username]



        if password == correct_password:




            st.session_state.authenticated=True



            st.session_state.username=username





            try:


                role = st.secrets["roles"][username]


            except:


                role="Viewer"





            st.session_state.role=role




            st.success(

                "Login berjaya"

            )



            st.rerun()



        else:



            st.error(

                "❌ Password salah"

            )




    else:



        st.error(

            "❌ Username tidak wujud"

        )





# ==========================================================
# LOGOUT
# ==========================================================


def logout():


    st.sidebar.markdown(

    "---"

    )



    st.sidebar.write(

        f"👤 {st.session_state.username}"

    )


    st.sidebar.write(

        f"Role: {st.session_state.role}"

    )



    if st.sidebar.button(

        "🚪 Logout"

    ):



        st.session_state.authenticated=False


        st.session_state.username=None


        st.session_state.role=None



        st.rerun()
