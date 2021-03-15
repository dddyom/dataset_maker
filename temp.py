import numpy as np

a = np.array([[[1, 2],
               [3, 4]],
              [[5, 6],
               [7, 8]]])

b = np.array([[[11, 12],
               [31, 41]],
              [[15, 16],
               [71, 81]]])

print(np.concatenate((a, b)))