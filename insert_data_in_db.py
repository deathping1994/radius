'''This module inserts data from data.csv into a database to query from.'''
import csv
import os
from math import radians
import pymysql
from dotenv import load_dotenv

load_dotenv()

TABLE = 'profiles'

def list_of_dict(file):
	'''Reads a CSV file as a dictionary and return a list of dictionaries to be 
	inserted into the database.

	The CSV file need to have headers in order for Python to read it as a dictionary.
	Argument:
	file -- a CSV file containing atleast latitude(phi) and longitude(lambda)
	'''
	profiles = []

	with open('data.csv') as f:
		reader = csv.DictReader(f)

		for row in reader:
			# appending lon, lat as radians to avoid conversion at query time
			profiles.append({
				'lon': radians(float(row['lambda'])),
				'lat': radians(float(row['phi']))
			})

	return profiles

def insert_into_db_table(profiles):
	'''Inserts data given as a list of dictionaries into the database table.'''
	# virtual environment variables in .env file
	connection = pymysql.connect(
		host=os.environ['DB_HOST'],
		user=os.environ['DB_USER'],
		password=os.environ['DB_PASSWORD'],
		db=os.environ['DB_NAME'],
		# cursorclass=pymysql.cursors.DictCursor
	)

	sql = f"INSERT INTO {TABLE} (lon, lat) VALUES (%s, %s)"

	try:
		with connection.cursor() as cursor:

			for profile in profiles:
				# inserting lon, lat into table
				cursor.execute(sql, (profile['lon'], profile['lat']))

		# commiting changes to database
		connection.commit()

	finally:
		connection.close()

def main():
	profiles = list_of_dict('data.csv') # get list of dictionaries
	insert_into_db_table(profiles) # insert into database table

if __name__ == '__main__':
	main()
