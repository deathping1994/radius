import sys
import datetime
from core import Requirement, Properties

data_file = open("data.csv")
start_time = datetime.datetime.utcnow()
batch_start_time = start_time
i =0 
for line in data_file:
	line = line.split(',')
	data = {
		"lat": float(line[1]),
		"lon": float(line[0]),
		"min_budget": 1000,
		"max_budget": 150000,
		"max_bath": 100,
		"min_bath": 3,
		"max_bed": 100,
		"min_bed": 4
	}
	r = Requirement(**data)
	r.find_matching_properties(10.0000,6371.000)

	data = {
		"lat": float(line[1]),
		"lon": float(line[0]),
		"price": 10000,
		"bed": 10,
		"bath": 4
	}
	r = Properties(**data)
	r.find_matching_requirements(10.0000,6371.000)
	i +=1
	if i % 100 ==0:
		print "Time %s" % (datetime.datetime.utcnow()-batch_start_time).total_seconds()
		batch_start_time = datetime.datetime.utcnow()
print "Total time: %s" % (datetime.datetime.utcnow()-start_time).total_seconds()
print "total count %s" % i
	
