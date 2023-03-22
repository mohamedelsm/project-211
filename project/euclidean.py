import numpy as np
import pandas as pd


arr = np.loadtxt("colorcsv/yellow.csv", delimiter=",", dtype=int)

sum_of_rows = arr.sum(axis=1)
normalized_array = arr / sum_of_rows[:, np.newaxis]

sum_arr = np.sum(normalized_array, axis=0)
mean_arr = sum_arr / len(normalized_array)

print("means:")
print(mean_arr)

means_expanded = np.tile(mean_arr, (len(normalized_array),1))
sub_arr = np.subtract(normalized_array, means_expanded)
square_arr = np.square(sub_arr)
sum_arr = np.sum(square_arr, axis=0)
mean_arr = sum_arr / len(normalized_array)
stdev_arr = np.sqrt(mean_arr)

print("stddev: ")
print(stdev_arr)

