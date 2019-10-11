'''This module provides functions to make distance queries to a database.

Profiles are sorted based on closeness to query point.
'''
import os
from math import radians, degrees
import pymysql
from dotenv import load_dotenv
from bound import bounding_rectangle
from distance import great_circle_distance

load_dotenv()

# LAT_RAD = radians(61.21759217) # first lat in data.csv
# LON_RAD = radians(-149.8935557) # first lon in data.csv
# DIST = 10 # test dist in Kms

HOST = os.environ['DB_HOST']
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']
DATABASE = os.environ['DB_NAME']

TABLE = "profiles"

def get_profiles(lat, lon, distance=10, max_results=10, in_radians=False):
    '''Get profiles from MySQL database.
    
    Returning first 20 nearest profiles.
    '''
    # convert to radians if not already in radians
    if not in_radians:
        lat, lon = radians(lat), radians(lon)

    # result set
    profiles = []

    # get bounding box
    min_lat, min_lon, max_lat, max_lon = bounding_rectangle(lat, lon, distance)

    # create database connection
    con = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        db=DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )

    # form SQL statement
    sql = f"SELECT id, lat, lon FROM {TABLE} "
    sql += f"WHERE ({min_lat} <= lat AND lat <= {max_lat}) AND "
    sql += f"({min_lon} <= lon AND lon <= {max_lon})"

    with con:

        cur = con.cursor()

        # execute SQL and fetch result set
        cur.execute(sql)

        rows = cur.fetchall()

        for row in rows:

            # check if profile is within specified distance
            dist = great_circle_distance(lat, lon, row['lat'], row['lon'])

            if dist <= distance:

                profiles.append({
                    'id': int(row['id']),
                    'lat': degrees(row['lat']),
                    'lon': degrees(row['lon']),
                    'dist': dist,
                })

        profiles.sort(key=lambda elem: elem['dist'])

        return profiles[:max_results]
