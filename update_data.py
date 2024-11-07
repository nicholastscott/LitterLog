import pandas as pd
import requests
from datetime import datetime

# Step 1: Fetch current dataset from GitHub
#url = "https://raw.githubusercontent.com/nicholastscott/LitterLog/main/dumpings.csv"
#current_data = pd.read_csv(url, parse_dates=['requested_datetime', 'closed_datetime'], encoding='latin1')

# Step 2: Find the most recent requested_datetime
#latest_date = current_data['requested_datetime'].max()
#latest_date = latest_date.tz_convert('UTC')

# Step 3: Query the API for new or modified records
query = f"""
SELECT cartodb_id,objectid,service_request_id,status,status_notes,requested_datetime,updated_datetime,expected_datetime,closed_datetime,address,zipcode,media_url,lat,lon 
FROM public_cases_fc 
WHERE 
      ( 
        (requested_datetime > '{latest_date}') --OR 
        --(status = 'Open' AND closed_datetime IS NOT NULL)
      ) 
      AND subject = 'Illegal Dumping'
"""
response = requests.get("https://phl.carto.com/api/v2/sql", params={'q': query})
new_data = pd.DataFrame(response.json()['rows'])
# Check if there are new records, if not then exit
if new_data.empty:
    print("No new records fetched from the API.")
    sys.exit(0)  # Exit the script gracefully with a status code of 0 (normal termination)

new_data['requested_datetime'] = pd.to_datetime(new_data['requested_datetime'])
