import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import json
from collections import Counter
#import folium

#Page Config
st.set_page_config(layout="wide")

#Sidebar
with st.sidebar:
    st.logo("logo-no-background.png")
    st.title("Where It Ends Up: Mapping Illegal Dumping")
    st.write("During the DC 33 strike that has frozen trash removal across the city of Philadelphia, reports of illegal dumping is sure to increase. The goal of this project is to increase transparency so that the City's 311 system and residents don't lose track of these requests at this critical time.")
    st.divider()
    st.subheader("Features")
    st.write("1. Stats")
    st.write("Methodology for D/D calculation: ")
    st.write("2. Map")
    st.write("Mapbox")
    

#Data

# Data Step 1: Query the API for new or modified records since 7/1/2025
query = f"""
SELECT cartodb_id,objectid,service_request_id,subject,status,status_notes,requested_datetime,updated_datetime,expected_datetime,closed_datetime,address,zipcode,media_url,lat,lon 
FROM public_cases_fc 
WHERE 
      ( 
        (requested_datetime >= '2025-07-01 00:00:00+00:00') OR 
        (status = 'Open' AND closed_datetime IS NOT NULL)
      ) 
      AND subject = 'Illegal Dumping'
      AND media_url IS NOT NULL
      AND media_url <> ''
"""
response = requests.get("https://phl.carto.com/api/v2/sql", params={'q': query})
new_data = pd.DataFrame(response.json()['rows'])


@st.cache_data           # <‑‑ put decorator *above* the function
def get_phl_data(sql_query: str) -> pd.DataFrame:
    """Fetch query from phl.carto.com and return as DataFrame (cached)."""
    response = requests.get(
        "https://phl.carto.com/api/v2/sql",
        params={"q": sql_query},
        timeout=30,
    )
    response.raise_for_status()        # good practice: surface HTTP errors
    return pd.DataFrame(response.json()["rows"])

# use the cached function
new_data = get_phl_data(query)



#Body of Webpage
st.header("High Level Stats")
st.write("Since 7/1/2025")

a, b = st.columns(2)

a.metric(
    label="Total Requests since Start of Strike", value=new_data.shape[0], delta_color="off"
)

#b.metric(
#    label="Day over Day Change", value=123, delta=123, delta_color="off"
#)

addresses = new_data['address']
word_counts= Counter(addresses)
top3adds= word_counts.most_common(3)

st.metric(
    label="Top Addresses Reported (Address, Frequency)", value=str(top3adds)
)

st.divider()

st.write("Map of Hotspots")

#m = folium.Map(new_data)

#HeatMap(new_data).add_to(m)

#st.pydeck_chart(m)

st.divider()



st.write("Raw Table from OpenData Philly")
#st.page_link("https://opendataphilly.org/datasets/311-service-and-information-requests/",label="OpenDataPhilly")
st.dataframe(new_data)

#Data Step 2: Caching Newly Queried Data
#@st.cache_data()
#def load_data():
#    data = pd.new_data
#    return data

# data = load_data()


# Cleaning up dataframe