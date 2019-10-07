import csv
from math import radians
from bound import bounding_rectangle, check_inside_bounding_rectangle
from distance import great_circle_distance

def sort_by_lat(elem):
    return elem['lat']

def sort_by_dist(elem):
    '''Sorting data by distance'''
    return elem['dist']

def get_profiles(lat, lon, distance, max_results=10):
    '''Gets profiles within the specified distance.

    Calculates the bounding box for the given geographic location and distance and returns a list of
    "profiles" from data.csv with specified number of results.

    Arguments:
    lat -- latitude in degrees
    lon -- longitude in degrees
    distance -- distance in Kms
    max_results -- number of results needed to be returned
    '''
    profiles = [] # result set
    min_lat, min_lon, max_lat, max_lon = bounding_rectangle(radians(lat), radians(lon), distance)

    with open('data.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rad_lat, rad_lon = radians(float(row['phi'])), radians(float(row['lambda']))
            # profiles appended only if they are within bounding box
            if check_inside_bounding_rectangle(
                    min_lat, min_lon, max_lat, max_lon,
                    rad_lat, rad_lon
                ):
                # get distance if inside bounding box
                dist = great_circle_distance(lat, lon, rad_lat, rad_lon)
                profiles.append({
                    'lat': float(row['phi']),
                    'long': float(row['lambda']),
                    'dist': dist,
                    'address': row['address']}
                )

    profiles.sort(key=sort_by_dist)

    return profiles[:max_results]

def main():
    with open('data.csv') as f:
        reader = csv.DictReader(f)
        profiles = []
        i = 0
        for row in reader:
            profiles.append({
                'lat': float(row['phi']),
                'long': float(row['lambda']),
                'address': row['address']}
            )
            i += 1
            if i > 100:
                break

    # print(profiles[:10])

    print('Sorting profiles based on latitude...')
    profiles.sort(key=sort_by_lat)

    print(profiles[:10])

if __name__ == '__main__':
    main()
