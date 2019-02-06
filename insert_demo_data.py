import MySQLdb
import random

conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="admin",
                  db="radius")
x = conn.cursor()

data = open("data.csv")
i = 0
for line in data:
    line = line.split(",")
    lat = int(float(line[0])*10000)
    lat = int(lat + random.randint(-10,10)*lat/100)
    long = int(float(line[1])*10000)
    long = int(long + random.randint(-10,10)*long/100)
    bed = random.randint(1,20)
    bath = random.randint(1,20)
    price = bed*bath*150
    try:
        resp = x.execute("""INSERT INTO properties (lat,lon,bed,bath,price) VALUES (%s,%s,%s,%s,%s)""",(lat,long,bed,bath,price))
        if i%100 ==0:
            conn.commit()
    except Exception as e:
        conn.rollback()
        print e
        i += 1

conn.close()