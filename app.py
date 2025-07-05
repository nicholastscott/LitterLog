import streamlit as st
import pandas as pd
import numpy as np

#Page Config
st.set_page_config(layout="wide")

#Body of Webpage

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

#Data Step 2: Caching Newly Queried Data
@st.cache_data(new_data)



# Cleaning up dataframe
data = data.drop(columns=[])