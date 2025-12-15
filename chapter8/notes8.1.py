# 8.1 Hierarchical Indexing
#---------------------------
import pandas as pd
import numpy as np

# Create a Series with a hierarchical (multi-level) index
data = pd.Series(
    np.random.uniform(size=9),
    index=[["a", "a", "a", "b", "b", "c", "c", "d", "d"],
           [1, 2, 3, 1, 3, 1, 2, 2, 3]]
)

print("Hierarchical Series:")
print(data)

# Inspect the multi-level index
print("\nIndex of the Series:")
print(data.index)

# Select all data for outer-level index 'b'
print("\nData for outer-level index 'b':")
print(data['b'])

# Slice over outer-level index
print("\nSlice data from 'b' to 'c':")
print(data["b":"c"])

# Select multiple outer-level index values
print("\nSelect multiple outer-level indices ['b','d']:")
print(data.loc[["b", "d"]])

# Select all inner-level index = 2
print("\nSelect all inner-level index 2:")
print(data.loc[:, 2])

#---------------------------
# Reshaping with unstack and stack
#---------------------------
# Hierarchical indexing is important for reshaping and group-based operations
print("\nUnstacked DataFrame (convert inner level index to columns):")
print(data.unstack())

print("\nStacked back to original Series:")
print(data.unstack().stack())

#---------------------------
# Multi-level DataFrame
#---------------------------
frame = pd.DataFrame(
    np.arange(12).reshape((4, 3)),
    index=[["a", "a", "b", "b"], [1, 2, 1, 2]],
    columns=[["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]]
)

# Set names for index and columns
frame.index.names = ["key1", "key2"]
frame.columns.names = ["state", "color"]

print("\nHierarchical DataFrame:")
print(frame)

# Number of index levels
print("\nNumber of levels in index:")
print(frame.index.nlevels)

# Access top-level column
print("\nColumn 'Ohio':")
print(frame['Ohio'])

# Create a MultiIndex from arrays
multi_index = pd.MultiIndex.from_arrays(
    [["Ohio", "Ohio", "Colorado"], ["Green", "Red", "Green"]],
    names=["state", "color"]
)
print("\nMultiIndex from arrays:")
print(multi_index)

#---------------------------
# Reordering and Sorting Levels
#---------------------------
# Swap index levels
print("\nSwap index levels 'key1' and 'key2':")
print(frame.swaplevel('key1','key2'))

# Sort by inner level
print("\nSort index by inner level (level=1):")
print(frame.sort_index(level=1))

# Swap and sort
print("\nSwap levels and sort by outer level:")
print(frame.swaplevel(0,1).sort_index(level=0))

# Note: Performance improves if the hierarchical index is lexicographically sorted.

#---------------------------
# Summary Statistics by Level
#---------------------------
# Aggregate values by a specific index level
print("\nSum grouped by index level 'key2':")
print(frame.groupby(level="key2").sum())

# Aggregate across columns by a column index level
print("\nSum grouped by column level 'color':")
print(frame.groupby(level="color", axis="columns").sum())

#---------------------------
# Indexing with DataFrame columns
#---------------------------
frame = pd.DataFrame({
    "a": range(7),
    "b": range(7, 0, -1),
    "c": ["one", "one", "one", "two", "two", "two", "two"],
    "d": [0, 1, 2, 0, 1, 2, 3]
})

print("\nOriginal DataFrame:")
print(frame)

# Set a multi-level index
frame2 = frame.set_index(['c', 'd'])
print("\nDataFrame with multi-level index ['c','d']:")
print(frame2)

# Keep original columns when setting multi-level index
print("\nMulti-level index without dropping original columns:")
print(frame.set_index(["c", "d"], drop=False))

# Reset index back to default integer index
print("\nReset multi-level index back to columns:")
print(frame2.reset_index())