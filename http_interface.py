# from data import get_profiles
from database import get_profiles
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the http interface for <i><b>radius!</b></i>'

@app.route('/profiles', methods=['GET'])
def profiles():
    '''GET nearby profiles.

    Only GET method for now.

    Arguments:
    lat -- latitude in degrees, centre of search circle
    lon -- longitude in degrees, centre of search circle
    dist -- search distance in Kms
    '''
    lat = float(request.args['lat'])
    lon = float(request.args['lon'])
    dist = request.args.get('dist') # dist not required
    # print(lat, lon, dist)
    if dist is None:
        profiles = get_profiles(lat, lon)
    else:
        profiles = get_profiles(lat, lon, float(dist))
    # profiles = get_profiles()
    return jsonify({'profiles': profiles})

if __name__ == '__main__':
    app.run(debug=True)
