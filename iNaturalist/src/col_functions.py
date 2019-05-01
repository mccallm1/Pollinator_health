from __future__ import print_function
import os
import sys
import elevation
import json
import requests

def test_import():
    print("col_functions.py test")

# 'Eval' functions are called from the merge_tables function to evaluate the
# contents of each column for the output spreadsheet. For each row in the
# original table, each eval function is called sequentially to construct the
# desired output row.

# I chose to encapsulate each column value in its own eval function to make
# the interpretation of input data as modular as possible. Each eval function
# uses potentially different logic to generate properly formatted output values,
# and each function can be modified independently.

def collector_name(in_file, user_name):
    # Open usernames CSV
    with open(in_file,'r') as file:
        for row in file:
            # Remove trailing characters and split line into array
            row = row.rstrip("\r\n")
            row = row.split(',')
            # Found a match...
            if row[1] == user_name:
                # First name: 1st word of column 1
                first_name = row[0].split(' ')[0]
                # First letter of the first name
                first_initial = first_name[0] + '.'
                # Last name: 2nd word of column 1
                last_name = row[0].split(' ')[1]
                #Done
                return first_name, first_initial, last_name
    return "","",""

def date_1(in_date):
    # Check input
    if in_date == '':
        return '','',''
    # Init vars
    in_date = in_date.split('/')
    month_numeral = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XIII']
    # Parse values from full date string
    day = in_date[1]
    # Reference numeral array
    month = month_numeral[int(in_date[0]) - 1]
    year = in_date[2]
    return day, month, year

def time_1(in_time):
    # Check input
    if in_time == '':
        return ''
    # Split full time string to remove date (1st word)
    in_time = in_time.split(' ')
    # Split time word by : to separate hours, mins, secs
    return_time = in_time[1].split(':')
    # Reattach the hours and minutes, leaving out seconds
    return_time = return_time[0] + ":" + return_time[1]
    return return_time

def date_2(in_date):
    # Check input
    if in_date == '':
        return '','','',''
    # Init vars
    month_numeral = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XIII']

    in_date = in_date.split('T')
    # There are several input formats for this col
    # If the format can be split with T continue:
    if len(in_date) == 2:
        #print("Splitting with T...")
        in_date = in_date[0].split('-')
        # Parse values from full date string
        day = in_date[2]
        # Reference numeral array
        month = month_numeral[int(in_date[1]) - 1]
        # Year is straight forward
        year = in_date[0]
        # Calculate merge string
        merge = "-" + day + month
    else:
        #print("Splitting without T...")
        in_date = in_date[0].split(' ')
        in_date = in_date[0].split('/')
        # Parse values from full date string
        day = in_date[0]
        # Reference numeral array
        month = month_numeral[int(in_date[1]) - 1]
        # Year is straight forward
        year = in_date[2]
        # Calculate merge string
        merge = "-" + day + month

    return day, month, year, merge

def time_2(in_time):
    # Check input
    if in_time == '':
        return ''

    # Split full time string to remove date (1st word)
    in_time = in_time.split('T')

    if len(in_time) == 2:
        #print("Splitting with T...")
        in_time = in_time[1].split(':')
        in_time = in_time[0] + ":" + in_time[1]
    else:
        #print("Splitting without T...")
        in_time = in_time[0].split(' ')
        in_time = in_time[1]

    return in_time

def location_guess(address, cities_file):
    #print("raw:",address)

    address = address.split(", ")
    #print("split on comma:",address)

    # If 'normal' address, should split in 4
    if len(address) == 4:
        #print("guess:",address[1])
        return address[1]
    else:
        #print("unusual format...")
        return ""

def specimen_id(specimen_id_str):
    if specimen_id_str is None:
        return " "
    if specimen_id_str != '':
        if specimen_id_str[0].isalpha():
            return "NOT INT"
        else:
            return specimen_id_str


def round_coord(coord):
    temp = '%.4f'%(float(coord))
    if len(temp.split('.')[1]) < 4:
        print("coordinate didn't have 4 digits:",temp)
        temp = float(str(temp) + "0")
        print("fixed(?):",temp)
        sys.exit()
    return temp


def

def elevation(lat, long):
    apikey = "AIzaSyBoc369wPHoc2R3fKHBSiIh4iwIY4qk7P4"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = requests.get(url+"?locations="+str(lat)+","+str(long)+"&key="+apikey)
    try:
        results = json.loads(request.text).get('results')
        if 0 < len(results):
            elevation = results[0].get('elevation')
            #resolution = results[0].get('resolution') # for RESOLUTION
            # ELEVATION
            return elevation
        else:
            print('HTTP GET Request failed.')
    except ValueError as e:
        print('JSON decode failed: '+str(request) + str(e))

def elevation_from_coords(lat,long):
    # Bottom Left: 41 N 124 W
    # Bottom Right: 41 N 116 W
    # Top Left: 46 N 124 W
    # Top Right: 46 N 116 W

    print("Calculating elevation...")
    # clip the SRTM1 30m DEM of Rome and save it to Rome-DEM.tif
    elevation.clip(bounds=(41, 116, 42, 117), output='./Oregon-DEM.tif')
    # clean up stale temporary files and fix the cache in the event of a server error
    #elevation.clean()
    print("saved test in file")
