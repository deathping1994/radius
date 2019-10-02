from flask import Flask, request, Response
from model import Property, Requirement

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/requirement',methods=["GET"])
@app.route('/requirement/<int:post_id>',methods=["GET","POST","PATCH","DELETE"])
def requirement(post_id=None):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/property',methods=["GET"])
@app.route('/property/<int:post_id>',methods=["GET","POST"])
def property(post_id=None):
    if request.method == "GET":
        if post_id is not None:
            obj = Property.get_by_id(post_id)
            if obj:
                return Response(obj.json, status=200)
            return Response(status=404)
        else:
            limit = request.get('limit', 10)
            objs = Property.get_all(limit)
            resp = [obj for obj in objs]
            return Response(json.dumps(resp), status=200)
    if request.method == "POST":
        lat = request.form.get('lat')
        lon = request.form.get('lon')
        price = request.form.get('price')
        bath = request.form.get('bath')
        bed = request.form.get('lat')
        if not (lat and lon and price and bath and bed):
            return Response(json.dumps({'msg':"Missing required parameter"}),status="400")
        obj = Property(lat,lon,bed,bath,price)
        obj.save()
        return Response(obj.json, status=201)

@app.route('/requirement/<int:post_id>/matches',methods=["GET"])
def requirement_matches(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/property/<int:post_id>/matches',methods=["GET"])
def property_matches(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

