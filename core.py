from math import pi, radians, asin, sin, cos
from hashlib import md5
import json
import redis
import sys
from db import DBHelper

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

class MatchesCollection(object):
	@classmethod
	def order_matches_by_score(cls, requirement, matches):
		max_budget = requirement.max_budget
		min_budget = requirement.min_budget
		max_bedroom = requirement.max_bedrooms
		min_bedroom = requirement.min_bedrooms
		max_bathroom = requirement.max_bathroom
		min_bathroom = requirement.min_bathroom

		for match in matches:
			price = match.price
			bathroom = match.bathroom
			bedroom = match.bedroom

			distance = match.distance if match.distance > 2 else 2
			distance_score = 0.3*(2/distance)

			if min_budget <= price <= max_budget:
				delta = 0
				leeway = 0
			else:
				if max_budget != min_budget:   # both max and min provided
					delta = (min(abs((min_budget-price)/min_budget), abs((max_budget-price)/max_budget))) * 0.3
					leeway = 0
				else:
					delta = abs((min_budget-price)/min_budget) * 0.3
					leeway = 0.1
			price_score = (0.3 - delta + leeway)
			price_score = price_score if price_score <= 0.3 else 0.3

			max_bedroom = max_bedroom or min_bedroom
			min_bedroom = min_bedroom or max_bedroom
			if min_bedroom <= bedroom <= max_bedroom:
				delta = 0
			else:
				if max_bedroom != min_bedroom:  # both max and min provided
					delta = min(abs((min_bedroom-bedroom)/min_bedroom), abs((max_bedroom-bedroom)/max_bedroom)) * 0.2
			bedroom_score = (0.2 - delta) 
			bedroom_score = bedroom_score if bedroom_score <= 0.2 else 0.2

			max_bathroom = max_bathroom or min_bathroom
			min_bathroom = min_bathroom or max_bathroom
			if min_bathroom <= bathroom <= max_bathroom:
				delta = 0
			else:
				if max_bathroom != min_bathroom:  # both max and min provided
					delta = min(abs((min_bathroom-bathroom)/min_bathroom), abs((max_bathroom-bathroom)/max_bathroom)) * 0.2
			bathroom_score = (0.2 - delta) 
			bathroom_score = bathroom_score if bathroom_score <= 0.2 else 0.2
			total_score = distance_score + price_score + bedroom_score + bathroom_score
			match.score = total_score
		return sorted(matches,key=lambda x:x.score, reverse=True)

	@classmethod
	def order_requirements_by_score(cls, property, matches):
		for match in matches:
			price = property.price
			bathroom = property.bathroom
			bedroom = property.bedroom
			max_budget = match.max_budget
			min_budget = match.min_budget
			max_bedroom = match.max_bedrooms
			min_bedroom = match.min_bedrooms
			max_bathroom = match.max_bathroom
			min_bathroom = match.min_bathroom

			distance = match.distance if match.distance > 2 else 2
			distance_score = 0.3*(2/distance)

			if min_budget <= price <= max_budget:
				delta = 0
				leeway = 0
			else:
				if max_budget != min_budget:   # both max and min provided
					delta = (min(abs((min_budget-price)/min_budget), abs((max_budget-price)/max_budget))) * 0.3
					leeway = 0
				else:
					delta = abs((min_budget-price)/min_budget) * 0.3
					leeway = 0.1
			price_score = (0.3 - delta + leeway)
			price_score = price_score if price_score <= 0.3 else 0.3

			max_bedroom = max_bedroom or min_bedroom
			min_bedroom = min_bedroom or max_bedroom
			if min_bedroom <= bedroom <= max_bedroom:
				delta = 0
			else:
				if max_bedroom != min_bedroom:  # both max and min provided
					delta = min(abs((min_bedroom-bedroom)/min_bedroom), abs((max_bedroom-bedroom)/max_bedroom)) * 0.2
			bedroom_score = (0.2 - delta) 
			bedroom_score = bedroom_score if bedroom_score <= 0.2 else 0.2

			max_bathroom = max_bathroom or min_bathroom
			min_bathroom = min_bathroom or max_bathroom
			if min_bathroom <= bathroom <= max_bathroom:
				delta = 0
			else:
				if max_bathroom != min_bathroom:  # both max and min provided
					delta = min(abs((min_bathroom-bathroom)/min_bathroom), abs((max_bathroom-bathroom)/max_bathroom)) * 0.2
			bathroom_score = (0.2 - delta) 
			bathroom_score = bathroom_score if bathroom_score <= 0.2 else 0.2
			total_score = distance_score + price_score + bedroom_score + bathroom_score
			match.score = total_score
		return sorted(matches,key=lambda x:x.score, reverse=True)

		
class Requirement(object):
	"""docstring for ClassName"""
	def __init__(self, lat,lon,min_budget,max_budget,min_bed,max_bed,min_bath,max_bath, distance=None,listed_on = None, id = None):
		self.lat = lat
		self.lat_rad = radians(lat)
		self.lon = lon
		self.lon_rad = radians(lon)
		self.min_budget = min_budget
		self.max_budget = max_budget
		self.min_bedrooms = min_bed
		self.max_bedrooms = max_bed
		self.min_bathroom = min_bath
		self.max_bathroom = max_bath
		self.id = id
		self.listed_on= listed_on
		self.sql = None
		self.distance = distance
		self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
		self.db = DBHelper.get_db()
		self.score = None
	
	def __repr__(self):
                temp = self.__dict__
                del temp['sql']
                del temp['db']
                del temp['redis']
                temp['listed_on'] = str(temp['listed_on'])
                return str(temp)

	

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
		sql = sql.format(*params)
		results = DBHelper.execute_query(self.db.cursor(),sql)
		matches = []
		for prop in results:
			prop = Properties(**prop)
			matches.append(prop)
		return MatchesCollection.order_matches_by_score(self,matches)

class Properties(object):
	def __init__(self, lat,lon,price,bed,bath,listed_on=None,distance=None,id=None):
		self.lat = lat
		self.lat_rad = radians(lat)
		self.lon = lon
		self.lon_rad = radians(lon)
		self.bedroom = bed
		self.bathroom = bath
		self.price = price
		self.score = 0
		self.sql = None
		self.distance = distance
		self.listed_on = listed_on
		self.id = id
		self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
		self.db = DBHelper.get_db()
	def __repr__(self):
		temp = self.__dict__
		del temp['sql']
		del temp['db']
		del temp['redis']
		temp['listed_on'] = str(temp['listed_on'])
		return str(temp)
	def _get_result_from_cache(self):
		if self.sql:
			sql_hash = md5(self.sql).hexdigest()
			cached_result = self.redis.zrange_by_score(sql_hash,0,0.4)
			return cached_result
	
	def _set_result_in_cache(self, sql, matches):
		sql_hash = md5(sql or self.sql).hexdigest()
		self.redis.set(sql_hash,matches)
		

	def find_matching_requirements(self, distance,radius):
		matches = self._get_result_from_cache()
		if matches:
			return matches
		bounding_coordinates = GeoHelper.get_bounding_coordinates(distance, radius,self.lat_rad,self.lon_rad)
		meridian180WithinDistance =bounding_coordinates[0][1] > bounding_coordinates[1][1]
		sql = """SELECT *, {} * (acos(sin({}) * sin(lat) + cos({}) * cos(lat) * cos(lon - {}))) as distance FROM requirements WHERE (lat >= {} AND lat <= {}) AND (lon >= {} """ + ("OR" if meridian180WithinDistance else "AND") + " lon <= {})"
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
			"min_budget*0.75 <= %s AND max_budget*1.25 >= %s " % (self.price, self.price),
			"min_bed -2<= %s AND max_bed +2>= %s" %(self.bedroom, self.bedroom),
			"min_bath -2<= %s AND max_bath +2>= %s" %(self.bathroom, self.bathroom)
		]
		sql_having_clause = " HAVING distance <= {}"
		sql_parts = [sql]
		sql_parts.extend(sql_where_clause)
		sql = " AND ".join(sql_parts) + sql_having_clause
		results = DBHelper.execute_query(self.db.cursor(),sql.format(*params))
		matches = []
		for prop in results:
			prop = Requirement(**prop)
			matches.append(prop)
		
		return MatchesCollection.order_requirements_by_score(self,matches)
