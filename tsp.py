from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from distance_matrix import calcul_distance_matrix

def create_data_model(locations):
    data = {}
    data['distance_matrix'] = calcul_distance_matrix(locations)
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    index = routing.Start(0)
    route_distance = 0
    solution_indices = [manager.IndexToNode(index)]
    while not routing.IsEnd(index):
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
        solution_indices.append(manager.IndexToNode(index))
    return solution_indices

def main(locations):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(locations)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
    data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        return print_solution(manager, routing, solution)