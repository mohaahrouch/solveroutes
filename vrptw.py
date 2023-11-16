# from ortools.constraint_solver import routing_enums_pb2
# from ortools.constraint_solver import pywrapcp
# from distance_matrix import calculate_time_matrix


# def create_data_model(locations, time_windows, nb_vehicles):
#     """Stores the data for the problem."""
#     data = {}
#     data['time_matrix'] = calculate_time_matrix(locations)
#     data['time_windows'] = time_windows
#     data['num_vehicles'] = nb_vehicles
#     data['depot'] = 0
#     return data


# def print_solution(data, manager, routing, solution):
#     """Returns the solution as a matrix."""
#     time_dimension = routing.GetDimensionOrDie('Time')
#     route_matrix = []
#     for vehicle_id in range(data['num_vehicles']):
#         index = routing.Start(vehicle_id)
#         route = []
#         while not routing.IsEnd(index):
#             node_index = manager.IndexToNode(index)
#             route.append((node_index, data['time_windows'][node_index]))
#             index = solution.Value(routing.NextVar(index))
#         node_index = manager.IndexToNode(index)
#         route.append((node_index, data['time_windows'][node_index]))
#         route_matrix.append(route)
#     return route_matrix


# def main(locations, time_windows, nb_vehicles):
#     """Solve the VRP with time windows."""
#     # Instantiate the data problem.
#     data = create_data_model(locations, time_windows, nb_vehicles)

#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(
#         len(data['time_matrix']), data['num_vehicles'], data['depot'])

#     # Create Routing Model.
#     routing = pywrapcp.RoutingModel(manager)

#     # Create and register a transit callback.
#     def time_callback(from_index, to_index):
#         """Returns the travel time between the two nodes."""
#         # Convert from routing variable Index to time matrix NodeIndex.
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return data['time_matrix'][from_node][to_node]

#     transit_callback_index = routing.RegisterTransitCallback(time_callback)

#     # Define cost of each arc.
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Add Time Windows constraint.
#     time = 'Time'
#     routing.AddDimension(
#         transit_callback_index,
#         30,  # allow waiting time
#         30,  # maximum time per vehicle
#         False,  # Don't force start cumul to zero.
#         time)
#     time_dimension = routing.GetDimensionOrDie(time)
#     # Add time window constraints for each location except depot.
#     for location_idx, time_window in enumerate(data['time_windows']):
#         if location_idx == data['depot']:
#             continue
#         index = manager.NodeToIndex(location_idx)
#         time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
#     # Add time window constraints for each vehicle start node.
#     depot_idx = data['depot']
#     for vehicle_id in range(data['num_vehicles']):
#         index = routing.Start(vehicle_id)
#         time_dimension.CumulVar(index).SetRange(
#             data['time_windows'][depot_idx][0],
#             data['time_windows'][depot_idx][1])

#     # Instantiate route start and end times to produce feasible times.
#     for i in range(data['num_vehicles']):
#         routing.AddVariableMinimizedByFinalizer(
#             time_dimension.CumulVar(routing.Start(i)))
#         routing.AddVariableMinimizedByFinalizer(
#             time_dimension.CumulVar(routing.End(i)))

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

#     # Solve the problem.
#     solution = routing.SolveWithParameters(search_parameters)

#     # Get the optimized route matrix.
#     if solution:
#         routes = print_solution(data, manager, routing, solution)
#         converted_routes = []
#         for route in routes:
#             converted_route = []
#             for node, _ in route:
#                 converted_route.append(node)
#             converted_routes.append(converted_route)
#         return converted_routes

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from distance_matrix import calculate_time_matrix

def create_data_model(locations, time_windows, nb_vehicles):
    data = {}
    data['time_matrix'] = calculate_time_matrix(locations)
    data['time_windows'] = time_windows
    data['num_vehicles'] = nb_vehicles
    data['depot'] = 0
    return data

def print_solution(data, manager, routing, solution):
    time_dimension = routing.GetDimensionOrDie('Time')
    route_list = []

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = []
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            time_window = data['time_windows'][node_index]
            route.append((node_index, time_window[0], time_window[1]))
            index = solution.Value(routing.NextVar(index))
        node_index = manager.IndexToNode(index)
        time_window = data['time_windows'][node_index]
        route.append((node_index, time_window[0], time_window[1]))
        route_list.append(route)

    return route_list

def main(locations, time_windows, nb_vehicles):
    data = create_data_model(locations, time_windows, nb_vehicles)
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        30,  # allow waiting time
        30,  # maximum time per vehicle
        False,
        time)
    time_dimension = routing.GetDimensionOrDie(time)

    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        routes = print_solution(data, manager, routing, solution)
        return routes
