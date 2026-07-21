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

# ==========================================================
# PART 3
# MAP + LOCATION ANALYSIS
# ==========================================================


import folium

from folium.plugins import HeatMap

from streamlit_folium import st_folium

from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter



# ==========================================================
# GEOCODING FUNCTION
# ==========================================================


@st.cache_data
def generate_coordinates(df):


    # Already have GPS

    if (

        lat_col in df.columns

        and

        lon_col in df.columns

    ):


        df["Latitude"]=pd.to_numeric(

            df[lat_col],

            errors="coerce"

        )


        df["Longitude"]=pd.to_numeric(

            df[lon_col],

            errors="coerce"

        )


        return df




    # If only address exists


    if address_col is None:


        return df




    geolocator=Nominatim(

        user_agent=
        "bilik_gerakan_dashboard"

    )



    geocode=RateLimiter(

        geolocator.geocode,

        min_delay_seconds=1

    )



    lat=[]

    lon=[]



    progress=st.progress(0)



    total=len(df)



    for i,address in enumerate(

        df[address_col]

    ):


        try:


            location=geocode(

                str(address)+", Malaysia"

            )



            if location:


                lat.append(

                    location.latitude

                )


                lon.append(

                    location.longitude

                )


            else:

                lat.append(None)

                lon.append(None)



        except:


            lat.append(None)

            lon.append(None)



        progress.progress(

            (i+1)/total

        )




    df["Latitude"]=lat

    df["Longitude"]=lon



    return df




# ==========================================================
# RUN LOCATION PROCESSING
# ==========================================================



with st.spinner(

"📍 Memproses lokasi kes..."

):


    map_df=generate_coordinates(

        data.copy()

    )




map_df["Latitude"]=pd.to_numeric(

    map_df["Latitude"],

    errors="coerce"

)



map_df["Longitude"]=pd.to_numeric(

    map_df["Longitude"],

    errors="coerce"

)



map_df=map_df.dropna(

    subset=[

        "Latitude",

        "Longitude"

    ]

)



# ==========================================================
# MAP HEADER
# ==========================================================



st.markdown(

"""

<div class="section-card">


<h2>

🇲🇾 Peta Taburan Kes Malaysia

</h2>


</div>

""",

unsafe_allow_html=True

)




# ==========================================================
# CREATE MAP
# ==========================================================



m=folium.Map(

    location=[

        4.2105,

        101.9758

    ],

    zoom_start=6

)




# Diagnosis colour


colour_list=[

"red",

"blue",

"green",

"orange",

"purple",

"darkred",

"cadetblue"

]



diagnosis_colour={}



if diag_col:


    diagnosis_values=data[diag_col].unique()



    for i,d in enumerate(

        diagnosis_values

    ):

        diagnosis_colour[d]=colour_list[

            i %

            len(colour_list)

        ]





heat_data=[]



for _,row in map_df.iterrows():



    diagnosis=row[diag_col] if diag_col else "Unknown"



    colour=diagnosis_colour.get(

        diagnosis,

        "red"

    )



    # count cases same location


    case_count=len(

        map_df[

            map_df["Latitude"]

            ==

            row["Latitude"]

        ]

    )



    radius=max(

        5,

        case_count*3

    )




    folium.CircleMarker(


        location=[

            row["Latitude"],

            row["Longitude"]

        ],


        radius=radius,


        color=colour,


        fill=True,


        fill_opacity=0.7,


        popup=f"""


        <b>BILIK GERAKAN</b>

        <br><br>

        Diagnosis:

        {diagnosis}


        <br>

        Lokasi:

        {row[address_col] if address_col else ''}


        """



    ).add_to(m)



    heat_data.append(

        [

            row["Latitude"],

            row["Longitude"],

            1

        ]

    )





# Heatmap layer


if heat_data:


    HeatMap(

        heat_data,

        radius=25

    ).add_to(m)




# Display map


st_folium(

    m,

    width=1200,

    height=650

)



# ==========================================================
# LATEST 5 CASES
# ==========================================================



st.markdown(

"""

<div class="section-card">


<h2>

📝 5 Pendaftaran Terkini

</h2>


</div>

""",

unsafe_allow_html=True

)



latest_columns=[]



for col in [

"Tarikh Diagnosis",

"Epid Minggu (Tkh Input Notifikasi)",

"Diagnosis",

"Sub Diagnosis",

"Status Pesakit",

"Alamat semasa/kejadian"

]:


    if col in data.columns:

        latest_columns.append(col)




if latest_columns:


    st.dataframe(

        data[latest_columns]

        .tail(5)

        .reset_index(drop=True),

        use_container_width=True

    )



# ==========================================================
# MASTER LIST PROTECTION
# ==========================================================



st.markdown(

"""

<div class="section-card">


<h2>

🔒 Data Induk Pesakit

</h2>


</div>

""",

unsafe_allow_html=True

)



st.info(

"""

Maklumat individu seperti Nama Pesakit dan No Pengenalan

tidak dipaparkan dalam dashboard awam.

Sila akses pangkalan data asal melalui sistem yang diluluskan.

"""

)



# Optional download for authorized user


safe_df=data.copy()



for sensitive in [

"Nama Pesakit",

"No Pengenalan/No Dokumen Perjalanan Pesakit"

]:


    if sensitive in safe_df.columns:


        safe_df=safe_df.drop(

            columns=sensitive

        )



csv=safe_df.to_csv(

    index=False

).encode("utf-8")



st.download_button(

    "⬇️ Export Ringkasan Data",

    csv,

    "bilik_gerakan_summary.csv",

    "text/csv"

)



# ==========================================================
# END APPLICATION
# ==========================================================
