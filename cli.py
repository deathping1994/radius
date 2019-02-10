from core import Requirement, Properties

def input_requirement():
	user_input = raw_input("Enter lat,long,min_budget,max_budget,max_bath,min_bath,max_bed,min_bed \n (If you want to leave any field blank then input '_' in it's place)")
	user_input = user_input.split(',')
	data = {
		"lat": float(user_input[0]),
		"lon": float(user_input[1]),
		"min_budget": float(user_input[2]) if user_input[2] is not '_' else None,
		"max_budget": float(user_input[3]) if user_input[2] is not '_' else None,
		"max_bath": int(user_input[4]) if user_input[2] is not '_' else None,
		"min_bath": int(user_input[5]) if user_input[2] is not '_' else None,
		"max_bed": int(user_input[6]) if user_input[2] is not '_' else None,
		"min_bed": int(user_input[7]) if user_input[2] is not '_' else None
	}
	r = Requirement(**data)
	r.find_matching_properties(10.0000,6371.000)
def input_property():
	user_input = raw_input("Enter lat,long,price,bathroom,bedroom \n")
	user_input = user_input.split(',')
	data = {
		"lat": float(user_input[0]),
		"lon": float(user_input[1]),
		"price": float(user_input[2]),
		"bed": float(user_input[3]),
		"bath": float(user_input[4])
	}
	r = Properties(**data)
	r.find_matching_requirements(10.0000,6371.000)

def main():
	while True:
		resp = int(raw_input("Press 1 for finding Requirements\n Press 2 for finding Properties"))
		if resp == 1:
			input_requirement()
		elif resp == 2:
			input_property()


if __name__ == '__main__':
	main()	
