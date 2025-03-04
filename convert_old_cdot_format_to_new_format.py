# This file contains utility functions for converting CDOT crash data from the 2007-2020 data format 
# to the 2021+ data format. 

import numpy as np 
import re

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Column Mapping Dictionaries 
map_location_old_to_new = {'ON': 'On Roadway', 
                'OFF LEFT': 'Ran off left side',
                'OFF RIGHT': 'Ran off right side', 
                'OFF AT TEE': 'Ran off "T" intersection',
                'UNKNOWN': np.nan,
                'OFF IN MEDIAN': 'Center median/ Island'}

map_road_desc_old_to_new = {'NON-INTERSECTION': 'Non-Intersection', 
                'AT INTERSECTION': 'At Intersection',
                'INTERSECTION RELATED': 'Intersection Related', 
                'PARKING LOT': 'Parking Lot',
                'AT DRIVEWAY ACCESS': 'Driveway Access Related',
                'ROUNDABOUT': 'Roundabout',
                'RAMP': 'Ramp', 
                'IN ALLEY': 'Alley Related',
                'UNKNOWN': np.nan}

map_harmful_event_old_to_new = {
    'HEAD-ON': 'Front to Front', 
    'GUARD RAIL': 'Guardrail unspecified',
    'PARKED MOTOR VEHICLE': 'Parked Motor Vehicle', 
    'REAR-END': 'Front to Rear',
    'BROADSIDE': 'old__broadside',
    'WILD ANIMAL': 'Wild Animal',
    'DELINEATOR POST': 'Delineator/Milepost',
    'LIGHT/UTILITY POLE': 'Light Pole/Utility Pole',
    'SIDESWIPE (SAME DIRECTION)': 'Side to Side-Same Direction', 
    'OVERTURNING': 'Overturning/Rollover',
    'CONCRETE BARRIER': 'Concrete Highway Barrier', 
    'PEDESTRIAN': 'Pedestrian', 
    'INVOLVING OTHER OBJECT': 'Other Non-Fixed Object (Describe in Narrative)', 
    'SIGN': 'Sign',
    'TREE/SHRUBBERY': 'Tree',
    'EMBANKMENT CUT/FILL SLOPE': 'Embankment', 
    'MAILBOX': 'Mailbox',
    'FENCE': 'Fence', 
    'CURB/RAISED MEDIAN': 'Curb', 
    'OTHER FIXED OBJECT': 'Other Fixed Object (Describe in Narrative)',
    'ROAD MAINTENANCE EQUIPMENT': 'old__road_maintenance_equipment',
    'BRIDGE RAIL': 'Bridge Structure (Not Overhead)',
    'SIDESWIPE (OPPOSITE DIRECTION)': 'Side to Side-Opposite Direction', 
    'LARGE BOULDERS OR ROCKS': 'Large Rocks or Boulder', 
    'OTHER NON-COLLISION': 'Other Non-Collision',
    'VEHICLE CARGO/DEBRIS': 'Vehicle Debris or Cargo',
    'BICYCLE': 'Bicycle/Motorized Bicycle', 
    'DOMESTIC ANIMAL': 'Domestic Animal', 
    'CABLE RAIL': 'Cable Rail', 
    'WALL/BUILDING': 'Wall or Building', 
    'CULVERT/HEADWALL': 'Culvert or Headwall', 
    'BARRICADE/TRAFFIC BARRIER': 'Barricade',
    'TRAFFIC SIGNAL POLE': 'Traffic Signal Pole', 
    'CRASH CUSHION': 'Crash Cushion/Traffic Barrel', 
    'RAILWAY VEHICLE': 'old__railway_vehicle', 
    'OVERTAKING TURN': np.nan, 
    'APPROACH TURN': np.nan,
    'UNKNOWN': np.nan}


map_accident_type_old_to_new = {
    'HEAD-ON': 'Head-On',
    'GUARD RAIL': 'Guardrail Unspecified',
    'PARKED MOTOR VEHICLE': 'Parked Motor Vehicle',
    'REAR-END': 'Rear-End', 
    'BROADSIDE': 'Broadside',
    'WILD ANIMAL': 'Wild Animal', 
    'OVERTURNING': 'Overturning/Rollover',
    'LIGHT/UTILITY POLE': 'Light Pole/Utility Pole',
    'SIDESWIPE (SAME DIRECTION)': 'Sideswipe Same Direction',
    'CONCRETE BARRIER': 'Concrete Highway Barrier',
    'PEDESTRIAN': 'Pedestrian',
    'SIGN': 'Sign',
    'TREE/SHRUBBERY': 'Tree',
    'APPROACH TURN': 'Approach Turn', 
    'EMBANKMENT CUT/FILL SLOPE': 'Embankment',
    'MAILBOX': 'Mailbox', 
    'FENCE': 'Fence', 
    'CURB/RAISED MEDIAN': 'Curb',
    'DELINEATOR POST': 'Delineator/Milepost', 
    'OTHER FIXED OBJECT': 'Other Fixed Object (Describe in Narrative)', 
    'BRIDGE RAIL': 'Bridge Structure (Not Overhead)', 
    'SIDESWIPE (OPPOSITE DIRECTION)': 'Sideswipe Opposite Direction', 
    'INVOLVING OTHER OBJECT': 'Other Non-Fixed Object Describe in Narrative)', 
    'OVERTAKING TURN': 'Overtaking Turn', 
    'CULVERT/HEADWALL': 'Culvert or Headwall',
    'LARGE BOULDERS OR ROCKS': 'Large Rocks or Boulder',
    'OTHER NON-COLLISION': 'Other Non-Collision', 
    'VEHICLE CARGO/DEBRIS': 'Vehicle Debris or Cargo', 
    'BICYCLE': 'Bicycle/Motorized Bicycle', 
    'ROAD MAINTENANCE EQUIPMENT': 'old__road_maintenance_equipment', 
    'DOMESTIC ANIMAL': 'Domestic Animal', 
    'CABLE RAIL': 'Cable Rail', 
    'WALL/BUILDING': 'Wall or Building', 
    'BARRICADE/TRAFFIC BARRIER': 'Barricade', 
    'TRAFFIC SIGNAL POLE': 'Traffic Signal Pole', 
    'CRASH CUSHION': 'Crash Cushion/Traffic Barrel', 
    'RAILWAY VEHICLE': 'old__railway_vehicle',
    'UNKNOWN': np.nan,
}

map_road_contour_curves_old_to_new = {
    'Not Applicable': np.nan,
    'STRAIGHT ON-LEVEL': 'Straight',
    'CURVE ON-GRADE': 'Curve Unknown Direction', 
    'STRAIGHT ON-GRADE': 'Straight',
    'CURVE ON-LEVEL': 'Curve Unknown Direction',
    'HILLCREST': 'Unknown',
    'UNKNOWN': 'Unknown',
}

map_road_contour_grade_old_to_new = {
    'Not Applicable': np.nan,
    'STRAIGHT ON-LEVEL': 'Level',
    'CURVE ON-GRADE': 'Unknown', 
    'STRAIGHT ON-GRADE': 'Unknown',
    'CURVE ON-LEVEL': 'Level',
    'HILLCREST': 'Hill Crest',
    'UNKNOWN': 'Unknown',
}

map_lighting_conditions_old_to_new = {
    'Not Applicable': np.nan, 
    'DARK-LIGHTED': 'Dark – Lighted', 
    'DAYLIGHT': 'Daylight', 
    'DAWN OR DUSK': 'Dawn or Dusk', 
    'DARK-UNLIGHTED': 'Dark – Unlighted', 
    'UNKNOWN': np.nan,
}

map_road_condition_old_to_new = {
    'Not Applicable': np.nan, 
    'ICY': 'Icy', 
    'DRY': 'Dry', 
    'SLUSHY': 'Slushy', 
    'WET W/VIS ICY ROAD TREATMENT': 'Wet W/Visible Icy Road Treatment', 
    'DRY W/VIS ICY ROAD TREATMENT': 'Dry W/Visible Icy Road Treatment',
    'WET': 'Wet', 
    'ICY W/VIS ICY ROAD TREATMENT': 'Icy W/Visible Icy Road Treatment', 
    'SNOWY': 'Snowy', 
    'UNKNOWN': np.nan, 
    'SNOWY W/VIS ICY ROAD TREATMENT': 'Snowy W/Visible Icy Road Treatment', 
    'SLUSHY W/VIS ICY ROAD TREATMENT': 'Slushy W/Visible Icy Road Treatment', 
    'FOREIGN MATERIAL': 'Foreign Material', 
    'MUDDY': 'Muddy'
}

map_weather_conditions_old_to_new = {
    'Not Applicable': np.nan, 
    'NONE': 'None', 
    'RAIN': 'Rain', 
    'SNOW/SLEET/HAIL': 'old__snow_sleet_hail',
    'WIND': 'Wind', 
    'FOG': 'Fog', 
    'DUST': 'Dust',
    'UNKNOWN': np.nan, 
}

map_system_code_old_to_new = {
    'CITY STREET': 'City Street', 
    'INTERSTATE': 'Interstate Highway', 
    'COUNTY ROAD': 'County Road', 
    'FRONTAGE ROAD': 'Frontage Road',
    'STATE HIGHWAY': 'State Highway', 
}


def convert_4digit_time_to_timestr(time_4digit):
    # convert the time format of '2359' to '23:59:00' 
    add_colons_and_seconds = time_4digit[0:2] + ':' + time_4digit[2:4] + ':00' 
    return add_colons_and_seconds

def convert_crash_time(df):
    #  convert handle nan values for manipulation
    df.loc[df['TIME'] == 'Not Applicable'] = np.nan
    df['TIME'] = df['TIME'].fillna(-1)
    # convert float time 2359.12 to a string '2359' which removes seconds information which is okay
    df['TIME_int_str'] = df['TIME'].astype(int).astype(str)
    # convert the string time '2359' to string '23:59:00' 
    df['Crash Time'] = df['TIME_int_str'].apply(lambda x: f"{x:04}").apply(convert_4digit_time_to_timestr)
    # add back in nans
    df.loc[df['Crash Time'].str.contains('-1')] = np.nan

    df = df.drop(['TIME'], axis=1)
    return df

def convert_location1_to_rd_number(LOC01):
    # convert Location 1 column to be formatted as expected for the Rd_Number column 

    # drop isolated numbers 
    # 1250 water st --> water st, but 23rd st stays the same
    drop_numbers = re.sub(r'\\d+\\s', '', str(LOC01))
    # drop single letters 
    # S main st --> main st 
    drop_single_letters = re.sub('\\s[a-z]\\s', '', drop_numbers)
    # split the remaining string and get the first 5 characters 
    split_list = drop_single_letters.split()
    if len(split_list) == 0:
        return np.nan
    else:
        get_first_word = split_list[0]
        first_word_first_five_letters_uppercase = get_first_word[0:5].upper()
        return first_word_first_five_letters_uppercase

def convert_road_number_and_section(df):

    # Populate the road number column (Rd_Number)
    # ************************************************
    # set Rd_Number to none since I'm not sure how to do these mappings
    df.loc[df['System Code'].isin(['City Street', 'County Road']), 'Rd_Number'] = np.nan

    # Rd_Number is the same as the old format RTE (with 3 digits) and the old format SEC
    # example: I-70 section A would be "070A" 
    df['RTE_3dig'] = df['RTE'].apply(lambda x: f"{x:03}")
    df['RTE_3dig_SEC'] = df['RTE_3dig'] + df['SEC']

    condition = df['System Code'].isin(['Interstate Highway', 'State Highway', 'Frontage Road'])
    df.loc[condition, 'Rd_Number'] = df.loc[condition, 'RTE_3dig_SEC']
    df = df.drop(['RTE_3dig', 'RTE_3dig_SEC', 'RTE', 'SEC'], axis=1) 

    # Populate the road section column (Rd_Section)
    # ************************************************
    # set Rd_Section to part of location 1 for City Street and County Road
    df['Location 1 converted to Rd_Section'] = df['Location 1'].apply(convert_location1_to_rd_number)
    condition = df['System Code'].isin(['City Street', 'County Road'])
    df.loc[condition, 'Rd_Section'] = df.loc[condition, 'Location 1 converted to Rd_Section']

    # Rd_Section is the mile marker (MP) for Highways and Frontage roads
    condition = df['System Code'].isin(['Interstate Highway', 'State Highway', 'Frontage Road'])
    df.loc[condition, 'Rd_Section'] = df.loc[condition, 'MP'].astype(str)

    df = df.drop(['MP', 'Location 1 converted to Rd_Section'], axis=1) 

    # Populate the city street (City_Street)
    # not sure how this mapping works so setting to NaN 
    df['City_Street'] = np.nan 

    return df
    


def convert_old_cdot_format_to_new_format(df):

    # Create columns that have no equivalent in old format 
    df['CUID'] = np.nan
    df['Fourth HE'] = np.nan
    df['Secondary Crash'] = np.nan
    df['Construction Zone'] = np.nan
    df['School Zone'] = np.nan
    df['Weather Condition 2'] = np.nan 
    df['Lane Position'] = np.nan 
    df['Record Status'] = np.nan 
    df['Processing Status'] = np.nan
    df['Last Updated'] = np.nan

    

    # Rename Columns 
    df = df.rename(
        columns={'DATE': 'Crash Date', 
                 'AGENCYNAME': 'Agency Id',
                 'CITY': 'City', 
                 'COUNTY': 'County', 
                 'LATITUDE': 'Latitude', 
                 'LONGITUDE': 'Longitude',
                 'LOC_01': 'Location 1', 
                 'LINK': 'Link', 
                 'LOC_02': 'Location 2',  
                 'INJURY 00': 'Injury 00', 
                 'INJURY 01': 'Injury 01', 
                 'INJURY 02': 'Injury 02', 
                 'INJURY 03': 'Injury 03',
                 'INJURY 04': 'Injury 04', 
                 'LOCATION': 'Location', 
                 'ROAD_DESC': 'Road Description',
                 'EVENT_1': 'First HE',
                 'EVENT_2': 'Second HE',
                 'EVENT_3': 'Third HE', 
                 'ACCTYPE': 'Crash Type',
                 'CONDITION': 'Road Condition',
                 'LIGHTING': 'Lighting Conditions',
                 'WEATHER': 'Weather Condition',
                 'VEHICLES': 'Total Vehicles',
                 'SYSTEM': 'System Code',
                 }
    )
    # rename manually wasn't working in the dictionary above
    df['Wild Animal'] = df['WAN_TYPE']

    # Map string values from old to new format 
    df['Location'] = df['Location'].map(map_location_old_to_new)
    df['Road Description'] = df['Road Description'].map(map_road_desc_old_to_new)
    df['First HE'] = df['First HE'].map(map_harmful_event_old_to_new)
    df['Second HE'] = df['Second HE'].map(map_harmful_event_old_to_new)
    df['Third HE'] = df['Third HE'].map(map_harmful_event_old_to_new)
    df['MHE'] = df['MHE'].map(map_harmful_event_old_to_new)
    df['Crash Type'] = df['Crash Type'].map(map_accident_type_old_to_new)
    df['Road Contour Curves'] = df['CONTOUR'].map(map_road_contour_curves_old_to_new)
    df['Road Contour Grade'] = df['CONTOUR'].map(map_road_contour_grade_old_to_new)
    df['Road Condition'] = df['Road Condition'].map(map_road_condition_old_to_new)
    df['Lighting Conditions'] = df['Lighting Conditions'].map(map_lighting_conditions_old_to_new)
    df['Weather Condition'] = df['Weather Condition'].map(map_weather_conditions_old_to_new)
    df['System Code'] = df['System Code'].map(map_system_code_old_to_new)

    # Cast 'Total Vehicles' to float 
    df['Total Vehicles'] = df['Total Vehicles'].astype(float)

    # Create 'Number Killed' and 'Number Injured' columns 
    df['Number Killed'] = df['Injury 04']
    df['Number Injured'] = df['Injury 01'] + df['Injury 02'] + df['Injury 03']

    # Approach Overtaking Turn 
    # get info from Crash Type
    df['Approach Overtaking Turn'] = np.nan
    df.loc[df['Crash Type'] == 'Approach Turn', 'Approach Overtaking Turn'] = 'Approach Turn'
    df.loc[df['Crash Type'] == 'Overtaking Turn', 'Approach Overtaking Turn'] = 'Overtaking Turn'
    df.loc[~df['Approach Overtaking Turn'].isin(['Approach Turn', 'Overtaking Turn']), 'Approach Overtaking Turn'] = 'Not Applicable'

    # Crash Time 
    df = convert_crash_time(df)

    # Rd_Number, Rd_Section, City_Street
    df = convert_road_number_and_section(df)

    # Drop no longer needed columns 
    df = df.drop([
        'CONTOUR', 
        'HAZMAT_1', 
        'HAZMAT_2', 
        'HAZMAT_3', 
        'VIOLCODE_1', 
        'VIOLCODE_2', 
        'VIOLCODE_3',
        'STATE_1', 
        'STATE_2',
        'STATE_3',
        'RAMP',
        'WAN_TYPE',
    ], axis=1)

    return df 
