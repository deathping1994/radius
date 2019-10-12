'''This module implements the various API end-points for radius.'''
from database import (
    post_profileDB, get_profilesDB, put_profileDB, delete_profileDB
)
from flask import (
    Flask, request, jsonify, abort, make_response
)

app = Flask(__name__)

@app.route('/')
def index():
    '''Home page for the radius app.'''
    return 'Welcome to the http interface for <i><b>radius!</b></i>'


@app.errorhandler(404)
def not_found(error):
    '''Friendlier error response.'''
    return make_response(jsonify({'error': 'Not Found!'}), 404)


@app.route('/api/profiles/create', methods=['POST'])
def create_profile():
    '''POST a new profile.

    NOTE TO SELF: consider adding a DATETIME stamp to profile database table for easier retrieval.
    
    Arguments:
    latitude -- intial latitude component of location in degrees
    longitude -- intial longitude component of location in degrees
    '''
    if not request.json or 'latitude' not in request.json and 'longitude' not in request.json:
        abort(404)

    lat, lon = request.json['latitude'], request.json['longitude']
    profile = post_profileDB(lat, lon)

    if len(profile) == 0:
        abort(404)

    return (jsonify({'profile': profile}), 201)


@app.route('/api/profiles/nearby/<int:profile_id>', methods=['GET'])
def retrieve_profiles(profile_id):
    '''GET nearby profiles.

    Arguments:
    profile_id -- profile near which other nearby profiles are to be fetched
    distance -- search distance in Kms
    '''
    distance = request.args.get('distance') # distance not required

    # if distance not provided, use default query distance
    if distance is None:
        profiles = get_profilesDB(profile_id)
    else:
        profiles = get_profilesDB(profile_id, float(distance))

    if len(profiles) == 0:
        abort(404)

    return jsonify({'profiles': profiles})


@app.route('/api/profiles/update/<int:profile_id>', methods=['PUT'])
def update_profile(profile_id):
    '''Update a profile.'''
    # if not request.json or 'latitude' not in request.json and 'longitude' not in request.json:
    #     abort(404)

    lat, lon = request.json['latitude'], request.json['longitude']
    profile = put_profileDB(profile_id, lat, lon)

    if len(profile) == 0:
        abort(404)

    return jsonify({'profile': profile})


@app.route('/api/profiles/delete/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    '''Delete a profile.'''
    result = None

    # if profile was deleted successfully, then return True
    if delete_profileDB(profile_id):
        result = True
    else:
        result = False

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
