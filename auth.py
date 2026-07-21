import streamlit as st


def check_login():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    return st.session_state.authenticated



def login_style():

    st.markdown(
    """

    <style>


    /* Background */

    .stApp {

        background:#eef3f8;

    }



    /* Login container */


    .login-box {


        background:white;


        padding:45px;


        border-radius:18px;


        box-shadow:

        0 8px 30px rgba(0,0,0,0.12);


        max-width:480px;


        margin:auto;


        border-top:

        6px solid #005b96;


    }




    /* Title */


    .login-title {


        color:#003366;


        text-align:center;


        font-size:34px;


        font-weight:800;


        margin-bottom:10px;


    }




    .login-subtitle {


        color:#475569;


        text-align:center;


        font-size:15px;


        line-height:1.5;


    }





    /* Streamlit labels */


    label {


        color:#334155 !important;


        font-weight:600 !important;


    }





    /* Input boxes */


    input {


        background:white !important;


        color:#111827 !important;


        border:1px solid #cbd5e1 !important;


        border-radius:8px !important;


    }






    /* Login button */


    div.stButton > button {


        width:100%;


        height:45px;


        background:#005b96;


        color:white;


        border-radius:8px;


        border:none;


        font-weight:bold;


        font-size:16px;


    }




    div.stButton > button:hover {


        background:#003366;


        color:white;


    }





    </style>


    """,

    unsafe_allow_html=True

    )



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

<span style="color:#00a651">

🟢 System Online

</span>


</div>


</div>

""",

unsafe_allow_html=True

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
