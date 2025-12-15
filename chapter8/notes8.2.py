import pandas as pd
import numpy as np
from pandas import MultiIndex # Explicitly import MultiIndex for clarity

# --- Core Functions for Combining Data ---

# pd.merge: Connects rows in DataFrames based on one or more keys (database-style join).
# pd.concat: Concatenates or “stacks” objects together along an axis (row or column-wise).
# pd.combine_first: Splices overlapping data to fill missing values in one object with values from another.


# ==============================================================================
# I. Database-Style DataFrame Joins (pd.merge)
# ==============================================================================

# --- Example 1: Many-to-One Join (Merging on a Shared Column) ---

df1 = pd.DataFrame({
    "key": ["b", "b", "a", "c", "a", "a", "b"],
    "data1": pd.Series(range(7), dtype="Int64")
})

df2 = pd.DataFrame({
    "key": ["a", "b", "d"],
    "data2": pd.Series(range(3), dtype="Int64")
})

print("--- DataFrames 1 & 2 ---")
print(df1)
print(df2)

# Default Merge (Inner Join): Uses overlapping column names ('key') as the join keys.
print("\n# Merge 1: Implicit 'on' (Inner Join)")
print(pd.merge(df1, df2))

# Good Practice: Explicitly specify the column(s) to join on.
print("\n# Merge 2: Explicit 'on=\"key\"'")
print(pd.merge(df1, df2, on="key"))


# --- Example 2: Merging on Differently Named Columns ---

df3 = pd.DataFrame({
    "lkey": ["b", "b", "a", "c", "a", "a", "b"],
    "data1": pd.Series(range(7), dtype="Int64")
})
df4 = pd.DataFrame({
    "rkey": ["a", "b", "d"],
    "data2": pd.Series(range(3), dtype="Int64")
})

print("\n--- DataFrames 3 & 4 ---")
print(df3)
print(df4)

# Merging using different key names.
print("\n# Merge 3: left_on='lkey', right_on='rkey' (Inner Join)")
print(pd.merge(df3, df4, left_on="lkey", right_on="rkey"))


# --- Example 3: Different Join Types ('how' argument) ---

# The 'how' argument controls which keys are included:
# how="inner" (Default): Intersection of keys.
# how="outer": Union of keys (combines left and right joins).
# how="left": All keys from the left table.
# how="right": All keys from the right table.

print("\n# Merge 4: how='outer' (union of all keys)")
print(pd.merge(df1, df2, how="outer"))

print("\n# Merge 5: how='outer' with different keys")
print(pd.merge(df3, df4, left_on="lkey", right_on="rkey", how="outer"))


# --- Example 4: Many-to-Many Joins ---

df1_m2m = pd.DataFrame({
    "key": ["b", "b", "a", "c", "a", "b"],
    "data1": pd.Series(range(6), dtype="Int64")
})

df2_m2m = pd.DataFrame({
    "key": ["a", "b", "a", "b", "d"],
    "data2": pd.Series(range(5), dtype="Int64")
})

print("\n--- DataFrames (Many-to-Many) ---")
print(df1_m2m)
print(df2_m2m)

# Many-to-Many: Key 'a' (2x in df1, 2x in df2) results in 4 combined rows.
print("\n# Merge 6: Many-to-Many (inner)")
print(pd.merge(df1_m2m, df2_m2m, how="inner"))

print("\n# Merge 7: Many-to-Many (left)")
print(pd.merge(df1_m2m, df2_m2m, on="key", how="left"))


# --- Example 5: Merging on Multiple Keys and Overlapping Columns ---

left = pd.DataFrame({
    "key1": ["foo", "foo", "bar"],
    "key2": ["one", "two", "one"],
    "lval": pd.Series([1, 2, 3], dtype='Int64')
})

right = pd.DataFrame({
    "key1": ["foo", "foo", "bar", "bar"],
    "key2": ["one", "one", "one", "two"],
    "rval": pd.Series([4, 5, 6, 7], dtype='Int64')
})

# Joins must match both 'key1' AND 'key2'.
print("\n# Merge 8: Multiple keys (outer)")
print(pd.merge(left, right, on=['key1', 'key2'], how='outer'))

# Overlapping columns (lval, rval) are NOT keys, but key1 and key2 are.
# If columns other than the key are shared, pandas adds default suffixes ('_x', '_y').
print("\n# Merge 9: Overlapping columns (default suffixes '_x', '_y')")
print(pd.merge(left, right, on="key1")) # Note: Merges only on 'key1' here.

# Custom Suffixes: Use the 'suffixes' argument.
print("\n# Merge 10: Overlapping columns (custom suffixes)")
print(pd.merge(left, right, on="key1", suffixes=("_left", "_right")))


# --- pd.merge() Argument Reference ---

"""
Argument | Description
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
left_on  | Columns in left DataFrame to use as join keys.
right_on | Analogous to left_on for the right DataFrame.
left_index | Use the row index in the left DataFrame as its join key.
right_index| Analogous to left_index.
sort     | Sort merged data lexicographically by join keys; False by default.
indicator| Adds a special column '_merge' (values: "left_only", "right_only", or "both").
"""


# ==============================================================================
# II. Merging on Index (left_index / right_index)
# ==============================================================================

# --- Example 6: Merging on Column (left) and Index (right) ---

left1 = pd.DataFrame({
    "key": ["a", "b", "a", "a", "b", "c"],
    "value": pd.Series(range(6), dtype="Int64")
})

right1 = pd.DataFrame({
    "group_val": [3.5, 7]
}, index=["a", "b"]) # Index labels are 'a' and 'b'

print("\n--- DataFrames 1 & 1 (for Index Merge) ---")
print(left1)
print(right1)

# Matches left1['key'] with right1's index. Default is 'inner' join.
print("\n# Merge 11: left_on='key', right_index=True (inner)")
print(pd.merge(left1, right1, left_on="key", right_index=True))

# Using 'outer' join to include key 'c' from left1.
print("\n# Merge 12: left_on='key', right_index=True (outer)")
print(pd.merge(left1, right1, left_on="key", right_index=True, how="outer"))


# --- Example 7: Merging on MultiIndex Keys ---

# Create a MultiIndex for the right DataFrame
righth_index = pd.MultiIndex.from_arrays([
    ["Nevada", "Nevada", "Ohio", "Ohio", "Ohio", "Ohio"],
    [2001, 2000, 2000, 2000, 2001, 2002]
], names=["key1", "key2"])

lefth = pd.DataFrame({
    "key1": ["Ohio", "Ohio", "Ohio", "Nevada", "Nevada"],
    "key2": [2000, 2001, 2002, 2001, 2002],
    "data": pd.Series(range(5), dtype="Int64")
})

righth = pd.DataFrame({
    "event1": pd.Series([0, 2, 4, 6, 8, 10], dtype="Int64", index=righth_index),
    "event2": pd.Series([1, 3, 5, 7, 9, 11], dtype="Int64", index=righth_index)
})

print("\n--- DataFrames (MultiIndex Merge) ---")
print(lefth)
print(righth)

# Matches left's ['key1', 'key2'] columns to righth's MultiIndex levels.
print("\n# Merge 13: Multi-Column on MultiIndex (inner)")
print(pd.merge(lefth, righth, left_on=["key1", "key2"], right_index=True))

print("\n# Merge 14: Multi-Column on MultiIndex (outer)")
print(pd.merge(lefth, righth, left_on=["key1", "key2"], right_index=True, how="outer"))


# --- Example 8: Merging on Both Indexes ---

left2 = pd.DataFrame(
    [[1., 2.], [3., 4.], [5., 6.]],
    index=["a", "c", "e"],
    columns=["Ohio", "Nevada"]
).astype("Int64")

right2 = pd.DataFrame(
    [[7., 8.], [9., 10.], [11., 12.], [13, 14]],
    index=["b", "c", "d", "e"],
    columns=["Missouri", "Alabama"]
).astype("Int64")

print("\n--- DataFrames 2 & 2 (Index-to-Index Merge) ---")
print(left2)
print(right2)

# Matches left2's index with right2's index, taking the union of indices (outer).
print("\n# Merge 15: Index-to-Index (outer)")
print(pd.merge(left2, right2, how='outer', left_index=True, right_index=True))


# ==============================================================================
# III. DataFrame.join() Method (Simplified Index Merging)
# ==============================================================================

# DataFrame.join() is a convenience method that simplifies merging by index.

# 1. Index-to-Index Join
print("\n# Join 1: Index-to-Index (outer)")
print(left2.join(right2, how='outer'))

# 2. Column-to-Index Join
# Defaults to a 'left' join.
print("\n# Join 2: Column on Left to Index on Right (default 'left' join)")
print(left1.join(right1, on='key'))

# 3. Joining a List of DataFrames (Index-to-Index)

another = pd.DataFrame([[7., 8.], [9., 10.], [11., 12.], [16., 17.]],
index=["a", "c", "e", "f"],
columns=["New York", "Oregon"])

print("\n--- DataFrame 'another' ---")
print(another)

# Inner Join (default): Intersection of indexes ('a', 'c', 'e')
print("\n# Join 3: Joining a list of DataFrames (inner)")
print(left2.join([right2, another]))

# Outer Join: Union of indexes ('a', 'b', 'c', 'd', 'e', 'f')
print("\n# Join 4: Joining a list of DataFrames (outer)")
print(left2.join([right2, another], how='outer'))


# ==============================================================================
# IV. Concatenating Along an Axis (pd.concat)
# ==============================================================================

# Concatenation/Stacking combines objects along an axis (rows or columns).

# NumPy array concatenation (default axis=0, or axis=1 for columns)
arr = np.arange(12).reshape((3, 4))
print("\n--- NumPy Array Concatenation ---")
print(arr)
print("# np.concatenate: axis=1 (columns)")
print(np.concatenate([arr, arr], axis=1))


# --- Concatenating Series (pd.concat) ---

s1 = pd.Series([0, 1], index=["a", "b"], dtype="Int64")
s2 = pd.Series([2, 3, 4], index=["c", "d", "e"], dtype="Int64")
s3 = pd.Series([5, 6], index=["f", "g"], dtype="Int64")

print("\n--- Series for Concatenation ---")
print(s1)
print(s2)
print(s3)

# Default: Concatenate along axis=0 (rows/index)
print("\n# Concat 1: axis=0 (default, stacking rows)")
print(pd.concat([s1, s2, s3]))

# Concatenate along axis=1 (columns/side-by-side)
print("\n# Concat 2: axis=columns (side-by-side)")
print(pd.concat([s1, s2, s3], axis="columns"))

s4 = pd.concat([s1, s3]) # Index: 'a', 'b', 'f', 'g'

# Concat with partial index overlap (outer join default)
print("\n# Concat 3: Partial index overlap (outer join default)")
print(pd.concat([s1, s4], axis="columns"))

# Forcing an 'inner' join keeps only common index labels ('a', 'b')
print("\n# Concat 4: Partial index overlap (inner join)")
print(pd.concat([s1, s4], axis="columns", join="inner"))

# --- Creating a Hierarchical Index with `keys` ---

# The 'keys' argument creates a MultiIndex to identify the source of each chunk.
result = pd.concat([s1, s1, s3], keys=["one", "two", "three"])
print("\n# Concat 5: Using 'keys' to create a MultiIndex")
print(result)

# Use unstack to convert the inner index level to columns
print("\n# Concat 6: Unstacking the MultiIndex result")
print(result.unstack())

# Using 'keys' for column concatenation (MultiIndex Columns)
print("\n# Concat 7: MultiIndex columns")
print(pd.concat([s1, s2, s3], axis="columns", keys=["one", "two", "three"]))


# --- Concatenating DataFrames (MultiIndex Columns) ---

df1_concat = pd.DataFrame(np.arange(6).reshape(3, 2), index=["a", "b", "c"], columns=["one", "two"])
df2_concat = pd.DataFrame(5 + np.arange(4).reshape(2, 2), index=["a", "c"], columns=["three", "four"])

print("\n--- DataFrames for Column Concatenation ---")
print(df1_concat)
print(df2_concat)

# Concatenating with MultiIndex columns
print("\n# Concat 8: MultiIndex Columns with 'keys'")
print(pd.concat([df1_concat, df2_concat], axis="columns", keys=["level1", "level2"]))

# Passing a dictionary uses the dictionary keys as the MultiIndex keys
print("\n# Concat 9: Using dictionary for 'keys'")
print(pd.concat({"level1": df1_concat, "level2": df2_concat}, axis="columns"))

# Adding names to the hierarchical index levels
print("\n# Concat 10: Naming MultiIndex levels")
print(pd.concat([df1_concat, df2_concat], axis="columns", keys=["level1", "level2"], names=["upper", "lower"]))

# --- Ignoring the Index ---

df1_rand = pd.DataFrame(np.random.standard_normal((3, 4)), columns=["a", "b", "c", "d"])
df2_rand = pd.DataFrame(np.random.standard_normal((2, 3)), columns=["b", "d", "a"])

print("\n--- DataFrames (Ignore Index Example) ---")
print(df1_rand)
print(df2_rand)

# ignore_index=True discards the original index and creates a new range index [0, 1, 2, ...]
print("\n# Concat 11: Stacking rows and ignoring index")
print(pd.concat([df1_rand, df2_rand], ignore_index=True))


# ==============================================================================
# V. Combining Data with Overlap (combine_first)
# ==============================================================================

# Used for "patching" missing values (NaN) in one dataset with non-missing
# values from another dataset, aligning by index.

# --- Example with Series ---

a = pd.Series([np.nan, 2.5, 0.0, 3.5, 4.5, np.nan], index=["f", "e", "d", "c", "b", "a"])
b = pd.Series([0., np.nan, 2., np.nan, np.nan, 5.], index=["a", "b", "c", "d", "e", "f"])

print("\n--- Series for Overlap Combination ---")
print(a)
print(b)

# combine_first: Aligns by index, then fills NaNs in the CALLING object (a) with values from the PASSED object (b).
print("\n# a.combine_first(b) (aligns indexes)")
print(a.combine_first(b))


# --- Example with DataFrames ---

df1_overlap = pd.DataFrame({
    "a": [1., np.nan, 5., np.nan],
    "b": [np.nan, 2., np.nan, 6.],
    "c": range(2, 18, 4)
})

df2_overlap = pd.DataFrame({
    "a": [5., 4., np.nan, 3., 7.],
    "b": [np.nan, 3., 4., 6., 8.]
})

print("\n--- DataFrames for combine_first ---")
print(df1_overlap)
print(df2_overlap)

# Fills NaNs in df1_overlap (the calling object) with aligned values from df2_overlap.
# Result includes the union of all indexes and columns.
print("\n# df1.combine_first(df2)")
print(df1_overlap.combine_first(df2_overlap))