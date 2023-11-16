from geopy.geocoders import Nominatim

def vrp_addresses(coordinates_list):
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    addresses_list = []
    
    for tour in coordinates_list:
        tour_addresses = []
        for coord in tour:
            lat, lng = coord
            location = geolocator.reverse(f"{lat}, {lng}", exactly_one=True)
            address = location.address if location else None
            tour_addresses.append(address)
        addresses_list.append(tour_addresses)
    
    return addresses_list