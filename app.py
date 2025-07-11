import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import json
from collections import Counter
import pydeck as pdk

#import folium
#from streamlit_folium import st_folium
#from folium.plugins import HeatMap

#Page Config
st.set_page_config(layout="wide")

#Sidebar
with st.sidebar:
    st.logo("logo-no-background.png")
    st.title("Where It Ends Up: Mapping Illegal Dumping")
    st.write("DC 33, a union representing Philadelphia's municipal workers, went on strike July 1, 2025. This has frozen trash removal across the city of Philadelphia in hopes of better wages for these essential workers. Reports of illegal dumping are suspected to increase. The goal of this project is to increase transparency so that the City's 311 system and residents don't lose track of these requests at this critical time.")
    st.divider()
    st.subheader("Features")
    st.write("1. Stats")
    st.caption("" \
    "" \
    "In Progress: Day over Day rate calculation of Illegal Dumping Reports")
    st.write("2. Map")
    st.write("Mapbox")
    st.divider()
    st.caption("The views expressed here are my own and do not necessarily represent the views of the City of Philadelphia, DC 33, or Parker administration.")
    
    

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


#@st.cache_data           # <‑‑ put decorator *above* the function
#def get_phl_data(sql_query: str) -> pd.DataFrame:
#    """Fetch query from phl.carto.com and return as DataFrame (cached)."""
#    response = requests.get(
#        "https://phl.carto.com/api/v2/sql",
#        params={"q": sql_query},
#        timeout=30,
#    )
#    response.raise_for_status()        # good practice: surface HTTP errors
#    return pd.DataFrame(response.json()["rows"])

# use the cached function
#new_data = get_phl_data(query)


#Body of Webpage
st.header("High Level Stats")
timestamp = pd.Timestamp.now()
st.caption(f'Data since 7/1/2025, Last Fetched: [{timestamp}]')

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

top3adds = str(top3adds)

st.metric(
    label="Top Addresses Reported (Address, Frequency)", value=top3adds
)

st.divider()

st.write("Map of Hotspots")

#st.map(new_data)

#PyDeck Map
# Map configuration
view_state = pdk.ViewState(
    latitude=39.95119,
    longitude=-75.16564,
    zoom=11,
    pitch=5
)

heat_layer = pdk.Layer(
    "HeatmapLayer",
    data=new_data,
    opacity=0.8,
    get_position=["lon", "lat"],
    aggregation=pdk.types.String("COUNT"),
    pickable=False,
    threshold=.4
)

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=new_data,
    get_radius=30,
    get_position=["lon", "lat"],
    pickable=True,
    get_fill_color=[255, 0, 0, 160],
    threshold=.4,
)

tooltip = {
    "html": """
        <b>Address:</b> {address}<br/>
        <img src="{media_url}" width="150"/>
        """,
    "style": {"backgroundColor": "steelblue", "color": "white"}
}



st.pydeck_chart(pdk.Deck(layers=[heat_layer, scatter_layer], initial_view_state=view_state, tooltip=tooltip))




st.divider()



st.write("Raw Table from OpenData Philly")
#st.page_link("https://opendataphilly.org/datasets/311-service-and-information-requests/",label="OpenDataPhilly")
st.dataframe(new_data)
