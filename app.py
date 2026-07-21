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

# ==========================================================
# BILIK GERAKAN
# Epidemiological Surveillance Dashboard
# Streamlit Government Version
# PART 2
# ==========================================================


import streamlit as st
import pandas as pd
import numpy as np

from datetime import datetime

from auth import (
    check_login,
    login_page,
    logout
)



# ==========================================================
# AUTHENTICATION
# ==========================================================


if not check_login():

    login_page()

    st.stop()



# ==========================================================
# PAGE CONFIG
# ==========================================================


st.set_page_config(

    page_title="BILIK GERAKAN",

    page_icon="🏥",

    layout="wide"

)



# ==========================================================
# GOVERNMENT CSS
# ==========================================================


st.markdown(

"""

<style>


/* BACKGROUND */


.stApp {

background:#f4f6f9;

}



/* REMOVE PADDING */


.block-container {

padding-top:1rem;

padding-left:3rem;

padding-right:3rem;

}




/* HEADER */


.gov-header {


background:

linear-gradient(

135deg,

#003366,

#005b96

);


padding:30px;


border-radius:15px;


color:white;


box-shadow:

0 4px 15px rgba(0,0,0,0.15);


}




.live {


color:#00e676;


font-weight:bold;


}




/* CARDS */


.card {


background:white;


padding:20px;


border-radius:12px;


box-shadow:

0 3px 10px rgba(0,0,0,0.08);


border-left:

5px solid #005b96;


}




.card-title {


font-size:14px;


color:#64748b;


}




.card-value {


font-size:28px;


font-weight:bold;


color:#003366;


}




.section {


background:white;


padding:20px;


border-radius:12px;


margin-top:20px;


box-shadow:

0 3px 10px rgba(0,0,0,0.06);


}



</style>


""",

unsafe_allow_html=True

)





# ==========================================================
# HEADER
# ==========================================================


st.markdown(

f"""

<div class="gov-header">


<h1>

🏥 BILIK GERAKAN

</h1>


<h3>

Epidemiological Surveillance System

</h3>


<p>

<span class="live">

🟢 SYSTEM ONLINE

</span>


&nbsp;&nbsp;


User:

<b>

{st.session_state.username}

</b>


|

Role:

<b>

{st.session_state.role}

</b>


</p>


</div>


""",

unsafe_allow_html=True

)



st.write("")



logout()



# ==========================================================
# LOAD GOOGLE SHEET
# ==========================================================



@st.cache_data

def load_data():


    url=st.secrets["GOOGLE_SHEET_URL"]



    csv_url=(

        url.split("/edit")[0]

        +

        "/export?format=csv"

    )



    df=pd.read_csv(csv_url)



    return df





df=load_data()



df=df.replace(

    ["",

    "-",

    "NA",

    "N/A"],

    np.nan

)



df=df.fillna(

    "Tidak diketahui"

)



# ==========================================================
# AUTO COLUMN DETECTION
# ==========================================================


def find_column(

    columns,

    keywords

):


    for col in columns:


        text=col.lower()



        for key in keywords:


            if key.lower() in text:


                return col



    return None




cols=df.columns



week_col=find_column(

    cols,

    [

    "epid",

    "minggu",

    "me",

    "week"

    ]

)



diag_col=find_column(

    cols,

    [

    "diag",

    "penyakit"

    ]

)



gender_col=find_column(

    cols,

    [

    "jantina",

    "jan",

    "sex",

    "gender"

    ]

)



age_col=find_column(

    cols,

    [

    "umur",

    "age"

    ]

)



address_col=find_column(

    cols,

    [

    "alamat",

    "lokasi",

    "address"

    ]

)




lat_col=find_column(

    cols,

    [

    "lat"

    ]

)



lon_col=find_column(

    cols,

    [

    "long",

    "longitude"

    ]

)





# ==========================================================
# DATA CLEANING
# ==========================================================



if age_col:


    df[age_col]=pd.to_numeric(

        df[age_col],

        errors="coerce"

    )



    def age_group(age):


        if pd.isna(age):

            return "Tidak diketahui"


        if age<=14:

            return "14 dan ke bawah"


        elif age<=50:

            return "15 - 50"


        else:

            return "51 dan ke atas"




    df["Kumpulan Umur"]=df[age_col].apply(

        age_group

    )






if gender_col:


    def gender_clean(x):


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



        else:


            return "Tidak diketahui"




    df["Jantina Standard"]=df[gender_col].apply(

        gender_clean

    )




# ==========================================================
# SIDEBAR FILTER
# ==========================================================



st.sidebar.title(

"🔎 PENAPIS DATA"

)



st.sidebar.caption(

"Dashboard Kawalan Epidemiologi"

)




filtered=df.copy()



if week_col:


    weeks=st.sidebar.multiselect(

        "Epid Minggu",

        sorted(

            df[week_col]

            .unique()

        )

    )


    if weeks:


        filtered=filtered[

            filtered[week_col]

            .isin(weeks)

        ]




if diag_col:


    diagnosis=st.sidebar.multiselect(

        "Diagnosis",

        sorted(

            df[diag_col]

            .unique()

        )

    )


    if diagnosis:


        filtered=filtered[

            filtered[diag_col]

            .isin(diagnosis)

        ]




if gender_col:


    gender=st.sidebar.multiselect(

        "Jantina",

        sorted(

            df[gender_col]

            .unique()

        )

    )


    if gender:


        filtered=filtered[

            filtered[gender_col]

            .isin(gender)

        ]





data=filtered
# ==========================================================
# PART 3
# KPI + ANALYTICS
# ==========================================================


import plotly.express as px



# ==========================================================
# RESET CROSS FILTER
# ==========================================================


if "cross_filter" not in st.session_state:

    st.session_state.cross_filter=None



def clear_filter():

    st.session_state.cross_filter=None

    st.rerun()



if st.session_state.cross_filter:


    st.warning(

        f"""

        Active Filter:

        {st.session_state.cross_filter}

        """

    )


    if st.button(

        "🔴 BATAL SEMUA TAPISAN SILANG"

    ):

        clear_filter()





# ==========================================================
# APPLY CROSS FILTER
# ==========================================================


if st.session_state.cross_filter:


    column,value=st.session_state.cross_filter


    if column in data.columns:


        data=data[

            data[column]==value

        ]





# ==========================================================
# DASHBOARD TITLE
# ==========================================================


st.markdown(

"""

<div class="section">

<h2>

📊 Ringkasan Epidemiologi

</h2>

</div>

""",

unsafe_allow_html=True

)



# ==========================================================
# KPI CALCULATION
# ==========================================================



total_cases=len(data)



if diag_col and len(data)>0:


    highest_diag=(

        data[diag_col]

        .value_counts()

        .idxmax()

    )

else:

    highest_diag="-"



if address_col:


    locality=data[address_col].nunique()


else:

    locality=0




last_update=datetime.now().strftime(

"%d/%m/%Y %H:%M"

)





# ==========================================================
# KPI CARDS
# ==========================================================


c1,c2,c3,c4=st.columns(4)



def kpi_card(title,value):


    return f"""

    <div class="card">


    <div class="card-title">

    {title}

    </div>


    <div class="card-value">

    {value}

    </div>


    </div>

    """





with c1:


    st.markdown(

        kpi_card(

            "Jumlah Kes",

            f"{total_cases:,}"

        ),

        unsafe_allow_html=True

    )





with c2:


    st.markdown(

        kpi_card(

            "Diagnosis Utama",

            highest_diag

        ),

        unsafe_allow_html=True

    )





with c3:


    st.markdown(

        kpi_card(

            "Lokaliti Terjejas",

            locality

        ),

        unsafe_allow_html=True

    )





with c4:


    st.markdown(

        kpi_card(

            "Kemaskini Terakhir",

            last_update

        ),

        unsafe_allow_html=True

    )




# ==========================================================
# DIAGNOSIS BAR CHART
# ==========================================================



st.markdown(

"""

<div class="section">

<h2>

🦠 Analisis Diagnosis

</h2>

</div>

""",

unsafe_allow_html=True

)




if diag_col:


    diag_df=(

        data[diag_col]

        .value_counts()

        .reset_index()

    )


    diag_df.columns=[

        "Diagnosis",

        "Kes"

    ]




    fig_diag=px.bar(

        diag_df,

        x="Kes",

        y="Diagnosis",

        orientation="h",

        text="Kes",

        color="Diagnosis",

        template="plotly_white"

    )



    fig_diag.update_layout(

        showlegend=False,

        height=450,

        font=dict(

            family="Arial",

            size=13

        )

    )




    diag_event=st.plotly_chart(

        fig_diag,

        use_container_width=True,

        on_select="rerun"

    )





# ==========================================================
# GENDER + AGE
# ==========================================================



col1,col2=st.columns(2)




# ==========================================================
# GENDER DOUGHNUT
# ==========================================================



with col1:



    st.markdown(

    """

    <div class="section">

    <h3>

    👥 Jantina

    </h3>

    </div>

    """,

    unsafe_allow_html=True

    )




    gender_df=(

        data["Jantina Standard"]

        .value_counts()

        .reset_index()

    )


    gender_df.columns=[

        "Jantina",

        "Kes"

    ]





    fig_gender=px.pie(

        gender_df,

        names="Jantina",

        values="Kes",

        hole=0.55,

        template="plotly_white"

    )



    st.plotly_chart(

        fig_gender,

        use_container_width=True

    )






# ==========================================================
# AGE GROUP
# ==========================================================



with col2:



    st.markdown(

    """

    <div class="section">


    <h3>

    👶 Kumpulan Umur

    </h3>


    </div>

    """,

    unsafe_allow_html=True

    )




    age_df=(

        data["Kumpulan Umur"]

        .value_counts()

        .reset_index()

    )



    age_df.columns=[

        "Kumpulan Umur",

        "Kes"

    ]




    fig_age=px.bar(

        age_df,

        x="Kumpulan Umur",

        y="Kes",

        text="Kes",

        template="plotly_white"

    )



    fig_age.update_layout(

        height=400

    )



    st.plotly_chart(

        fig_age,

        use_container_width=True

    )


# ==========================================================
# PART 4
# GIS OUTBREAK MAP + SECURITY
# ==========================================================


import folium

from folium.plugins import HeatMap

from streamlit_folium import st_folium

from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter





# ==========================================================
# ADDRESS TO GPS
# ==========================================================


@st.cache_data(show_spinner=False)

def geocode_address(df):


    # Already has coordinate


    if (

        lat_col

        and

        lon_col

        and

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





    if address_col is None:


        return df





    geolocator=Nominatim(

        user_agent=

        "bilik_gerakan_system"

    )



    geocode=RateLimiter(

        geolocator.geocode,

        min_delay_seconds=1

    )



    lat=[]

    lon=[]




    for address in df[address_col]:


        try:


            result=geocode(

                str(address)+", Malaysia"

            )



            if result:


                lat.append(

                    result.latitude

                )



                lon.append(

                    result.longitude

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






# ==========================================================
# PROCESS MAP DATA
# ==========================================================


with st.spinner(

"🗺️ Membina peta outbreak..."

):


    map_df=geocode_address(

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

<div class="section">

<h2>

🇲🇾 Peta Pemantauan Kes

</h2>

<p>

Geospatial Epidemiological Surveillance

</p>


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

    zoom_start=6,

    tiles="CartoDB positron"

)




# Diagnosis colour


colors=[

"red",

"blue",

"green",

"orange",

"purple",

"darkred",

"cadetblue"

]



diag_color={}



if diag_col:


    for i,d in enumerate(

        data[diag_col].unique()

    ):


        diag_color[d]=colors[

            i %

            len(colors)

        ]




heat=[]




for _,row in map_df.iterrows():



    diagnosis=(

        row[diag_col]

        if diag_col

        else

        "Unknown"

    )



    colour=diag_color.get(

        diagnosis,

        "red"

    )



    folium.CircleMarker(

        location=[

            row["Latitude"],

            row["Longitude"]

        ],


        radius=8,


        color=colour,


        fill=True,


        fill_opacity=0.65,


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



    heat.append(

        [

        row["Latitude"],

        row["Longitude"],

        1

        ]

    )





# Heat layer


if heat:


    HeatMap(

        heat,

        radius=30

    ).add_to(m)





st_folium(

    m,

    width=1200,

    height=650

)





# ==========================================================
# LATEST CASES
# ==========================================================



st.markdown(

"""

<div class="section">


<h2>

📋 5 Pendaftaran Terkini

</h2>


</div>

""",

unsafe_allow_html=True

)



latest_columns=[]



for c in [

"Tkh Input Notifikasi",

"Tarikh Diagnosis",

"Diagnosis",

"Sub Diagnosis",

"Status Pesakit",

"Alamat semasa/kejadian"

]:


    if c in data.columns:


        latest_columns.append(c)





if latest_columns:


    st.dataframe(

        data[latest_columns]

        .tail(5),

        use_container_width=True

    )






# ==========================================================
# DATA SECURITY
# ==========================================================



st.markdown(

"""

<div class="section">


<h2>

🔒 Keselamatan Data Pesakit

</h2>


</div>


""",

unsafe_allow_html=True

)



st.info(

"""

Maklumat peribadi pesakit tidak dipaparkan.

Dashboard ini hanya menunjukkan analisis epidemiologi.

Akses rekod penuh adalah melalui sistem pangkalan data berautoriti.

"""

)





# ==========================================================
# EXPORT CONTROL
# ==========================================================



if st.session_state.role=="Administrator":



    export_df=data.copy()



    sensitive=[

    "Nama Pesakit",

    "No Pengenalan/No Dokumen Perjalanan Pesakit"

    ]



    for c in sensitive:


        if c in export_df.columns:


            export_df.drop(

                columns=c,

                inplace=True

            )




    csv=export_df.to_csv(

        index=False

    )



    st.download_button(

        "⬇️ Export Laporan",

        csv,

        "laporan_bilik_gerakan.csv",

        "text/csv"

    )



else:


    st.warning(

    "Export laporan hanya untuk Administrator."

    )



# ==========================================================
# END SYSTEM
# ==========================================================


st.markdown(

"""

<hr>


<center>

<b>

🏥 BILIK GERAKAN

</b>


<br>

Epidemiological Surveillance System


<br>

Government Monitoring Platform


</center>


""",

unsafe_allow_html=True

)
