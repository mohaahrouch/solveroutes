from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from distance_matrix import calcul_distance_matrix



def create_data_model(locations,num_vehicles):
    data = {}
    data['distance_matrix'] =calcul_distance_matrix(locations)
    data['num_vehicles'] = int(num_vehicles)
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution):
    routes = []
    max_route_distance = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = [manager.IndexToNode(index)]
        route_distance = 0
        while not routing.IsEnd(index):
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
            route.append(manager.IndexToNode(index))
        max_route_distance = max(route_distance, max_route_distance)
        routes.append(route)
    return routes



def main(locations, num_vehicles):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(locations, num_vehicles)
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), num_vehicles, data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(data, manager, routing, solution)
    else:
        print({'message':'error'})


# locations = [
#         {'lat': 11.5148422781311, 'lng': -11.14076957717038766},
#         {'lat': 41.5148422781311, 'lng': -0.14076957717038766},
#         {'lat': 61.5148422781311, 'lng': -54.14076957717038766},
#         {'lat': 31.5122781311, 'lng': -0.1957717038766},
#         {'lat': 31.52781311, 'lng': -0.14076957717038766},
#         {'lat': 31.581311, 'lng': -0.1457717038766}
#     ]
# num_vehicles = 2

# routes = main(locations, num_vehicles)
# print(routes)
