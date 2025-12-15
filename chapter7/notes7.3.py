# 7.3 Extension Data Types in pandas

# pandas traditionally relied on NumPy’s data types.
# NumPy types cannot represent missing values for integers or booleans.
# To solve this, pandas introduced *Extension Types*:
# - Allow new data types that store missing values properly (NA)
# - Treated as “first-class” dtypes inside pandas (Series, DataFrame)
# - Work seamlessly with pandas operations

import numpy as np
import pandas as pd

# -----------------------------------------
# Basic Series: default integer type = int64
# But int64 CANNOT store missing values, so pandas upcasts to float64
# -----------------------------------------

s = pd.Series([1, 2, 3, None])
print(s.dtype)
# Output: float64   (because None forces floats)

# -----------------------------------------
# Nullable Integer Type: Int64
# This is NOT NumPy int64
# - It can store missing values using pd.NA (not np.nan)
# - Behaves like integers, not floats
# -----------------------------------------

s = pd.Series([1, 2, 3, None], dtype=pd.Int64Dtype())
# OR equivalently:
s = pd.Series([1, 2, 3, None], dtype="Int64")

print(s)
print(s.isna())
print(s.dtype)

print(s[3])              # Shows <NA>
print(s[3] is pd.NA)      # True

# -----------------------------------------
# Nullable String Type: StringDtype
# Regular object dtype stores Python strings → slow & inconsistent.
# StringDtype → optimized, consistent string handling + supports pd.NA.
# -----------------------------------------

s = pd.Series(['one', 'two', None, 'three'], dtype=pd.StringDtype())
print(s)

# -----------------------------------------
# Converting DataFrame columns to extension types
# -----------------------------------------

df = pd.DataFrame({
    "A": [1, 2, None, 4],
    "B": ["one", "two", "three", None],
    "C": [False, None, False, True]
})

print(df)

# Convert columns to pandas extension dtypes
df["A"] = df["A"].astype("Int64")     # nullable integer
df["B"] = df["B"].astype("string")    # StringDtype
df["C"] = df["C"].astype("boolean")   # nullable BooleanDtype

print(df)

# -----------------------------------------
# Summary of Important Extension Dtypes
# -----------------------------------------
# These dtypes allow missing values (pd.NA) and behave more consistently
# than NumPy types within pandas.

# BooleanDtype      → nullable boolean ("boolean")
# CategoricalDtype  → categorical ("category")
# DatetimeTZDtype   → timezone-aware datetime
# Float32Dtype      → nullable float32 ("Float32")
# Float64Dtype      → nullable float64 ("Float64")

# Nullable integer types (all allow pd.NA):
# Int8Dtype    - "Int8"
# Int16Dtype   - "Int16"
# Int32Dtype   - "Int32"
# Int64Dtype   - "Int64"

# Nullable unsigned integers:
# UInt8Dtype   - "UInt8"
# UInt16Dtype  - "UInt16"
# UInt32Dtype  - "UInt32"
# UInt64Dtype  - "UInt64"

# Key advantage:
# Unlike traditional NumPy dtypes, these allow missing values *without forcing floats*.