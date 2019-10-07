from data import get_profiles
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/profiles', methods=['GET'])
def profiles():
    lat = float(request.args['lat'])
    lon = float(request.args['lon'])
    dist = float(request.args['dist'])
    print(lat, lon, dist)
    profiles = get_profiles(lat, lon, dist)
    return jsonify({'profiles': profiles})

if __name__ == '__main__':
    app.run(debug=True)
