import sys
from core import Requirement, Properties
data = {
	"lat": float(sys.argv[1]),
	"lon": float(sys.argv[2]),
	"min_budget": 1000,
	"max_budget": 150000,
	"max_bath": 100,
	"min_bath": 3,
	"max_bed": 100,
	"min_bed": 4
}
r = Requirement(**data)
print r.find_matching_properties(10.0000,6371.000)

data = {
	"lat": float(sys.argv[1]),
	"lon": float(sys.argv[2]),
	"price": 10000,
	"bed": 10,
	"bath": 4
}
r = Properties(**data)
print len(r.find_matching_requirements(1000.0000,6371.000))
