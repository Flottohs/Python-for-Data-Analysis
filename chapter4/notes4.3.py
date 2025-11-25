# ------------------------------------------------------------
# 4.3 Universal Functions (ufuncs): Fast Element-Wise Operations
# ------------------------------------------------------------

import numpy as np

# A ufunc is a "universal function" — it performs fast vectorized 
# element-wise operations on NumPy arrays.

arr = np.arange(10)
print("arr:", arr)

print("sqrt(arr):", np.sqrt(arr))     # unary ufunc
print("exp(arr):",  np.exp(arr))      # unary ufunc (e**x)

# ------------------------------------------------------------
# Binary ufuncs (take two arrays)
# ------------------------------------------------------------

rng = np.random.default_rng()        # standalone random generator instance

x = rng.standard_normal(8)
y = rng.standard_normal(8)

print("\nx:", x)
print("y:", y)

# maximum chooses the element-wise larger value
print("maximum(x, y):", np.maximum(x, y))

# ------------------------------------------------------------
# Ufunc returning multiple arrays (modf example)
# ------------------------------------------------------------

arr = rng.standard_normal(7) * 5
print("\narr:", arr)

# modf splits into fractional + whole parts
fractional, whole = np.modf(arr)
print("fractional part:", fractional)
print("whole part:", whole)

# ------------------------------------------------------------
# Using the 'out' parameter (store results into existing array)
# ------------------------------------------------------------

out = np.zeros_like(arr)

print("\narr + 1  :", np.add(arr, 1))
print("arr + 1 -> out:", np.add(arr, 1, out=out))
print("out array:", out)

# ------------------------------------------------------------
# Common unary ufuncs
# ------------------------------------------------------------
"""
abs, fabs        - Absolute value
sqrt             - Square root
square           - Square
exp              - e**x
log, log10, log2 - Logarithms
sign             - Returns -1, 0, or 1
ceil, floor      - Rounding functions
rint             - Round to nearest integer (keeps dtype)
modf             - Fractional + whole parts
isnan, isfinite  - Boolean checks
cos, sin, tan    - Trigonometric
arccos, arcsin   - Inverse trig
logical_not      - Element-wise NOT
"""

# ------------------------------------------------------------
# Common binary ufuncs
# ------------------------------------------------------------
"""
add, subtract, multiply, divide, floor_divide
power
maximum, minimum   (# fmax/fmin ignore NaN)
mod
copysign
greater, less, equal, not_equal
logical_and, logical_or, logical_xor
"""