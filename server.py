from flask import Flask, request, jsonify
from flask_cors import CORS
from tsp import main as tspMain
from vrp import main as vrpMain
from cvrp import main as cvrpMain
from vrptw import main as vrptwMain
from get_tsp_addresses import tsp_address
from get_vrp_addresses import vrp_addresses 

import time
app = Flask(__name__)
CORS(app)


@app.route("/tsp", methods=['GET', 'POST'])
def tsp():
    try:
        # Get data from a JSON request
        data = request.get_json()
        # Convert array of JSON {'lat':, 'lng': } objects to an array of tuples
        latlng = [tuple(d.values()) for d in data]
        # solve the problem
        optimal_route_indice = tspMain(data)

        optimal_route = [latlng[i] for i in optimal_route_indice]
        
        # Convert latitudes and longitudes to addresses
        optimal_addresses = [tsp_address(lat,lng) for lat,lng in optimal_route]
        
        

        
        return jsonify({'coordinates': optimal_route, 'addresses': optimal_addresses})

    except:
        return jsonify({'error': 'something went wrong !!!'})

@app.route("/vrp", methods=['GET', 'POST'])
def vrp():

    try:
        # Get data from a JSON request
        data = request.get_json()
        # Convert array of JSON {'lat':, 'lng': } objects to an array of tuples
        latlng = [tuple(d.values()) for d in data['locations']]
        # solve the problem
        optimal_route_indice = vrpMain(data['locations'], data['num_vehicles'])

        optimal_route = [[latlng[j] for j in i] for i in optimal_route_indice]
        optimal_addresses=vrp_addresses(optimal_route)
        print(optimal_addresses,"\n")
        return jsonify({"cords":optimal_route,"adds":optimal_addresses})


    except:
        return jsonify({'error': 'something went wrong !!!'})


@app.route('/cvrp', methods=['POST'])
def cvrp_solution():
    try:

        # Get data from a JSON request
        data = request.get_json()
        # Convert array of JSON {'lat':, 'lng': } objects to an array of tuples
        latlng = [tuple(d.values()) for d in data['locations']]

        demands = list(data['demandes'])  # [0,1,2,3]
        num_vehicles = int(data['vehicles'])
        vehicle_capacities = list(data['capacities'])

        optimal_route_indice = cvrpMain(data['locations'], demands, vehicle_capacities, num_vehicles)
        # print('before')
        opi =  [[t[0] for t in route] for route in optimal_route_indice]
        demands= [t[1] for route in optimal_route_indice for t in route]
        # print('after')
        optimal_routes = [[latlng[j] for j in i] for i in opi]
        # print(optimal_routes)
         # Convert latitudes and longitudes to addresses
        adds = vrp_addresses(optimal_routes)
        # print(optimal_addresses)
      
        return jsonify({'coordinates': optimal_routes,'demands':demands,'addresses':adds})

    except:
        return jsonify({'error': 'something went wrong !!!'})


@app.route("/vrptw", methods=['GET', 'POST'])
def vrptw():

    try:
        # Get data from a JSON request
        data = request.get_json()
        # # Convert array of JSON {'lat':, 'lng': } objects to an array of tuples
        latlng = [tuple(d.values()) for d in data['locations']]
        # solve the problem
        
        optimal_route_indice = vrptwMain(data['locations'], data['time_windows'], data['num_vehicles'])
        print("::::::::::::::::::::::::::::::")
        print(optimal_route_indice)
        print("::::::::::::::::::::::::::::::")
        opr = [[tup[0] for tup in sublist] for sublist in optimal_route_indice]
        tw = [[(0, 0)] + [(item[1], item[2]) for item in sublist if item[0] != 0 or item[1] != 0 or item[2] != 0] + [(0, 0)] for sublist in optimal_route_indice]
        print(" OPR :::::::::")
        print(opr)
        print(" OPR :::::::::")
        print(" TW :::::::::")

        print(tw)
        print(" TW :::::::::")
        optimal_routes = [[latlng[j] for j in i] for i in opr]
        adds=vrp_addresses(optimal_routes)
        
        print(optimal_routes)
        return jsonify({'coordinates':optimal_routes,'time':tw,'addresses':adds})

    except:
        return jsonify({'error' : 'something went wrong !!!'})


# Run the app if it is the main module
if __name__ == '__main__':
    app.run(debug=False)
