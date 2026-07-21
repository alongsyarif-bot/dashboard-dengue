import streamlit as st
import pandas as pd
import plotly.express as px

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

from geopy.geocoders import Nominatim
import time


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Bilik Gerakan Dashboard",
    page_icon="🏥",
    layout="wide"
)


# =====================================
# TITLE
# =====================================

st.title(
    "🏥 BILIK GERAKAN"
)

st.subheader(
    "Epidemiological Surveillance Dashboard"
)


# =====================================
# LOAD DATA
# =====================================


@st.cache_data
def load_data():


    url = st.secrets["GOOGLE_SHEET_URL"]


    csv_url = (
        url
        .replace(
            "/edit?usp=sharing",
            ""
        )
        +
        "/export?format=csv"
    )


    df=pd.read_csv(csv_url)


    return df



df=load_data()



df=df.fillna("Unknown")



# =====================================
# CLEAN
# =====================================


df["Umur (Tahun)"]=pd.to_numeric(
    df["Umur (Tahun)"],
    errors="coerce"
)



# =====================================
# SIDEBAR FILTER
# =====================================


st.sidebar.header(
"🔎 FILTER"
)


week_filter=st.sidebar.multiselect(

"Epid Minggu",

df["Epid Minggu (Tkh Input Notifikasi)"]
.unique()

)



diagnosis_filter=st.sidebar.multiselect(

"Diagnosis",

df["Diagnosis"]
.unique()

)



gender_filter=st.sidebar.multiselect(

"Jantina",

df["Jantina"]
.unique()

)



filtered=df.copy()



if week_filter:

    filtered=filtered[
        filtered[
        "Epid Minggu (Tkh Input Notifikasi)"
        ].isin(
            week_filter
        )
    ]



if diagnosis_filter:

    filtered=filtered[
        filtered["Diagnosis"]
        .isin(
            diagnosis_filter
        )
    ]



if gender_filter:

    filtered=filtered[
        filtered["Jantina"]
        .isin(
            gender_filter
        )
    ]



# =====================================
# KPI
# =====================================


col1,col2,col3,col4=st.columns(4)



with col1:

    st.metric(
        "Total Cases",
        len(filtered)
    )


with col2:

    death=filtered[
    filtered["Status Pesakit"]
    =="Meninggal"
    ]

    st.metric(
        "Death",
        len(death)
    )


with col3:

    st.metric(
        "Average Age",
        round(
        filtered["Umur (Tahun)"]
        .mean(),
        1
        )
    )


with col4:

    st.metric(
        "Diagnosis",
        filtered["Diagnosis"]
        .nunique()
    )



# =====================================
# CHART SECTION
# =====================================


st.divider()


col1,col2=st.columns(2)



with col1:


    week_chart=(

    filtered
    .groupby(
    "Epid Minggu (Tkh Input Notifikasi)"
    )
    .size()
    .reset_index(
    name="Cases"
    )

    )


    fig=px.line(

        week_chart,

        x="Epid Minggu (Tkh Input Notifikasi)",

        y="Cases",

        markers=True,

        title="Epidemic Trend"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



with col2:


    diag=(

    filtered
    ["Diagnosis"]
    .value_counts()
    .reset_index()

    )


    diag.columns=[
    "Diagnosis",
    "Cases"
    ]


    fig=px.bar(

        diag,

        x="Diagnosis",

        y="Cases",

        title="Diagnosis Distribution"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =====================================
# DEMOGRAPHIC
# =====================================


st.subheader(
"👥 Patient Demographic"
)



col1,col2=st.columns(2)



with col1:

    gender=filtered[
    "Jantina"
    ].value_counts()


    fig=px.pie(

        values=gender.values,

        names=gender.index,

        title="Gender"

    )

    st.plotly_chart(fig)



with col2:

    status=filtered[
    "Status Pesakit"
    ].value_counts()


    fig=px.pie(

        values=status.values,

        names=status.index,

        title="Patient Status"

    )


    st.plotly_chart(fig)



# =====================================
# MAP
# =====================================


st.divider()


st.subheader(
"🇲🇾 Outbreak Location Map"
)



map_df=filtered.dropna(
subset=[
"Latitude",
"Longitude"
]
)



m=folium.Map(

location=[
4.21,
101.97
],

zoom_start=6

)



# markers


for _,row in map_df.iterrows():


    folium.CircleMarker(

        [

        row["Latitude"],

        row["Longitude"]

        ],

        radius=5,

        popup=

        f"""

        Name:
        {row['Nama Pesakit']}

        <br>

        Diagnosis:
        {row['Diagnosis']}

        """

    ).add_to(m)



# heatmap


heat_data=[

[
row["Latitude"],
row["Longitude"],
1

]

for _,row in map_df.iterrows()

]


HeatMap(
heat_data
).add_to(m)



st_folium(

m,

width=1000,

height=600

)



# =====================================
# PATIENT TABLE
# =====================================


st.divider()


st.subheader(
"📋 Patient Database"
)



st.dataframe(

filtered,

use_container_width=True

)
