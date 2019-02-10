from datetime import datetime
from db import get_db

class Model(object):
	@property
	def json(self):
		return json.dumps(self.__dict__)

class Property(Model):
	table = "properties"

	def __init__(self,lat,lon,bed,bath,price, listed_on,id=None):
		self.lat = lat
		self.lon = lon
		self.bed = bed
		self.bath = bath
		self.price = price
		self.listed_on = listed_on or int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())
		self.id = id

	def save(self):
		db = get_db()
		try:
			x = db.cursor()
			x.execute("""INSERT INTO properties (lat,lon,bed,bath,price,listed_on) VALUES (%s,%s,%s,%s,%s,%s)""",
				(self.lat,self.lon,self.bed,self.bath,self.price, self.listed_on))
			db.commit()
		except Exception as e:
			print e
			db.rollback()
		finally:
			x.close()

	@classmethod
	def get_by_id(cls,id):
		db = get_db()
		try:
			x = db.cursor()
			sql = ('SELECT lat,lon,bed,bath,price,listed_on,id FROM {} WHERE id = %s'.format(cls.table))
			x.execute(sql,(id,))
			data = x.fetchone()
			if data:
				obj = cls(*data)
		except Exception as e:
			print e
		finally:
			x.close()
	def get_all(limit):
		return []

class Requirement(Model):
	table = "requirements"

	def __init__(self,lat,lon,min_bed,max_bed,min_bath,max_bath,min_budget,max_budget, listed_on):
		self.lat = lat
		self.lon = lon
		self.min_bed = min_bed
		self.max_bed = max_bed
		self.min_bath = min_bath
		self.max_bath = max_bath
		self.min_budget = min_budget
		self.max_budget = max_budget
		self.listed_on = listed_on or int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())

	def save(self):
		db = get_db()
		try:
			x = db.cursor()
			return x.execute("""INSERT INTO requirements (lat,lon,min_bed,max_bed,min_bath,max_bath,min_budget,max_budget,listed_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
				(self.lat,self.lon,self.min_bed,self.max_bed,self.min_bath,self.max_bath,self.min_budget,self.max_budget,self.listed_on))
			db.commit()
		except Exception as e:
			print e
			db.rollback()
		finally:
			x.close()




