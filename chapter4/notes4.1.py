"""
Python for Data Analysis – NumPy Notes
Author: Your Name
Description: Notes and examples from Wes McKinney's book "Python for Data Analysis".
"""

# ----------------------------
# Import NumPy
import numpy as np

# ----------------------------
# Why NumPy?
# - ndarray: efficient multidimensional array for fast arithmetic and broadcasting
# - Mathematical functions operate on entire arrays without loops
# - Tools for reading/writing arrays and memory-mapped files
# - Linear algebra, random numbers, Fourier transforms
# - C API for integration with C/C++/Fortran

# ----------------------------
# Creating Large Arrays
my_arr = np.arange(1_000_000)  # NumPy array with 1 million elements
my_list = list(range(1_000_000))  # Python list with 1 million elements

# NumPy is generally 10-100x faster than Python lists and uses less memory

# ----------------------------
# 4.1 The NumPy ndarray
data = np.array([[1.5, -0.1, 3], [0, -3, 6.5]])
print(data)
print(data * 10)  # element-wise multiplication
print(data + data)  # element-wise addition
print(data.shape)  # (rows, columns)
print(data.dtype)  # data type

# ----------------------------
# Creating ndarrays from lists
data1 = [6, 7.5, 8, 0, 1]
arr1 = np.array(data1)
print(arr1)

data2 = [[1, 2, 3, 4], [5, 6, 7, 8]]
arr2 = np.array(data2)
print(arr2)

# Dimensions and shape
print(arr1.ndim, arr2.ndim)
print(arr1.shape, arr2.shape)

# ----------------------------
# Filling arrays
print(np.zeros(10))  # 1D zeros
print(np.zeros((3, 6)))  # 2D zeros
print(np.ones((2, 3, 4), dtype=np.int16))  # 3D ones, int
print(np.empty((2, 3, 4)))  # uninitialized

# ----------------------------
# Array creation functions
print(np.arange(15))  # like range but returns ndarray

# ----------------------------
# Data Types
arr = np.array([1, 2, 3], dtype=np.float64)
print(arr.dtype)

arr = np.array([1, 2, 3], dtype=np.int32)
print(arr.dtype)

arr = np.array([1, 2, 3, 4, 5])
print(arr.dtype)

# ----------------------------
# Casting arrays
arr = np.array([1, 2, 3, 4, 5])
float_arr = arr.astype(np.float64)
print(float_arr, float_arr.dtype)

arr2 = np.array([3.7, -1.2, -2.6, 0.5, 12.9, 10.1])
print(arr2.astype(np.int32))

# ----------------------------
# Arithmetic
arr = np.array([[1., 2., 3.], [4., 5., 6.]])
print(arr * arr)  # element-wise multiplication
print(arr - arr)  # subtraction
print(1 / arr)    # division
print(arr ** 0.5) # square root

arr2 = np.array([[0., 4., 1.], [7., 2., 12.]])
print(arr2 > arr)  # element-wise comparison

# ----------------------------
# Indexing and slicing
arr = np.arange(10)
print(arr[5])
print(arr[5:8])
arr[5:8] = 12
print(arr)

arr_slice = arr[5:8]  # view
arr_slice[1] = 12345  # mutates original array
print(arr)

arr_slice[:] = 0  # reset slice
print(arr)

# ----------------------------
# Multidimensional indexing
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr2d[0, 2])

arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(arr3d[0])
print(arr3d[1, 0])

# Boolean indexing
names = np.array(["Bob", "Joe", "Will", "Bob", "Will", "Joe", "Joe"])
data = np.array([[4, 7], [0, 2], [-5, 6], [0, 0], [1, 2], [-12, -4], [3, 4]])
print(data[names == "Bob"])
print(data[names == "Bob", 1:])

cond = names == "Bob"
print(data[~cond])  # invert condition

mask = (names == "Bob") | (names == "Will")
print(data[mask])

data[data < 0] = 0
data[names == 'Bob'] = 7
print(data)

# ----------------------------
# Fancy indexing
arr = np.zeros((8, 4))
for i in range(8):
    arr[i] = i
print(arr)

print(arr[[4, 3, 0, 6]])  # select rows in specific order
print(arr[[-3, -5, -7]])   # negative indices

arr = np.arange(32).reshape((8, 4))
print(arr[[1, 5, 7, 2], [0, 3, 1, 2]])  # select specific elements

arr[[1, 5, 7, 2], [0, 3, 1, 2]] = 0  # modify with fancy indexing
print(arr)

# ----------------------------
# Transposing and matrix multiplication
arr = np.arange(15).reshape((3, 5))
print(arr.T)

arr = np.array([[0, 1, 0], [1, 2, -2], [6, 3, 2], [-1, 0, -1], [1, 0, 1]])
print(np.dot(arr.T, arr))#dot multiplication is different for vectors and matrices, for matrices its matrix multiplication, for vectors is like matrice multiplication but results in scalar, as you add all the values together to get a value.
print(arr.T @ arr)  # matrix multiplication shortcut
print(arr.swapaxes(0, 1))