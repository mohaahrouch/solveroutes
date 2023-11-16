# routes_list = [[(0, 0), (4, 500), (3, 500), (0, 0)], [(0, 0), (1, 0), (2, 10), (0, 0)]]

# # Extract the first elements of each tuple into the first_variable
# first_variable = [t[0] for route in routes_list for t in route]

# # Extract the second elements of each tuple into the second_variable
# second_variable = [t[1] for route in routes_list for t in route]

# print("First Variable:", first_variable)
# print("Second Variable:", second_variable)










routes_list = [[(0, 0), (4, 500), (6,900),(3, 500), (0, 0)], [(0, 0), (1, 0), (2, 10), (0, 0)]]

# Extract the first elements of each tuple into the first_variable
first_variable = [[t[0] for t in route] for route in routes_list]

# Extract the second elements of each tuple into the second_variable
second_variable = [t[1] for route in routes_list for t in route]

print("First Variable:", first_variable)
print("Second Variable:", second_variable)
