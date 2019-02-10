import sys
from core import Requirement
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