from core import Requirement, Properties

def input_requirement():
    user_input = raw_input("Enter lat, lon, min_budget, max_budget, min_bed, max_bed, min_bath, max_bath\n: ")
    user_input = user_input.split(', ')
    data = {
        "lat": float(user_input[0]),
        "lon": float(user_input[1]),
        "min_budget": float(user_input[2]),
        "max_budget": float(user_input[3]),
        "min_bed": int(user_input[4]),
        "max_bed": int(user_input[5]),
        "max_bath": int(user_input[6]),
        "min_bath": int(user_input[7]),
    }
    r = Requirement(**data)
    print r.find_matching_properties(10.0000, 6371.000)

def input_property():
    user_input = raw_input("Enter lat, lon, price, bedroom, bathroom\n: ")
    user_input = user_input.split(', ')
    data = {
        "lat": float(user_input[0]),
        "lon": float(user_input[1]),
        "price": float(user_input[2]),
        "bed": float(user_input[3]),
        "bath": float(user_input[4])
    }
    r = Properties(**data)
    print r.find_matching_requirements(10.0000, 6371.000)

def main():
    while True:
        resp = int(raw_input("Press 1 for finding Requirements, press 2 for finding Properties: "))
        if resp == 2:
            input_requirement()
        elif resp == 1:
            input_property()
        else:
            print "Exiting..."
            break

if __name__ == '__main__':
    main()  
