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

map_helmet_x_old_to_new = {
    'NONE': 'No Helmet',
    'EYE PROTECTION ONLY': 'old__eye_protection_only',
    'BICYCLE HELMET (BICYCLE ONLY)': 'old__bicycle_helmet_bicycle_only',
    'HELMET AND EYE PROTECTION': 'old__helmet_and_eye_protection',
    'HELMET ONLY': 'old__helmet_only',
}

map_belt_x_old_to_new = {
    'Y': 'old__yes',
    'N': 'old__no',
}

map_human_factor_x_old_to_new = {
    'NO APPARENT CONTRIBUTING FACTOR': 'No Apparent Contributing Factor',
    'UNKNOWN': np.nan,
    'DRIVER UNFAMILIAR WITH AREA': 'Driver Unfamiliar With Area',
    'DRIVER PREOCCUPIED':'Distracted',
    'DRIVER INEXPERIENCE': 'Driver Inexperience',
    'DRIVER FATIGUE': 'Asleep or Fatigued',
    'ASLEEP AT WHEEL': 'Asleep at the wheel',
    'ILLNESS': 'Illness',
    'DRIVER EMOTIONALLY UPSET': 'Driver Emotionally Upset',
    'DISTRACTED BY PASSENGER': 'Distracted/Other Occupant',
    'EVADING LAW ENFORCEMENT OFFICER': 'Evading Law Enforcement Officer',
    'PHYSICAL DISABILITY': 'Physical Disability',
}

map_movement_x_old_to_new = {
    'BACKING': 'Backing',
    'OTHER': 'Other (Describe in Narrative)',
    'AVOIDING OBJECT/VEHICLE IN ROAD': 'Swerve/Avoidance',
    'CHANGING LANES': 'Changing Lanes',
    'GOING STRAIGHT': 'Going Straight',
    'ENTERING/LEAVING PARKED POSITION': 'Entering/Leaving Parked Position',
    'PASSING': 'Passing',
    'MAKING LEFT TURN': 'Making Left Turn',
    'SLOWING': 'Slowing',
    'WEAVING': 'Weaving',
    'MAKING U-TURN': 'Making U-Turn',
    'MAKING RIGHT TURN': 'Making Right Turn',
    'PARKED': 'Parked',
    'STOPPED IN TRAFFIC': 'Stopped in Traffic',
    'WRONG WAY': 'Traveled Wrong Way',
    'UNKNOWN': np.nan,
}

map_direction_x_old_to_new = {
    'S': 'South', 
    'N': 'North',
    'W': 'West',
    'UK': 'Unknown',
    'E': 'East',
    'SE': 'Southeast',
    'NW': 'Northwest',
    'NE': 'Northeast',
    'SW': 'Southwest',
}

map_vehicle_to_tu_type_x = {'HIT & RUN - UNKNOWN': 'Unknown', 
                 'UNKNOWN': 'Unknown',
                 'PICKUP TRUCK/UTILITY VAN': 'Pickup Truck/Utility Van', 
                 'PASSENGER CAR/VAN': 'Passenger Car/Passenger Van', 
                 'SUV': 'SUV', 
                 'MOTORCYCLE': 'Motorcycle', 
                 'PASSENGER CAR/VAN W/TRAILER': 'Passenger Car/Passenger Van with Trailer - RET',
                 'SCHOOL BUS < 15 PEOPLE': 'School Bus (all school buses)',
                 'FARM EQUIPMENT': 'Farm Equipment',
                 'MOTOR HOME': 'Motor Home',
                 'TRUCK GVW > 10K/BUSSES > 15 PEOPLE': 'old__truck_gvw_gr_10k_busses_gr_15_people',
                 'SUV W/TRAILER': 'old__SUV_w_trailer',
                 'PICKUP TRUCK/UTILITY VAN W/TRAILER': 'old__pickup_truck_utility_van_w_trailer',
                 'NON-SCHOOL BUS < 15 PEOPLE': '',
                 'OTHER - SEE REPORT': 'Other Vehicle Type (Describe in Narrative)',
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

def determine_motorists_vs_non_motorists(df):
    # Determine for each traffic unit (i.e. VEHICLE_X) whether they are a motorist or non-motorist
    # Identify which VEHICLE_X columns need to be converted to NM columns in new format 

    for x in [1, 2, 3]:
        # initialize columns
        df[f"TU-{x} Type"] = ''
        df[f"TU-{x} NM Type"] = ''
        df[f"vehicle_{x}_is_nm"] = False

        # When the accident type is Pedestrian the vast majority of the time the "VEHICLE_X" column that says "OTHER - SEE REPORT" is referring to a pedestrian 
        # there are a handful of accidents that have multiple "VEHICLE_X" columns that say "OTHER - SEE REPORT" so it is ambiguous which X is the pedestrian 
        df.loc[(df['ACCTYPE'] == 'PEDESTRIAN') & (df[f"VEHICLE_{x}"] == 'OTHER - SEE REPORT'), f"vehicle_{x}_is_nm"] = True 
        df.loc[(df['ACCTYPE'] == 'PEDESTRIAN') & (df[f"VEHICLE_{x}"] == 'OTHER - SEE REPORT'), f"TU-{x} NM Type"] = 'Pedestrian'

        # Old format has Bicycle as a type of vehicle, so filter for VEHICLE_X == BICYCLE or MOTORIZED BICYCLE, then slot those in as non-motorists 
        # accident type isn't always bicycle when a bicycle is involved 
        df.loc[(df[f"VEHICLE_{x}"] == 'BICYCLE') | (df[f"VEHICLE_{x}"] == 'MOTORIZED BICYCLE'), f"vehicle_{x}_is_nm"] = True
        df.loc[df[f"VEHICLE_{x}"] == 'BICYCLE', f"TU-{x} NM Type"] = 'Bicyclist'
        df.loc[df[f"VEHICLE_{x}"] == 'MOTORIZED BICYCLE', f"TU-{x} NM Type"] = 'Other Bicyclist/Cyclist'

        # Convert VEHICLE_X to TU-X Type - when VEHICLE_X is a motorist 
        # don't map bicycle or motorized bicycle since they will always be mapped to non-motorists 

        # In the new data format, if the accident is between a motorist and a non-motorist
        # there is no re-use of the 1, 2 numbers 
            # TU-1 Type = Null 
            # TU-2 Type = SUV
            # TU-1 NM = Pedestrian
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Type"] = df[f"VEHICLE_{x}"].map(map_vehicle_to_tu_type_x)

    return df


def convert_tu_metadata(df):
    # Based on motorist or non-motorist for each traffic unit, convert 
    # direction, movement, hit and run, speed limit, estimated speed, human contributing factor
    # age, sex, safety restraint use, safety helpmet, alcohol suspected, marijuana suspected, 
    # and other drugs suspected 
    # Initialize all NM and Motorist columns to empty strings 
    # add a third vehicle and non-motorist to map VEHICLE_3 to from old format 

    for x in ['1', '2', '3']:
        # handle inconsistent column naming
        if x == '1':
            sex_col = f"TU-{x} Sex "
            safety_helmet_col = f"TU-{x} Safety Helmet"
            marijuana_suspected_col = f"TU-{x}  Marijuana Suspected"
        elif x == '2':
            sex_col = f"TU-{x} Sex" 
            safety_helmet_col = f"TU-{x}  Safety Helmet"
            marijuana_suspected_col = f"TU-{x} Marijuana Suspected"
        else:
            sex_col = f"TU-{x} Sex"
            safety_helmet_col = f"TU-{x} Safety Helmet"
            marijuana_suspected_col = f"TU-{x} Marijuana Suspected"

        people_columns = [
            f"TU-{x} Direction",
            f"TU-{x} Movement",
            f"TU-{x} Speed Limit",
            f"TU-{x} Estimated Speed",
            f"TU-{x} Human Contributing Factor",
            f"TU-{x} Age",
            f"TU-{x} Safety restraint Use",
            f"TU-{x} Alcohol Suspected",
            f"TU-{x} Other Drugs Suspected ",
            f"TU-{x} NM Direction",
            f"TU-{x} NM Movement",
            f"TU-{x} NM Age ",
            f"TU-{x} NM Sex ",
            f"TU-{x} NM Human Contributing Factor ",
            f"TU-{x} NM Safety Helmet ",
            f"TU-{x} NM Alcohol Suspected ",
            f"TU-{x} NM Marijuana Suspected ",
            f"TU-{x} NM Other Drugs Suspected ",
        ] + [sex_col + safety_helmet_col + marijuana_suspected_col]
        for col_name in people_columns:
            df[col_name] = ''
        

        # direction
        df.loc[df[f"vehicle_{x}_is_nm"] == True, f"TU-{x} NM Direction"] = df[f"DIR_{x}"].map(map_direction_x_old_to_new)
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Direction"] = df[f"DIR_{x}"].map(map_direction_x_old_to_new)

        # movement
        df.loc[df[f"vehicle_{x}_is_nm"] == True, f"TU-{x} NM Movement"] = df[f"VEH_MOVE_{x}"].map(map_movement_x_old_to_new)
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Movement"] = df[f"VEH_MOVE_{x}"].map(map_movement_x_old_to_new)

        # hit and run (only for motorists)
        condition_hit_and_run__true = (df[f"vehicle_{x}_is_nm"] == False) & (df[f"VEHICLE_{x}"] == "HIT & RUN - UNKNOWN")
        condition_hit_and_run__false = (df[f"vehicle_{x}_is_nm"] == False) & (df[f"VEHICLE_{x}"] != "HIT & RUN - UNKNOWN")
        df.loc[condition_hit_and_run__true, f"TU-{x} Hit And Run"] = True
        df.loc[condition_hit_and_run__false, f"TU-{x} Hit And Run"] = False

        # speed limit (only for motorists)
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Speed Limit"] = df[f"LIMIT{x}"].replace('UK', '-1').astype(int).replace(-1, np.nan)

        # estimated speed (only for motorists)
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Estimated Speed"] = df[f"SPEED_{x}"] \
                                        .replace('UK', '-1') \
                                        .replace(np.nan, '-1').str.replace(r'^0+(?!\s*$)', '', regex=True) \
                                        .astype('int').replace(-1, np.nan)

        # human contributing factor
        df.loc[df[f"vehicle_{x}_is_nm"] == True, f"TU-{x} NM Human Contributing Factor "] = df[f"FACTOR_{x}"].map(map_human_factor_x_old_to_new)
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Human Contributing Factor"] = df[f"FACTOR_{x}"].map(map_human_factor_x_old_to_new)

        # Age
        df.loc[df[f"vehicle_{x}_is_nm"] == True, f"TU-{x} NM Age "] = df[f"AGE_{x}"]
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Age"] = df[f"AGE_{x}"]

        # Sex
        df.loc[df[f"vehicle_{x}_is_nm"] == True, f"TU-{x} NM Sex"] = df[f"SEX_{x}"]
        df.loc[df[f"vehicle_{x}_is_nm"] == False, sex_col] = df[f"SEX_{x}"]

        # Safety restraint use (only for motorists)
        df.loc[df[f"vehicle_{x}_is_nm"] == False, f"TU-{x} Safety restraint Use"] = df[f"BELT_{x}"].map(map_belt_x_old_to_new)

        # safety helmet
        df.loc[df[f"vehicle_{x}_is_nm"] == True, f"TU-{x} NM Safety Helmet "] = df[f"CYCPROT_{x}"].map(map_helmet_x_old_to_new)
        df.loc[df[f"vehicle_{x}_is_nm"] == False, safety_helmet_col] = df[f"CYCPROT_{x}"].map(map_helmet_x_old_to_new)

        # Alcohol, Marijuana, Other Drugs
        # *********************************************************************
        condition_motorist = df[f"vehicle_{x}_is_nm"] == False
        condition_non_motorist = df[f"vehicle_{x}_is_nm"] == True
        condition_no_impairment = df[f"DRIVER_{x}"] == 'NO IMPAIRMENT SUSPECTED'
        condition_alcohol_involved = df[f"DRIVER_{x}"] == 'ALCOHOL INVOLVED'
        condition_alcohol_drugs = df[f"DRIVER_{x}"] == 'ALCOHOL/DRUGS'
        condition_rx_med_drugs = df[f"DRIVER_{x}"] == 'RX/MEDICATION/DRUGS'

        # No Impairment 
        # OLD: NO IMPAIRMENT SUSPECTED 
        # --> NEW Alcohol Suspected - "No" 
        # --> NEW Marijuana Suspected - "Marijuana Not Suspected"
        # --> NEW Other Drugs Suspected - "No" 
        df.loc[condition_non_motorist & condition_no_impairment, f"TU-{x} NM Alcohol Suspected "] = "No"
        df.loc[condition_non_motorist & condition_no_impairment, f"TU-{x} NM Marijuana Suspected "] = 'Marijuana Not Suspected'
        df.loc[condition_non_motorist & condition_no_impairment, f"TU-{x} NM Other Drugs Suspected "] = "No"

        df.loc[condition_motorist & condition_no_impairment, f"TU-{x} Alcohol Suspected"] = "No"
        df.loc[condition_motorist & condition_no_impairment, marijuana_suspected_col] = 'Marijuana Not Suspected'
        df.loc[condition_motorist & condition_no_impairment, f"TU-{x} Other Drugs Suspected "] = "No"

        # Alcohol Involved 
        # OLD: ALCOHOL INVOLVED 
        # --> New Alcohol Suspected - "Yes" 
        # --> NEW Marijuana Suspected - "Unknown"
        # --> NEW Other Drugs Suspected - "Unknown" 
        df.loc[condition_non_motorist & condition_alcohol_involved, f"TU-{x} NM Alcohol Suspected "] = "Yes"
        df.loc[condition_non_motorist & condition_alcohol_involved, f"TU-{x} NM Marijuana Suspected "] = 'Unknown'
        df.loc[condition_non_motorist & condition_alcohol_involved, f"TU-{x} NM Other Drugs Suspected "] = "Unknown"

        df.loc[condition_motorist & condition_alcohol_involved, f"TU-{x} Alcohol Suspected"] = "Yes"
        df.loc[condition_motorist & condition_alcohol_involved, marijuana_suspected_col] = 'Unknown'
        df.loc[condition_motorist & condition_alcohol_involved, f"TU-{x} Other Drugs Suspected "] = "Unknown"

        # Alcohol / Drugs 
        # OLD: ALCOHOL/DRUGS 
        # --> New Alcohol Suspected - "old__alcohol_drugs" 
        # --> NEW Marijuana Suspected - "old__alcohol_drugs"
        # --> NEW Other Drugs Suspected - "old__alcohol_drugs"
        df.loc[condition_non_motorist & condition_alcohol_drugs, f"TU-{x} NM Alcohol Suspected "] = "old__alcohol_drugs"
        df.loc[condition_non_motorist & condition_alcohol_drugs, f"TU-{x} NM Marijuana Suspected "] = 'old__alcohol_drugs'
        df.loc[condition_non_motorist & condition_alcohol_drugs, f"TU-{x} NM Other Drugs Suspected "] = "old__alcohol_drugs"

        df.loc[condition_motorist & condition_alcohol_drugs, f"TU-{x} Alcohol Suspected"] = "old__alcohol_drugs"
        df.loc[condition_motorist & condition_alcohol_drugs, marijuana_suspected_col] = 'old__alcohol_drugs'
        df.loc[condition_motorist & condition_alcohol_drugs, f"TU-{x} Other Drugs Suspected "] = "old__alcohol_drugs"

        # RX/MEDICATION/DRUGS
        # OLD: RX/MEDICATION/DRUGS 
        # --> New Alcohol Suspected - "No" 
        # --> NEW Marijuana Suspected - "old__rx_medication_drugs"
        # --> NEW Other Drugs Suspected - "old__rx_medication_drugs"
        df.loc[condition_non_motorist & condition_alcohol_drugs, f"TU-{x} NM Alcohol Suspected "] = "No"
        df.loc[condition_non_motorist & condition_alcohol_drugs, f"TU-{x} NM Marijuana Suspected "] = 'old__rx_medication_drugs'
        df.loc[condition_non_motorist & condition_alcohol_drugs, f"TU-{x} NM Other Drugs Suspected "] = "old__rx_medication_drugs"

        df.loc[condition_motorist & condition_alcohol_drugs, f"TU-{x} Alcohol Suspected"] = "No"
        df.loc[condition_motorist & condition_alcohol_drugs, marijuana_suspected_col] = 'old__rx_medication_drugs'
        df.loc[condition_motorist & condition_alcohol_drugs, f"TU-{x} Other Drugs Suspected "] = "old__rx_medication_drugs"

    return df


def convert_old_cdot_format_to_new_format(df):

    # Create columns that have no equivalent in old format 
    # some column names have spaces at the end 
    nan_columns = [
        'CUID', 
        'Fourth HE', 
        'Secondary Crash', 
        'Construction Zone', 
        'School Zone', 
        'Weather Condition 2',
        'Lane Position',
        'Record Status',
        'Processing Status', 
        'Last Updated', 
        'TU-1 Special Function',
        'TU-2 Special Function', 
        'TU-3 Special Function',
        'TU-1 Autonomous Vehicle', 
        'TU-2 Autonomous Vehicle', 
        'TU-3 Autnomous Vehicle',
        'TU-1 Speed',
        'TU-2 Speed', 
        'TU-3 Speed', 
        'TU-1 Driver Action', 
        'TU-2 Driver Action', 
        'TU-3 Driver Action', 
        'TU-1 Safety System Available ', 
        'TU-2 Safety System Available ', 
        'TU-3 Safety System Avaliable ', 
        'TU-1 NM Facility Available', 
        'TU-2 NM Facility Available',
        'TU-3 NM Facility Available',
        'TU-1 NM Location ', 
        'TU-2 NM Location ', 
        'TU-3 NM Location ',
        'TU-1 NM Action ',
        'TU-2 NM Action ',
        'TU-3 NM Action ',
    ]
    for nc in nan_columns:
        df[nc] = np.nan

    # Determine if entity (traffic unit) 1, 2, 3 are motorists or non-motorists
    # Define TU-X Type and TU-X NM Type 
    df = determine_motorists_vs_non_motorists(df)
    # convert metadata columns based on motorist / non-motorist
    df = convert_tu_metadata(df)
    
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
        'DUI_1', 
        'DUI_2', 
        'DUI_3',
        'SEVERITY',
        'DRVINJ_1', 
        'DRVINJ_2', 
        'DRVINJ_3',
        'vehicle_1_is_nm', 
        'vehicle_2_is_nm', 
        'vehicle_3_is_nm',
        'VEHICLE_1',
        'VEHICLE_2', 
        'VEHICLE_3', 
        'LIMIT1', 
        'LIMIT2', 
        'LIMIT3', 
        'REGION', 
        'RUCODE', 
        'DIR_1', 
        'DIR_2', 
        'DIR_3', 
        'DRIVER_1', 
        'DRIVER_2', 
        'DRIVER_3', 
        'FACTOR_1', 
        'FACTOR_2', 
        'FACTOR_3', 
        'SPEED_1', 
        'SPEED_2', 
        'SPEED_3', 
        'VEH_MOVE_1', 
        'VEH_MOVE_2', 
        'VEH_MOVE_3', 
        'AGE_1', 
        'AGE_2', 
        'AGE_3', 
        'SEX_1', 
        'SEX_2', 
        'SEX_3', 
        'BELT_1', 
        'BELT_2', 
        'BELT_3', 
        'CYCPROT_1', 
        'CYCPROT_2', 
        'CYCPROT_3', 
        'TIME_int_str', 
    ], axis=1)

    return df 
