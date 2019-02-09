import MySQLdb
import random
from math import radians

conn = MySQLdb.connect(host= "indianfire.in",
                  user="root",
                  passwd="admin",
                  db="radius-temp")
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