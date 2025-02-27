# This file contains utility functions for converting CDOT crash data from the 2007-2020 data format 
# to the 2021+ data format. 

import numpy as np 



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
                 'WAN_TYPE': 'Wild Animal', 
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
                 'LIGHTING': 'Lighting Condition',
                 'WEATHER': 'Weather Condition',
                 }
    )


    # Map string values from old to new format 
    df['Location'] = df['Location'].map(map_lighting_conditions_old_to_new)
    df['Road Description'] = df['Road Description'].map(map_road_desc_old_to_new)
    df['First HE'] = df['First HE'].map(map_harmful_event_old_to_new)
    df['Second HE'] = df['Second HE'].map(map_harmful_event_old_to_new)
    df['Third HE'] = df['Third HE'].map(map_harmful_event_old_to_new)
    df['MHE'] = df['MHE'].map(map_harmful_event_old_to_new)
    df['Crash Type'] = df['Crash Type'].map(map_accident_type_old_to_new)
    df['Road Contour Curves'] = df['CONTOUR'].map(map_road_contour_curves_old_to_new)
    df['Road Contour Grade'] = df['COUNTOUR'].map(map_road_contour_grade_old_to_new)
    df['Road Condition'] = df['Road Condition'].map(map_road_condition_old_to_new)
    df['Lighting Condition'] = df['Lighting Conditions'].map(map_lighting_conditions_old_to_new)
    df['Weather Condition'] = df['Weather Condition'].map(map_weather_conditions_old_to_new)

    # write utility functions for the following 

        # Approach Overtaking Turn 

        # Number Killed 
        # Number Injured 
        # use new names 

        # Total Vehicles 

        # System Code, Rd_Number, Rd_Section, City_Street
        # call function 

        # Crash Time

    # Drop no longer needed columns 
    df.drop(['COUNTOUR'])

    return df 
