from math import pi, radians, asin, sin, cos
from hashlib import md5
import redis
import sys
import db

PI = pi


	
class GeoHelper(object):
	"""docstring for ClassName"""
	MIN_LAT = radians(-90)*1
	MAX_LAT = radians(90)*1
	MIN_LON = radians(-180)*1
	MAX_LON = radians(180)*1
	
	@classmethod
	def get_bounding_coordinates(cls,distance, radius, rad_lat, rad_lon):
			if (radius < 0 or distance < 0):
				raise ValueError("Radius and Distance must be greater than 0")

			# angular distance in radians on a great circle
			rad_dist = distance / radius

			min_lat = rad_lat - rad_dist
			max_lat = rad_lat + rad_dist

			if (min_lat > cls.MIN_LAT and max_lat < cls.MAX_LAT):
				delta_lon = asin(sin(rad_dist)/cos(rad_lat))
				min_lon = rad_lon - delta_lon
				if (min_lon < cls.MIN_LON):
					min_lon += 2 * PI
				max_lon = rad_lon + delta_lon
				if (max_lon > cls.MAX_LON):
					max_lon -= 2 * PI
			else:
				# a pole is within the distance
				min_lat = max(min_lat, cls.MIN_LAT)
				max_lat = min(max_lat, cls.MAX_LAT)
				min_lon = cls.MIN_LON
				max_lon = cls.MAX_LON

			return [(min_lat, min_lon),
					(max_lat, max_lon)]
		

class Requirement(object):
	"""docstring for ClassName"""
	def __init__(self, lat,lon,min_budget,max_budget,min_bedrooms,max_bedrooms,min_bathroom,max_bathroom):
		self.lat = lat
		self.lat_rad = radians(lat)
		self.lon = lon
		self.lon_rad = radians(lon)
		self.min_budget = min_budget
		self.max_budget = max_budget
		self.min_bedrooms = min_bedrooms
		self.max_bedrooms = max_bedrooms
		self.min_bathroom = min_bathroom
		self.max_bathroom = max_bathroom
		self.sql = None
		self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
		self.db = db.get_db()

	def _get_result_from_cache(self):
		if self.sql:
			sql_hash = md5(self.sql).hexdigest()
			cached_result = self.redis.zrange_by_score(sql_hash,0,0.4)
			return cached_result
	
	def _set_result_in_cache(self, sql, matches):
		sql_hash = md5(sql or self.sql).hexdigest()
		self.redis.zadd(sql_hash,matches)
		
	

	def find_matching_properties(self, distance,radius):
		# matches = self._get_result_from_cache()
		# if matches:
		# 	return matches
		bounding_coordinates = GeoHelper.get_bounding_coordinates(distance, radius,self.lat_rad,self.lon_rad)
		meridian180WithinDistance =bounding_coordinates[0][1] > bounding_coordinates[1][1]
		sql = """SELECT *, {} * (acos(sin({}) * sin(lat) + cos({}) * cos(lat) * cos(lon - {}))) as distance FROM properties_new WHERE (lat >= {} AND lat <= {}) AND (lon >= {} """ + ("OR" if meridian180WithinDistance else "AND") + " lon <= {})"
		params = (	radius,
					self.lat_rad,
					self.lat_rad,
					self.lon_rad,
					bounding_coordinates[0][0],
					bounding_coordinates[1][0],
					bounding_coordinates[0][1],
					bounding_coordinates[1][1],
					distance
					)
		sql_where_clause =[
			"price BETWEEN %s AND %s" % ((self.min_budget*0.75 or self.max_budget*0.75),(self.max_budget*1.25 or self.min_budget*1.25)),
			"bed BETWEEN %s AND %s" %((self.min_bedrooms - 2 or self.max_bedrooms - 2),(self.max_bedrooms + 2 or self.min_bedrooms + 2)),
			"bath BETWEEN %s AND %s" % ((self.min_bathroom - 2 or self.max_bathroom - 2),(self.max_bathroom + 2 or self.min_bathroom + 2))
		]
		sql_having_clause = " HAVING distance <= {}"
		sql_parts = [sql]
		sql_parts.extend(sql_where_clause)
		sql = " AND ".join(sql_parts) + sql_having_clause
		x = self.db.cursor()
		x.execute(sql.format(*params))
		for row in x:
			print row



data = {
	"lat": float(sys.argv[1]),
	"lon": float(sys.argv[2]),
	"min_budget": 1000,
	"max_budget": 150000,
	"max_bathroom": 100,
	"min_bathroom": 3,
	"max_bedrooms": 100,
	"min_bedrooms": 4
}
r = Requirement(**data)
r.find_matching_properties(10.0000,6371.000)