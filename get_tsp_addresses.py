from geopy.geocoders import Nominatim

def tsp_address(lat, lng):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(f"{lat}, {lng}", exactly_one=True)
    address = location.address if location else None
    return address

