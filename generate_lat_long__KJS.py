#!/usr/bin/env python3

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