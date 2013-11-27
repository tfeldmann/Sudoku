import numpy as np

a = np.array([[569, 106],
              [768, 356],
              [531, 105],
              [800, 139]])
# sort by y
a = a[np.argsort(a[:, 1])]

# put in groups
a = np.reshape(a, (2, 2, 2))

# sort rows by x
a = np.vstack([row[np.argsort(row[:, 0])] for row in a])

# regroup
a = np.reshape(a, (4, 1, 2))

print a
