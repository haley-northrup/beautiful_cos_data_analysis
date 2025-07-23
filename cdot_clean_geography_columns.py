# This file contains utility functions for cleaning CDOT crash data geography columns. 

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


def get_city_from_coordinates(latitude, longitude):
    """
    Retrieves the city from given latitude and longitude.
    """
    geolocator = Nominatim(user_agent="hmn") # Replace "my_geocoding_app" with a unique identifier
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            address = location.raw.get('address', {})
            city = address.get('city') or \
                   address.get('town') or \
                   address.get('village')
            return city
        else:
            return "NONE"
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Geocoding error: {e}")
        return "NONE"
    

def handle_missing_values_in_geography_columns(cdot_pdf):
    '''
    Ensure that all missing data NaN, None, Unknown, 999 are all 
    the same for a given column so filtering is easier. 
    '''

    # fill City and County nan values with 'NONE'
    string_geography_cols = ['City', 'County']
    cdot_pdf[string_geography_cols] = cdot_pdf[string_geography_cols].fillna('NONE')
    
    # mark "unknown" city as 'NONE'
    cdot_pdf.loc[cdot_pdf['City'].str.contains('UNKNOWN'), 'City'] = 'NONE'

    # fill latitude and longitude with 999.999000
    cdot_pdf['Latitude'] = cdot_pdf['Latitude'].fillna(999.999000)
    cdot_pdf['Longitude'] = cdot_pdf['Longitude'].fillna(999.999000)

    # set default Denver latitude and longitude value to 999.999000
    default_lat = 39.74602
    default_long = -104.98877
    default_lat_long_condition = (cdot_pdf['Latitude'] == default_lat) & (cdot_pdf['Longitude'] == default_long)
    cdot_pdf.loc[default_lat_long_condition, 'Latitude'] = 999.999000
    cdot_pdf.loc[default_lat_long_condition, 'Longitude'] = 999.999000

    # set 000 Latitude and Longitude to 999.999000
    zero_lat_long_condition = (cdot_pdf['Latitude'].round() == 0) & (cdot_pdf['Longitude'].round() == 0)
    cdot_pdf.loc[zero_lat_long_condition, 'Latitude'] = 999.999000
    cdot_pdf.loc[zero_lat_long_condition, 'Longitude'] = 999.999000

    return cdot_pdf

def fill_missing_city_values(cdot_pdf):
    # ensure all missing values are handled / aligned
    cdot_pdf = handle_missing_values_in_geography_columns(cdot_pdf)

    # remove missing Latitude and Longitude info
    cdot_pdf_w_lat_long = cdot_pdf.loc[~(cdot_pdf['Latitude'] == 999.999000) & ~(cdot_pdf['Longitude'] == 999.999000)]

    # filter to where city is not provided and see how often we can get the associated city
    cdot_pdf_w_latlong_and_no_city = cdot_pdf_w_lat_long.loc[cdot_pdf_w_lat_long['City'] == 'NONE']

    # get city from lat long
    cdot_pdf_w_latlong_and_no_city['City'] = cdot_pdf_w_latlong_and_no_city.apply(
            lambda row: get_city_from_coordinates(row['Latitude'], row['Longitude']),
            axis=1,
        )

    # join back in the new city values
    cdot_pdf.loc[cdot_pdf_w_latlong_and_no_city.index, 'City'] = cdot_pdf_w_latlong_and_no_city['City'].str.upper().values
    
    # some values set to null so reset those to "NONE"
    cdot_pdf['City'] = cdot_pdf['City'].fillna('NONE')
    
    return cdot_pdf 

def create_truncated_lat_long(cdot_pdf, decimal):
    '''
    Create truncated latitude and longitude columns to a specified decimal place
    '''
    cdot_pdf.loc[:, f"Latitude_{decimal}dec"] = cdot_pdf['Latitude'].round(decimal)
    cdot_pdf.loc[:, f"Longitude_{decimal}dec"] = cdot_pdf['Longitude'].round(decimal)
    
    return cdot_pdf

def combine_loc1_loc2_alphabetically(cdot_pdf):
    '''
    Create a combined location 1 and location 2 column ordered alphabetically 
    to make counting and filtering easier.
    '''
    # determine if Location 1 is first alphabetically
    cdot_pdf.loc[:, 'loc1_first'] = cdot_pdf.loc[:, 'Location 1'] < cdot_pdf.loc[:, 'Location 2'] 

    # combine Location 1 and Location 2 alphabetically 
    # location 1 is first
    cdot_pdf.loc[cdot_pdf['loc1_first'], 'alph_loc1_loc2'] = \
            cdot_pdf.loc[cdot_pdf['loc1_first'], 'Location 1'] + \
            ' ' + \
            cdot_pdf.loc[cdot_pdf['loc1_first'], 'Location 2']
    # location 2 is second 
    cdot_pdf.loc[~cdot_pdf['loc1_first'], 'alph_loc1_loc2'] = \
            cdot_pdf.loc[~cdot_pdf['loc1_first'], 'Location 2'] + \
            ' ' + \
            cdot_pdf.loc[~cdot_pdf['loc1_first'], 'Location 1']
    
    return cdot_pdf

