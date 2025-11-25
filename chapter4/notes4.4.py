"""
Python for Data Analysis – NumPy Notes
Chapter 4.5: Conditional Logic, Aggregations, and Set Operations
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Creating a 2D grid of points
points = np.arange(-5, 5, 0.01)  # points from -5 to 5 with step size 0.01
xs, ys = np.meshgrid(points, points)  # create 2D grid
print("X grid:\n", xs)
print("Y grid:\n", ys)

# Compute distance from origin using Pythagoras
z = np.sqrt(xs**2 + ys**2)
print("Distance array:\n", z)

# Display as an image
plt.imshow(z, cmap=plt.cm.gray, extent=(-5, 5, -5, 5))
plt.colorbar()
plt.show()

# Close all figures
plt.close('all')

# ----------------------------
# Expressing conditional logic as array operations
xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
cond = np.array([True, False, True, True, False])

# Python list comprehension (less efficient)
result_list = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]

# NumPy vectorized approach (faster, supports multidimensional arrays)
result = np.where(cond, xarr, yarr)
print("Conditional selection result:", result)

# ----------------------------
# Random arrays and element-wise conditional operations
rng = np.random.default_rng()  # standalone random generator
arr = rng.standard_normal((4, 4))
print("Random 4x4 array:\n", arr)

# Boolean mask
print("Positive mask:\n", arr > 0)

# Conditional replacement
print("Replace pos -> 2, neg -> -2:\n", np.where(arr > 0, 2, -2))
print("Replace pos -> 2, leave neg as is:\n", np.where(arr > 0, 2, arr))

# ----------------------------
# Aggregation functions
print("Mean:", arr.mean())
print("Mean (np.mean):", np.mean(arr))
print("Sum:", arr.sum())

# Axis-specific operations
print("Mean by column:", arr.mean(axis=0))
print("Sum by column:", arr.sum(axis=0))

# ----------------------------
# Cumulative operations
arr1d = np.arange(9).reshape((1, 9))
print("Array:", arr1d)
print("Cumulative sum:", arr1d.cumsum())
print("Cumulative product:", arr1d.cumprod())
print("Cumsum along rows:", arr1d.cumsum(axis=0))
print("Cumsum along columns:", arr1d.cumsum(axis=1))

# ----------------------------
# Methods for Boolean arrays
arr = rng.standard_normal(100)
print("Number of positive values:", (arr > 0).sum())
print("Number of non-positive values:", (arr <= 0).sum())

bools = np.array([False, False, True, False])
print("Any True?", bools.any())
print("All True?", bools.all())

# ----------------------------
# Sorting arrays
arr = rng.standard_normal(6)
print("Original 1D array:", arr)
arr.sort()  # sorts in-place
print("Sorted in-place:", arr)

arr2d = rng.standard_normal((5, 3))
print("Original 2D array:\n", arr2d)
arr2d.sort(axis=0)  # sort along columns
print("Sorted by column:\n", arr2d)
arr2d.sort(axis=1)  # sort along rows
print("Sorted by row:\n", arr2d)

# numpy.sort returns a sorted copy
arr2 = np.array([5, -10, 7, 1, 0, -3])
sorted_arr2 = np.sort(arr2)
print("Sorted copy:", sorted_arr2)

# ----------------------------
# Unique values and set operations
names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
print("Unique names:", np.unique(names))

ints = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4, 4])
print("Unique integers:", np.unique(ints))

values = np.array([6, 7, 2, 3, 6, 8, 2, 4, 9, 3])
print("Values in [2,3,6]?", np.isin(values, [2, 3, 6]))

# Other useful set operations:
# np.intersect1d(x, y) - sorted common elements
# np.union1d(x, y) - sorted union
# np.setdiff1d(x, y) - elements in x not in y
# np.setxor1d(x, y) - symmetric difference
