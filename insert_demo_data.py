import MySQLdb
import random
from math import radians
import os
from dotenv import load_dotenv

load_dotenv()

conn = MySQLdb.connect(
    host=os.environ.get('DB_HOST', 'localhost'),
    user=os.environ.get('DB_USER', 'radius'),
    passwd=os.environ.get('DB_PASSWORD', 'radius'),
    db=os.environ.get('DB_NAME', 'radius')
)
x = conn.cursor()

data = open("data.csv")
i = 0
for line in data:
    line = line.split(",")
    lat = float(line[0])
    lat = lat + random.randint(-10,10)*lat/100
    lat = radians(lat)
    long = float(line[1])
    long = radians(long + random.randint(-10,10)*long/100)
    bed = random.randint(1,20)
    bath = random.randint(1,20)
    price = bed*bath*150
    try:
        resp = x.execute("""INSERT INTO properties_new (lat,lon,bed,bath,price) VALUES (%s,%s,%s,%s,%s)""",(lat,long,bed,bath,price))
        if i%100 ==0:
            conn.commit()
    except Exception as e:
        conn.rollback()
        print e
        i += 1

conn.close()