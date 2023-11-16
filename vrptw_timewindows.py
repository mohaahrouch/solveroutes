original_list = [[(0, 0, 0), (1, 1, 2), (0, 0, 0)], [(0, 0, 0), (4, 3, 4), (3, 2, 3), (2, 3, 4), (0, 0, 0)]]

modified_list =[[tup[0] for tup in sublist] for sublist in original_list]

print(modified_list)





