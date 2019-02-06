import MySQLdb
import os

DB_USER = os.environ.get('DB_USER', 'root')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'admin')
DB_NAME = os.environ.get('DB_NAME', 'radius')

db = MySQLdb.connect(host= DB_HOST,
                  user=DB_USER,
                  passwd=DB_PASSWORD,
                  db=DB_NAME)

def get_db():
	if not db:
		global db
		db = MySQLdb.connect(host= DB_HOST,
                  user=DB_USER,
                  passwd=DB_PASSWORD,
                  db=DB_NAME)
		return db
	return db

