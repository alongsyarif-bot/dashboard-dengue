# ==========================================================
# BILIK GERAKAN
# Epidemiological Surveillance Dashboard
# Streamlit Version
# ==========================================================


import streamlit as st
import pandas as pd
import numpy as np

import re
from datetime import datetime


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="BILIK GERAKAN",
    page_icon="🏥",
    layout="wide"
)



# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""

<style>


/* MAIN BACKGROUND */

.stApp {

background-color:#4169e1;

}



/* REMOVE DEFAULT TOP SPACE */

.block-container {

padding-top:1rem;

}



/* HEADER */

.main-header {

background:white;

padding:25px;

border-radius:20px;

box-shadow:0px 5px 20px rgba(0,0,0,0.25);

text-align:center;

}



/* LIVE DOT */


.live-dot {

height:15px;

width:15px;

background:#00cc44;

border-radius:50%;

display:inline-block;

animation:pulse 1s infinite;

}


@keyframes pulse {

0% {

opacity:1;

}


50% {

opacity:0.2;

}


100% {

opacity:1;

}

}



/* KPI CARD */


.kpi-card {


background:white;

padding:20px;

border-radius:18px;

box-shadow:
0px 5px 15px rgba(0,0,0,0.25);

text-align:center;

height:120px;

}



.kpi-title {

font-size:16px;

color:#555;

}



.kpi-value {

font-size:32px;

font-weight:bold;

color:#4169e1;

}



/* SECTION CARD */


.section-card {

background:white;

padding:20px;

border-radius:18px;

box-shadow:
0px 5px 15px rgba(0,0,0,0.2);

}



/* BUTTON */


div.stButton > button {


background:#dc2626;

color:white;

border-radius:10px;

font-weight:bold;

width:100%;


}



</style>


""", unsafe_allow_html=True)



# ==========================================================
# HEADER
# ==========================================================


st.markdown(

"""

<div class="main-header">


<h1>
🏥 BILIK GERAKAN
</h1>


<h3>

<span class="live-dot"></span>

 LIVE

</h3>


<p>

Dibina oleh <b>[NAMA ANDA]</b>

</p>


</div>


""",

unsafe_allow_html=True

)



st.write("")



# ==========================================================
# LOAD GOOGLE SHEET DATA
# ==========================================================


@st.cache_data
def load_data():


    url = st.secrets["GOOGLE_SHEET_URL"]


    csv_url = (
        url
        .split("/edit")[0]
        +
        "/export?format=csv"
    )


    df = pd.read_csv(csv_url)


    return df




df = load_data()



# ==========================================================
# AUTOMATIC COLUMN DETECTION
# ==========================================================


def find_column(columns, keywords):


    for col in columns:


        name = col.lower()


        for key in keywords:


            if key.lower() in name:

                return col


    return None



columns=df.columns



week_col=find_column(

columns,

[
"epid",
"minggu",
"me",
"week"
]

)



diag_col=find_column(

columns,

[
"diag",
"penyakit"
]

)



gender_col=find_column(

columns,

[
"jan",
"sex",
"gender"
]

)



age_col=find_column(

columns,

[
"umur",
"age"
]

)



address_col=find_column(

columns,

[
"alamat",
"lokasi",
"address"
]

)



name_col=find_column(

columns,

[
"nama"
]

)



lat_col=find_column(

columns,

[
"lat"
]

)



lon_col=find_column(

columns,

[
"long",
"longitude"
]

)



# ==========================================================
# DATA CLEANING
# ==========================================================



# AGE GROUP


if age_col:


    df[age_col]=pd.to_numeric(

        df[age_col],

        errors="coerce"

    )



    def age_group(x):


        if pd.isna(x):

            return "Tidak diketahui"


        elif x<=14:

            return "14 dan ke bawah"


        elif x<=50:

            return "15 - 50"


        else:

            return "51 dan ke atas"



    df["Kumpulan Umur"]=df[age_col].apply(age_group)





# GENDER CLEANING


if gender_col:


    def clean_gender(x):


        x=str(x).lower()


        if x in [
            "l",
            "lelaki",
            "male",
            "m"
        ]:

            return "Lelaki"


        elif x in [
            "p",
            "perempuan",
            "female",
            "f"
        ]:

            return "Perempuan"


        return "Tidak diketahui"



    df["Jantina Standard"]=df[gender_col].apply(

        clean_gender

    )



# ==========================================================
# SESSION FILTER STATE
# ==========================================================


if "filtered_df" not in st.session_state:


    st.session_state.filtered_df=df.copy()



data=st.session_state.filtered_df



# ==========================================================
# SIDEBAR FILTER
# ==========================================================


st.sidebar.header(
"🔎 FILTER DATA"
)



if week_col:


    selected_week=st.sidebar.multiselect(

        "Epid Minggu",

        df[week_col].dropna().unique()

    )

else:

    selected_week=[]



if diag_col:


    selected_diag=st.sidebar.multiselect(

        "Diagnosis",

        df[diag_col].dropna().unique()

    )

else:

    selected_diag=[]



if gender_col:


    selected_gender=st.sidebar.multiselect(

        "Jantina",

        df[gender_col].dropna().unique()

    )

else:

    selected_gender=[]




if st.sidebar.button(
"🔄 BATAL SEMUA TAPISAN"
):


    st.session_state.filtered_df=df.copy()

    st.rerun()



# APPLY FILTER


filtered=df.copy()



if selected_week:


    filtered=filtered[
        filtered[week_col].isin(selected_week)
    ]



if selected_diag:


    filtered=filtered[
        filtered[diag_col].isin(selected_diag)
    ]



if selected_gender:


    filtered=filtered[
        filtered[gender_col].isin(selected_gender)
    ]



data=filtered
