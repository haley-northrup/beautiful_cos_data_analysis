#!/usr/bin/env python3
"""
This Python code that does the following 
- read the CDOT CSV files
- identify the rows with missing lat/long fields
- call the Google Geocode API with a Location 1/2 combined value, and write out updated rows.  

Obviously this code is not production ready but ran error free and the output passed basic validation checks.  
The initial shell of code was pulled from some Python/Google Geocode API tutorial.

NOTE: Need to set up a Google Cloud account which requires a credit card number even if you are planning on staying in the free API
volume range(s), enabling just the Geocoding API, and finding the right API key to add to my script.  

Google Cloud offers a myriad of APIs, options, security settings, etc. 
Here is a link to the Google Geocoding API for developers overview - https://developers.google.com/maps/documentation/geocoding/overview  

The strengths of the Google Geocode API over say Openstreet Maps is that it will return geocoding data (e.g. lat/long) for known logical intersections. 
It is my belief that maps.google.com uses the same API when an interactive user types a location into the "Search Google Maps" 
input box, which means I was able to manually test differing formats of my API input strings easily 
in advance and also sanity check results on a Google map.

"""

import requests
import pandas as pd
import math
import re

def geocode_address(api_key, address):

  url = 'https://maps.googleapis.com/maps/api/geocode/json'

  params = {
    'address': address,
    'key': api_key
  }

  response = requests.get(url, params=params)

  if response.status_code == 200:
    data = response.json()

    if data['status'] == 'OK':
      location = data['results'][0]['geometry']['location']
      lat = location['lat']
      lng = location['lng']
      return lat, lng

    else:
      print(f"Error: {data['error_message']}")
      return None, None

  else:
    print('Request failed.')
    return None, None

##########
## MAIN ##
##########
# open and read CSV
csv_file = 'test_locations.csv'
data = pd.read_csv(csv_file)
null_lat_long = 0

for index, row in data.iterrows():
   # initialize values
   city = ""
   crash_location = ""

   # get location raw data
   raw_lat = row['Latitude']
   raw_long = row['Longitude']
   location1 = row['Location 1']
   location2 = row['Location 2']
   city = row['City']

   # read next row if city is blank or
   # location 1 is unknown
   if city == '' or (isinstance(city, float) and math.isnan(city)) or re.match("UNK", location1):
      continue

   # check if latitude value is populated
   if math.isnan(raw_lat) or raw_lat == 999.999 or raw_lat == "" or not raw_lat :

      null_lat_long += 1
      # ignore unknown location 2 values
      if re.match("UNK", location2):
         crash_location = f'{row['Location 1']} {city} COLORADO'
      else:
         # combine locations in Google API format
         crash_location = f'{row['Location 1']} & {row['Location 2']} {city} COLORADO'
      ### print(null_lat_long, ': ', crash_location)

      api_key = '<insert_google_cloud_api_key>'

      lat, lon = geocode_address(api_key, crash_location)
      print(index, ': ', crash_location, ' => ',lat,lon)

      data.loc[index, ['Latitude']] = lat
      data.loc[index, ['Longitude']] = lon

      ### print(row)

data.to_csv(r'./updated_test_data.csv', sep=',', index=False)