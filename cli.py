from math import radians
from pprint import pprint
from data import get_profiles

def main():
    '''Taking input and showing output interactively.'''
    # taking user input in derees and converting into radians
    lat, lon = map(
        lambda inp: radians(float(inp)),
        input('Enter your latitude, longitude (in degrees): ').split(', ')
    )
    dist = float(input('Enter search distance (in Kms): '))

    profiles = get_profiles(lat, lon, dist, in_radians=True)

    print(f'Found {len(profiles)}!')
    pprint(profiles[:10])

if __name__ == '__main__':
    main()
