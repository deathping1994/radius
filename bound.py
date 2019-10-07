'''This module finds the bounding rectangle coordinates for a given geographic point and distance.'''
from math import cos, sin, radians, asin, pi, degrees

EARTH_RADIUS = 6371.0088 # in kms

# phi - latitude, lmbda - longitude
def check_poles_or_180th_meridian(phi_min, lmbda_min, phi_max, lmbda_max):
    '''Checks if the bounding rectangle includes either poles or the 180th meridian,
    and returns modified bounding coordinates.

    Arguments:
    phi_min -- minimum latitude in radians
    lmbda_min -- minimum longitude in radians
    phi_max -- maximum latitude in radians
    lmbda_max -- maximum longitude in radians
    '''

    # if maximum latitude is greater than pi/2, parts of all meridians at North pole are within the bounding rectangle
    if phi_max > pi / 2:
        phi_min = phi_min
        lmbda_min = (-1) * pi

        phi_max = pi / 2
        lmbda_max = pi

    # if minimum latutide is less than -pi/2, parts of all meridians at South pole are within the bounding rectangle
    elif phi_min < (-1) * pi / 2:
        phi_min = (-1) * pi / 2
        lmbda_min = (-1) * pi

        phi_max = phi_max
        lmbda_max = pi

    # if any one of minimum or maximum longitudes are outside [-pi, pi], the 180th meridian is within the bounding rectangle
    elif lmbda_min < (-1) * pi or lmbda_max > pi:
        phi_min = phi_min
        lmbda_min = (-1) * pi

        phi_max = phi_max
        lmbda_max = pi

    return (phi_min, lmbda_min, phi_max, lmbda_max)

def bounding_rectangle(phi, lmbda, distance):
    '''For a given latitude and longitude (in radians) and distance (in Kms), finds the
    bounding rectangle that includes the circle including all points within that distance from
    given geographic coordinate.

    Arguments:
    phi -- latitude in radians
    lmbda -- longitude in radians
    distance -- radius of the circle around the latitude and longitude in Kms

    Reference article:
    http://janmatuschek.de/LatitudeLongitudeBoundingCoordinates
    '''
    angular_distance = distance / EARTH_RADIUS

    # fixing the longitude, minimum and maximum latitudes may be found by simply subtracting and
    # adding the angular distance that is made when moving on the earth between two points having
    # specified distance
    phi_min = phi - angular_distance
    phi_max = phi + angular_distance

    # calculating minimum and maximum longitudes is not as simple as it is for finding the bounding latitudes
    # the following formulae are found in a good math handbook
    # https://www.amazon.co.uk/Handbook-Mathematics-I-N-Bronshtein/dp/3662462206/ref=sr_1_fkmr3_2?keywords=Handbook+of+Mathematics+Paperback+%E2%80%93+24+Aug+2007&qid=1570284856&s=books&sr=1-2-fkmr3
    phi_t = asin(sin(phi)/cos(angular_distance))
    delta_lmbda = asin(sin(angular_distance) / cos(phi))

    # then simply subtract and add delta_lmbda to find minimum and maximum longitudes
    lmbda_min = lmbda - delta_lmbda
    lmbda_max = lmbda + delta_lmbda

    # check for poles or 180th meridian
    phi_min, lmbda_min, phi_max, lmbda_max = check_poles_or_180th_meridian(phi_min, lmbda_min, phi_max, lmbda_max)

    return (phi_min, lmbda_min, phi_max, lmbda_max)

def check_inside_bounding_rectangle(phi_min, lmbda_min, phi_max, lmbda_max, phi, lmbda):
    '''Checks if a geopgraphic location is inside the calculated bounding rectangle and returns a Boolean.'''
    if phi_min <= phi and phi <= phi_max and lmbda_min <= lmbda and lmbda <= lmbda_max:
        return True
    else:
        return False

def main():
    '''Takes input and displays output interactively.'''
    phi1, lmbda1 = map(lambda x: radians(float(x)), input('Enter latitude, longitude: ').split(', '))
    distance = float(input('Enter distance(Kms): '))

    # get bounding rectangle
    phi_min, lmbda_min, phi_max, lmbda_max = bounding_rectangle(phi1, lmbda1, distance)

    # phi_min = degrees(phi_min)
    # lmbda_min = degrees(lmbda_min)

    # phi_max = degrees(phi_max)
    # lmbda_max = degrees(lmbda_max)

    # convert back to degrees
    bounding_coordinates = ((degrees(phi_min), degrees(lmbda_min)), (degrees(phi_max), degrees(lmbda_max)))

    print(f'Bounding coordinates for ({degrees(phi1)}, {degrees(lmbda1)}):')
    print(bounding_coordinates)

    phi2, lmbda2 = map(lambda x: radians(float(x)), input('Enter another latitude, longitude: ').split(', '))

    if check_inside_bounding_rectangle(phi_min, lmbda_min, phi_max, lmbda_max, phi2, lmbda2):
        print(f'Position within {distance} Kms of ({degrees(phi1)}, {degrees(lmbda1)})!')
    else:
        print('Position outside bounding rectangle.')

if __name__ == '__main__':
    main()
