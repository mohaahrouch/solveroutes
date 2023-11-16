import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points 
    on the Earth's surface in kilometers using the Haversine formula."""
    
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = (math.sin(dlat/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin(dlon/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    distance = r * c
    
    return distance

def calcul_distance_matrix(locations):
    n = len(locations)
    dist_matrix = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = round(calculate_distance(locations[i]['lat'], locations[i]['lng'], locations[j]['lat'], locations[j]['lng']))
    return dist_matrix


def calculate_time_matrix(locations):
    """Calculates the time matrix for a set of locations given their latitude and longitude coordinates."""
    num_locations = len(locations)
    time_matrix = [[0] * num_locations for i in range(num_locations)]
    for i in range(num_locations):
        for j in range(i+1, num_locations):
            distance = calculate_distance(locations[i]['lat'], locations[i]['lng'], locations[j]['lat'], locations[j]['lng'])
            time = distance / 50 * 60  #Assuming that the average speed is 50 km/h, we can calculate the time it takes to travel the distance between two locations as distance / speed * 60. This gives us the travel time in minutes, assuming a constant speed of 50 km/h. You may adjust this calculation based on the actual speed limit and traffic conditions in your specific context.
            
            time_matrix[i][j] = time
            time_matrix[j][i] = time
    return time_matrix