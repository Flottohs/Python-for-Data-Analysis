 # ----------------------------
# 5.1 Introduction to pandas Data Structures
# ----------------------------

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# ----------------------------
# Series: One-Dimensional Labeled Arrays
# ----------------------------

# A Series is a 1D array-like object with an associated array of labels called the index.

# Simplest Series from data only:
obj = pd.Series([4, 7, -5, 3])
print(obj)

# Access underlying data array and index
print(obj.array)
print(obj.index)

# Series with custom index labels
obj2 = pd.Series([4, 7, -5, 3], index=["d", "b", "a", "c"])
print(obj2)
print(obj2.index)

# Indexing by label
print(obj2["a"])

# Multiple label indexing
print(obj2[["c", "a", "d"]])

# Filtering values
print(obj2[obj2 > 0])  # values greater than 0

# Arithmetic and vectorized operations
print(obj2 * 2)
print(np.exp(obj2))

# Series can be thought of as a fixed-length, ordered dictionary
if "b" in obj2:
    print(True)

# Creating a Series from a dictionary
sdata = {"Ohio": 35000, "Texas": 71000, "Oregon": 16000, "Utah": 5000}
obj3 = pd.Series(sdata)
print(obj3.to_dict())

# Overriding order of dictionary keys with index
states = ["California", "Ohio", "Oregon", "Texas"]
obj4 = pd.Series(sdata, index=states)
print(obj4)

# Detect missing data
print(pd.isna(obj4))
print(pd.notna(obj4))
print(obj4.isna())

# Operations with Series align on index
print(obj3 + obj4)

# Assigning custom index
object = pd.Series(range(3))
object.index = ["a", "b", "c"]
print(object)

# ----------------------------
# DataFrame: Two-Dimensional Labeled Data
# ----------------------------

# A DataFrame represents a rectangular table of data with named columns
# Each column can have a different type (numeric, string, boolean, etc.)

data = {
    "state": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada", "Nevada"],
    "year": [2000, 2001, 2002, 2001, 2002, 2003],
    "pop": [1.5, 1.7, 3.6, 2.4, 2.9, 3.2]
}
frame = pd.DataFrame(data)
print(frame)

# View first/last rows
print(frame.head())
print(frame.tail())

# Specify column order
print(pd.DataFrame(data, columns=['year', 'state', 'pop']))

# Columns not in data get missing values
frame2 = pd.DataFrame(data, columns=["year", "state", "pop", "debt"])
print(frame2)
print(frame2.columns)

# Access columns
print(frame2.state)
print(frame2.year)

# Access rows
print(frame2.loc[1])   # by label
print(frame2.iloc[1])  # by integer position

# Assign a scalar value to a column
frame2["debt"] = 16.5
print(frame2)

# Assign array or list: must match DataFrame length
frame2["debt"] = np.arange(6.)
print(frame2)

# Assign Series with possibly mismatched index
val = pd.Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
frame2["debt"] = val
print(frame2)

# Boolean assignment
frame2["eastern"] = frame2["state"] == "Ohio"
print(frame2)

# Delete a column
del frame2['eastern']
print(frame2)

# Columns are views, not copies
# Modifying the Series modifies the DataFrame unless explicitly copied

# ----------------------------
# DataFrame from Nested Dictionaries
# ----------------------------

populations = {"Ohio": {2000: 1.5, 2001: 1.7, 2002: 3.6},
               "Nevada": {2001: 2.4, 2002: 2.9}}

# Outer keys become columns, inner keys become row indices
frame3 = pd.DataFrame(populations)
print(frame3)

# Transpose swaps rows and columns
print(frame3.T)

# Explicit index
popdata = pd.DataFrame(populations, index=[2001, 2002, 2003])
print(popdata)

# Dictionary of Series
pdata = {"Ohio": frame3["Ohio"][:-1], "Nevada": frame3["Nevada"][:2]}
print(pd.DataFrame(pdata))

# Different input types for DataFrame:
# - 2D ndarray
# - Dictionary of arrays/lists/tuples
# - Dictionary of Series
# - Dictionary of dictionaries
# - List of dictionaries or Series
# - List of lists or tuples
# - Another DataFrame
# - NumPy MaskedArray

# Naming axes
frame3.index.name = "year"
frame3.columns.name = "state"
print(frame3)

# Convert DataFrame to NumPy array
print(frame3.to_numpy())
print(frame2.to_numpy())

# ----------------------------
# Index Objects
# ----------------------------

obj = pd.Series(range(3), index=["a", "b", "c"])
index = obj.index
print(index)
print(index[1:])

# Index objects are immutable: safe to share among data structures
labels = pd.Index(np.arange(3))
print(labels)

obj2 = pd.Series([1.5, -2.5, 0], index=labels)
print(obj2)
print(obj2.index is labels)  # Same Index object

# Membership
print("Ohio" in frame3.columns)
print(2003 in frame3.index)

# Create Index
print(pd.Index(['foo', 'bar', 'baz', 'qux']))

# Useful Index methods:
# append()       Concatenate with additional Index objects
# difference()   Compute set difference
# intersection() Compute set intersection
# union()        Compute set union
# isin()         Boolean array indicating membership
# delete()       Delete element at index i
# drop()         Delete passed values
# insert()       Insert element at index i
# is_monotonic   Check if index values are sorted
# is_unique      Check for duplicate values
# unique()       Return unique values
