'''This module finds the great circle distance for two given geographic points.'''
from math import cos, sin, radians, acos

EARTH_RADIUS = 6371.0088 # in kms

# phi - latitude, lmbda - longitude (lambda)
def n_vector(phi, lmbda):
    '''Convert a geographic coordinate (in radians) into n-vector representation and return as a list.'''
    n = (cos(phi) * cos(lmbda), cos(phi) * sin(lmbda), sin(phi))

    return n

def dot_product(vector1, vector2):
    '''Return algebraic dot product of two vectors as a scalar.'''
    dot = 0
    for i, j in zip(vector1, vector2):
        dot += i * j

    return dot

def great_circle_distance(phi1, lmbda1, phi2, lmbda2):
    '''Returns the great circle distance in Kms.

    Coordinates are converted into n-vector representation. Both vectors are then dotted and the
    inverse cosine is taken to get the angular distance. Finally, it is then multiplied by the
    Earth's radius to get the radial distance (in Kms).

    Arguments:
    phi1 -- first latitude
    lmbda1 -- first longitude
    phi2 -- second latitude
    lmbda2 -- second longitude

    Wikipedia article for great circle distance:
    https://en.wikipedia.org/wiki/Great-circle_distance
    '''
    n_vector1 = n_vector(phi1_rad, lmbda1_rad)
    n_vector2 = n_vector(phi2_rad, lmbda2_rad)
    dot = dot_product(n_vector1, n_vector2)

    delta_sigma = acos(dot)
    approx_distance = EARTH_RADIUS * delta_sigma

    return approx_distance

def main():
    '''Takes input and displays output interactively.'''
    # convert degrees into radians
    phi1, lmbda1 = map(lambda x: radians(float(x)), input('Enter first latitude, longitude: ').split(', '))
    phi2, lmbda2 = map(lambda x: radians(float(x)), input('Enter second latitude, longitude: ').split(', '))

    n_vector1 = n_vector(phi1, lmbda1)
    n_vector2 = n_vector(phi2, lmbda2)

    print('n-vector representation of first geographic position:')
    print(n_vector1)
    print('n-vector representation of second geographic position:')
    print(n_vector2)

    dot = dot_product(n_vector1, n_vector2)

    print(f'Dot product of n-vectors: {dot}')

    delta_sigma = acos(dot) # angular distance (in radians) between the two points

    print('Angular distance between first and second geographic positions(rads):')
    print(delta_sigma)

    approx_distance = EARTH_RADIUS * delta_sigma # radial distance (in kms)

    print('Approximate distance between first and second geographic positions(Kms):')
    print(approx_distance)

if __name__ == '__main__':
    main()
