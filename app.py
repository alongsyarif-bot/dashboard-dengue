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
# ==========================================================
# KPI SECTION
# ==========================================================


st.markdown(
"""
<div class="section-card">

<h2>
📊 Ringkasan Kes
</h2>

</div>
""",
unsafe_allow_html=True
)


st.write("")



# KPI CALCULATIONS


total_cases=len(data)



# Highest Diagnosis

if diag_col and len(data)>0:


    top_diag=data[diag_col].value_counts().idxmax()


else:

    top_diag="Tiada Data"



# Location affected

if address_col:


    affected_location=data[address_col].nunique()


else:

    affected_location=0



update_time=datetime.now().strftime(
"%d-%m-%Y %H:%M:%S"
)



# ==========================================================
# KPI CARDS
# ==========================================================


k1,k2,k3,k4=st.columns(4)



with k1:


    st.markdown(

    f"""

    <div class="kpi-card">

    <div class="kpi-title">
    Jumlah Kes
    </div>


    <div class="kpi-value">
    {total_cases:,}
    </div>


    </div>

    """,

    unsafe_allow_html=True

    )



with k2:


    st.markdown(

    f"""

    <div class="kpi-card">


    <div class="kpi-title">

    Diagnosis Tertinggi

    </div>


    <div class="kpi-value">

    {top_diag}

    </div>


    </div>

    """,

    unsafe_allow_html=True

    )




with k3:


    st.markdown(

    f"""

    <div class="kpi-card">


    <div class="kpi-title">

    Lokaliti Terjejas

    </div>


    <div class="kpi-value">

    {affected_location}

    </div>


    </div>


    """,

    unsafe_allow_html=True

    )




with k4:


    st.markdown(

    f"""

    <div class="kpi-card">


    <div class="kpi-title">

    Kemaskini Terakhir

    </div>


    <div class="kpi-value">

    {update_time}

    </div>


    </div>


    """,

    unsafe_allow_html=True

    )



st.write("")



# ==========================================================
# IMPORT PLOTLY
# ==========================================================


import plotly.express as px



# ==========================================================
# DIAGNOSIS ANALYSIS
# ==========================================================


st.markdown(

"""

<div class="section-card">

<h2>
🦠 Analisis Diagnosis
</h2>

</div>

""",

unsafe_allow_html=True

)



if diag_col:


    diag_count=(

        data[diag_col]

        .value_counts()

        .reset_index()

    )


    diag_count.columns=[

        "Diagnosis",

        "Jumlah"

    ]



    fig_diag=px.bar(

        diag_count,

        x="Jumlah",

        y="Diagnosis",

        orientation="h",

        text="Jumlah",

        title="Taburan Diagnosis"

    )


    fig_diag.update_layout(

        plot_bgcolor="white",

        paper_bgcolor="white",

        height=450

    )



    st.plotly_chart(

        fig_diag,

        use_container_width=True

    )



else:


    st.warning(
    "Lajur diagnosis tidak dijumpai"
    )





# ==========================================================
# GENDER + AGE CHART
# ==========================================================


c1,c2=st.columns(2)



# ------------------------------
# GENDER DOUGHNUT
# ------------------------------


with c1:



    st.markdown(

    """

    <div class="section-card">

    <h3>
    👥 Analisis Jantina
    </h3>

    </div>

    """,

    unsafe_allow_html=True

    )



    if "Jantina Standard" in data.columns:


        gender_count=(

            data["Jantina Standard"]

            .value_counts()

            .reset_index()

        )


        gender_count.columns=[

            "Jantina",

            "Jumlah"

        ]



        fig_gender=px.pie(

            gender_count,

            values="Jumlah",

            names="Jantina",

            hole=0.55

        )


        fig_gender.update_layout(

            height=400

        )


        st.plotly_chart(

            fig_gender,

            use_container_width=True

        )



# ------------------------------
# AGE GROUP
# ------------------------------


with c2:



    st.markdown(

    """

    <div class="section-card">


    <h3>

    👶 Analisis Kumpulan Umur

    </h3>


    </div>

    """,

    unsafe_allow_html=True

    )



    if "Kumpulan Umur" in data.columns:


        age_count=(

            data["Kumpulan Umur"]

            .value_counts()

            .reset_index()

        )



        age_count.columns=[

            "Kumpulan Umur",

            "Jumlah"

        ]



        fig_age=px.bar(

            age_count,

            x="Kumpulan Umur",

            y="Jumlah",

            text="Jumlah",

            title=""

        )



        fig_age.update_layout(

            height=400,

            plot_bgcolor="white"

        )


        st.plotly_chart(

            fig_age,

            use_container_width=True

        )



# ==========================================================
# END PART 2
# ==========================================================
