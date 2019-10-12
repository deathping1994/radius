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

def create_db_connection():
    '''Helper function to create database connection.

    Connection has to be closed by the calling function.
    '''
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        db=DATABASE,
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


def post_profileDB(lat, lon, in_radians=False):
    '''Post a profile, inserts new profile into MySQL database.
    
    Returns a valid profile_id if created successfully.
    '''
    # created profile, initially empty
    profile = {}

    # convert into radians if not already in radians
    if not in_radians:
        lat, lon = radians(lat), radians(lon)

    # create database connection
    connection = create_db_connection()

    # form SQL INSERT statement to create a new profile
    sql_INSERT = f"INSERT INTO {TABLE} (lat, lon) VALUES ({lat}, {lon})"

    # form SQL SELECT statement to retrieve newly created profile
    sql_SELECT = f"SELECT * FROM {TABLE} WHERE lat = {lat} AND lon = {lon}"

    try:
        with connection.cursor() as cursor:
            # execute SQL INSERT query
            cursor.execute(sql_INSERT)

        # commit changes to database table
        connection.commit()

        with connection.cursor() as cursor:
            #execute SQL SELECT query
            cursor.execute(sql_SELECT)

            # fetch result row
            row = cursor.fetchone()

            row_count = cursor.rowcount

            if row_count == 1:
                # if result row has 1 row (hopefully profile was created)
                profile = {
                    'id': row['id'],
                    'latitude': row['lat'],
                    'longitude': row['lon']
                }

    finally:
        # close connection
        connection.close()

    return profile


def get_profilesDB(profile_id, distance=10, max_results=10):
    '''Get profiles from MySQL database.
    
    Returning profiles sorted by distance.
    Arguments:
    profile_id -- profile near which distance query needs to be done
    distance -- query distance in kilometers
    '''
    # result set
    profiles = []

    # create database connection
    connection = create_db_connection()

    # form SQL to the latitude and longitude of the profile
    sql = f"SELECT lat, lon FROM {TABLE} WHERE id = {profile_id}"

    with connection.cursor() as cursor:
        # execute SQL SELECT query
        cursor.execute(sql)

        # fetch profile data
        row = cursor.fetchone()

        row_count = cursor.rowcount

    if row_count == 0:
        # returning if no profile with given profile_id exists
        return profiles

    lat, lon = row['lat'], row['lon']

    # get bounding box
    min_lat, min_lon, max_lat, max_lon = bounding_rectangle(
        lat, lon, distance
    )

    # create a new database connection to fetch nearby profiles
    connection = create_db_connection()

    # form SQL statement
    sql = f"SELECT id, lat, lon FROM {TABLE} "
    sql += f"WHERE ({min_lat} <= lat AND lat <= {max_lat}) AND "
    sql += f"({min_lon} <= lon AND lon <= {max_lon})"

    with connection.cursor() as cursor:

        # execute SQL SELECT query and fetch result set
        cursor.execute(sql)

        rows = cursor.fetchall()

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


def put_profileDB(profile_id, lat, lon, in_radians=False):
    '''Update a profile's location in the database table.'''
    # updated profile, initially empty
    profile = {}

    # convert to radians if not already in radians
    if not in_radians:
        lat, lon = radians(lat), radians(lon)

    # create database connection
    connection = create_db_connection()

    # form SQL UPDATE query to update profile
    sql_UPDATE = f"UPDATE {TABLE} SET lat = {lat}, lon = {lon}"
    sql_UPDATE += f"WHERE id = {profile_id}"

    # form SQL SELECT query to retrieve updated profile
    sql_SELECT = f"SELECT * FROM {TABLE} WHERE id = {profile_id}"

    try:
        with connection.cursor() as cursor:
            # execute SQL UPDATE query
            cursor.execute(sql_UPDATE)

            row_count = cursor.rowcount

            # if row_count == 0:
            #     # returning if no profile with given profile_id exists
            #     return profile

        # commit changes to database table
        connection.commit()

        with connection.cursor() as cursor:
            # execute SQL SELECT query
            cursor.execute(sql_SELECT)

            # fetch updated profile
            row = cursor.fetchone()

            row_count = cursor.rowcount

            if row_count == 1:
                # returning if no profile with given profile_id exists
                profile = {
                    'id': row['id'],
                    'latitude': row['lat'],
                    'longitude': row['lon']
                }

    finally:
        # close connection
        connection.close()

    return profile


def delete_profileDB(profile_id):
    '''Delete a profile from the database table.'''
    # create database connection
    connection = create_db_connection()

    # form SQL DELETE query to remove profile from database table
    sql_DELETE = f"DELETE FROM {TABLE} WHERE id = {profile_id}"

    try:
        with connection.cursor() as cursor:
            # execute SQL DELETE query
            cursor.execute(sql_DELETE)

            row_count = cursor.rowcount

            if row_count == 0:
                # returning if no profile with given profile_id exists
                return False

        # commit changes to database table
        connection.commit()

    finally:
        # close connection
        connection.close()

    return True
