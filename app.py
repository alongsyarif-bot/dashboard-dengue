import streamlit as st
import pandas as pd
import plotly.express as px

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Bilik Gerakan Dashboard",
    page_icon="🏥",
    layout="wide"
)


# ==================================================
# HEADER
# ==================================================

st.title(
    "🏥 BILIK GERAKAN"
)

st.subheader(
    "Epidemiological Surveillance Dashboard"
)



# ==================================================
# GOOGLE SHEET LOAD
# ==================================================


def convert_sheet_url(url):

    import re

    sheet_id=re.search(
        r"/d/([a-zA-Z0-9-_]+)",
        url
    ).group(1)


    return (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    )



@st.cache_data
def load_data():

    url=st.secrets[
        "GOOGLE_SHEET_URL"
    ]


    csv_url=convert_sheet_url(
        url
    )


    df=pd.read_csv(
        csv_url
    )


    return df



df=load_data()



df=df.fillna(
    "Unknown"
)



# ==================================================
# ADDRESS GEOCODING
# ==================================================


@st.cache_data
def geocode_addresses(df):


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


    for address in df[
        "Alamat semasa/kejadian"
    ]:


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



    df["Latitude"]=lat

    df["Longitude"]=lon


    return df



if (
"Latitude" not in df.columns
or
"Longitude" not in df.columns
):

    with st.spinner(
        "📍 Converting addresses to GPS coordinates..."
    ):

        df=geocode_addresses(df)



# ==================================================
# DATA CLEANING
# ==================================================


df["Umur (Tahun)"]=pd.to_numeric(
    df["Umur (Tahun)"],
    errors="coerce"
)



# ==================================================
# SIDEBAR FILTER
# ==================================================


st.sidebar.header(
"🔎 FILTER"
)



week=st.sidebar.multiselect(

"Epid Minggu",

df[
"Epid Minggu (Tkh Input Notifikasi)"
]
.unique()

)



diagnosis=st.sidebar.multiselect(

"Diagnosis",

df[
"Diagnosis"
]
.unique()

)



gender=st.sidebar.multiselect(

"Jantina",

df[
"Jantina"
]
.unique()

)



data=df.copy()



if week:

    data=data[
        data[
        "Epid Minggu (Tkh Input Notifikasi)"
        ]
        .isin(week)
    ]



if diagnosis:

    data=data[
        data["Diagnosis"]
        .isin(diagnosis)
    ]



if gender:

    data=data[
        data["Jantina"]
        .isin(gender)
    ]



# ==================================================
# KPI
# ==================================================


c1,c2,c3,c4=st.columns(4)



with c1:

    st.metric(
        "Total Cases",
        len(data)
    )



with c2:

    death=data[
        data[
        "Status Pesakit"
        ]
        ==
        "Meninggal"
    ]


    st.metric(
        "Death",
        len(death)
    )



with c3:

    st.metric(

        "Average Age",

        round(
            data[
            "Umur (Tahun)"
            ]
            .mean(),
            1
        )

    )



with c4:

    st.metric(

        "Diagnosis",

        data[
        "Diagnosis"
        ]
        .nunique()

    )



# ==================================================
# CHARTS
# ==================================================


st.divider()


col1,col2=st.columns(2)



with col1:


    trend=data.groupby(

        "Epid Minggu (Tkh Input Notifikasi)"

    ).size().reset_index(

        name="Cases"

    )


    fig=px.line(

        trend,

        x=
        "Epid Minggu (Tkh Input Notifikasi)",

        y="Cases",

        markers=True,

        title="Epidemic Trend"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )




with col2:


    diag=data[
        "Diagnosis"
    ].value_counts().reset_index()


    diag.columns=[
        "Diagnosis",
        "Cases"
    ]



    fig=px.bar(

        diag,

        x="Diagnosis",

        y="Cases",

        title="Diagnosis"

    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )




# ==================================================
# DEMOGRAPHIC
# ==================================================


col1,col2=st.columns(2)



with col1:


    gender_chart=data[
        "Jantina"
    ].value_counts()


    fig=px.pie(

        values=
        gender_chart.values,

        names=
        gender_chart.index,

        title="Gender"

    )


    st.plotly_chart(fig)



with col2:


    status=data[
        "Status Pesakit"
    ].value_counts()



    fig=px.pie(

        values=
        status.values,

        names=
        status.index,

        title="Patient Status"

    )


    st.plotly_chart(fig)




# ==================================================
# MAP
# ==================================================


st.divider()


st.subheader(
"🇲🇾 Outbreak Map"
)



map_data=data.copy()



map_data["Latitude"]=pd.to_numeric(

map_data["Latitude"],

errors="coerce"

)


map_data["Longitude"]=pd.to_numeric(

map_data["Longitude"],

errors="coerce"

)



map_data=map_data.dropna(

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



heat=[]



for _,row in map_data.iterrows():


    folium.CircleMarker(

        location=[

            row["Latitude"],

            row["Longitude"]

        ],

        radius=6,

        popup=

        f"""

        <b>{row['Nama Pesakit']}</b>

        <br>

        Diagnosis:
        {row['Diagnosis']}

        <br>

        Status:
        {row['Status Pesakit']}

        """

    ).add_to(m)



    heat.append(

        [

        row["Latitude"],

        row["Longitude"],

        1

        ]

    )



if heat:


    HeatMap(
        heat
    ).add_to(m)



else:

    st.warning(
        "No address can be mapped"
    )



st_folium(

m,

width=1000,

height=600

)






