"""
NumPy Linear Algebra Notes
Chapter: Linear Algebra with Arrays
"""

import numpy as np
from numpy.linalg import inv, qr

# ----------------------------
# Dot product vs element-wise multiplication
x = np.array([[1., 2., 3.], [4., 5., 6.]])
y = np.array([[6., 23.], [-1, 7], [8, 9]])

print("Matrix x:\n", x)
print("Matrix y:\n", y)

# Element-wise multiplication uses * (not matrix multiplication)
# Matrix multiplication uses np.dot() or the @ operator
print("x.dot(y):\n", x.dot(y))  # equivalent to np.dot(x, y)

# Dot product measures similarity of vectors:
# - Large positive → vectors point in similar direction
# - Zero → perpendicular (no similarity)
# - Negative → opposite directions

# Matrix-vector multiplication
print("x @ ones vector:", x @ np.ones(3))

# ----------------------------
# Random matrix and inverse
rng = np.random.default_rng()
X = rng.standard_normal((5, 5))
mat = X.T @ X  # symmetric positive-definite matrix
print("mat:\n", mat)

# Compute inverse
mat_inv = inv(mat)
print("Inverse of mat:\n", mat_inv)

# Multiplying a matrix by its inverse should give identity (approx due to floating-point errors)
identity_approx = mat @ mat_inv
print("mat @ inv(mat):\n", identity_approx)

# ----------------------------
# Common Linear Algebra functions in NumPy
"""
diag    : Return diagonal elements of a square matrix as 1D array, or convert 1D array to square matrix with zeros elsewhere
dot     : Matrix multiplication
trace   : Sum of diagonal elements
det     : Determinant of a square matrix
eig     : Eigenvalues and eigenvectors of a square matrix
inv     : Inverse of a square matrix
pinv    : Moore-Penrose pseudoinverse
qr      : QR decomposition
svd     : Singular value decomposition
solve   : Solve linear system Ax = b
lstsq   : Least-squares solution to Ax = b
"""
