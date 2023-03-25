import numpy as np
import statistics

arr = np.loadtxt("colorcsv/yellow.csv", delimiter=",", dtype=int)
print(len(arr))
norms = np.linalg.norm(arr, axis=1)
print(norms)



# print("means:")
# print(mean_arr)

# means_expanded = np.tile(mean_arr, (len(normalized_array),1))
# sub_arr = np.subtract(normalized_array, means_expanded)
# square_arr = np.square(sub_arr)
# sum_arr = np.sum(square_arr, axis=0)
# mean_arr = sum_arr / len(normalized_array)
# stdev_arr = np.sqrt(mean_arr)

# print("stddev: ")
# print(stdev_arr)

