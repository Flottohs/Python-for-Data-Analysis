# 5.2 Essential Functionality - pandas
# Author: Notes and examples from "Python for Data Analysis" by Wes McKinney
# Purpose: Demonstrates reindexing, selection, arithmetic, mapping, sorting, and handling of duplicate labels in Series and DataFrames.

import pandas as pd
import numpy as np
from sympy import limit

# ----------------------------
# Reindexing
# ----------------------------

# Reindexing allows you to change the row/column labels of a Series or DataFrame.
# If a label is not present in the original object, pandas will introduce missing values (NaN) unless you specify a fill method.

obj = pd.Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
print("Original Series:\n", obj)

# Reindex with new labels including a missing value 'e'
obj2 = obj.reindex(['a', 'b', 'c', 'd', 'e'])
print("\nReindexed Series with a missing index 'e':\n", obj2)

# Forward-fill example: missing values are filled with the previous valid entry
obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
print("\nForward fill example:\n", obj3.reindex(range(6), method='ffill'))

# ----------------------------
# DataFrame Reindexing
# ----------------------------
frame = pd.DataFrame(np.arange(9).reshape((3,3)),
                     index=['a', 'c', 'd'],
                     columns=['Ohio', 'Texas', 'California'])
print("\nOriginal DataFrame:\n", frame)

# Reindex rows: adds missing row 'b' with NaNs
frame2 = frame.reindex(['a', 'b', 'c', 'd'])
print("\nDataFrame with reindexed rows:\n", frame2)

# Reindex columns
states = ['Texas', 'Utah', 'California']
print("\nDataFrame with reindexed columns:\n", frame.reindex(columns=states))
# Alternative syntax using axis parameter
print("\nDataFrame with reindexed columns using axis keyword:\n", frame.reindex(states, axis='columns'))

# Reindex parameters explanation:
# labels - new sequence for index
# index - new row labels
# columns - new column labels
# axis - "index" or "columns"
# method - "ffill" or "bfill" for filling missing values
# fill_value - value used for missing data
# limit - maximum number of elements to fill
# tolerance - max difference for inexact matches
# level - used for MultiIndex
# copy - whether to copy underlying data

# ----------------------------
# Selection with loc and iloc
# ----------------------------
# loc: label-based selection (select rows/columns by labels)
# iloc: integer-based selection (select rows/columns by integer position)

print("\nLabel-based selection using loc:\n", frame.loc[['a', 'd', 'c'], ['California', 'Texas']])

# ----------------------------
# Dropping Entries
# ----------------------------
# Drop removes entries from Series or DataFrame

obj = pd.Series(np.arange(5.), index=['a','b','c','d','e'])
print("\nOriginal Series:\n", obj)
print("Drop 'c':\n", obj.drop('c'))
print("Drop multiple labels ['d','c']:\n", obj.drop(['d','c']))

data = pd.DataFrame(np.arange(16).reshape((4,4)),
                    index=['Ohio','Colorado','Utah','New York'],
                    columns=['one','two','three','four'])
print("\nOriginal DataFrame:\n", data)
print("Drop rows ['Colorado','Ohio']:\n", data.drop(index=["Colorado","Ohio"]))
print("Drop column 'two':\n", data.drop(columns=['two']))
print("Drop multiple columns using axis=1:\n", data.drop(['two','four'], axis='columns'))

# ----------------------------
# Indexing, Selection, and Filtering
# ----------------------------
obj = pd.Series(np.arange(4.), index=['a','b','c','d'])
print("\nSeries Indexing Examples:")
print("obj['b'] ->", obj['b'])           # single label
print("obj.iloc[1] ->", obj.iloc[1])     # integer position
print("obj.iloc[2:4] ->", obj.iloc[2:4]) # slicing by integer position
print("obj[['b','a','d']] ->", obj[['b','a','d']]) # list of labels
print("obj[obj < 2] ->", obj[obj < 2])   # boolean filtering

# Label-based slicing includes the endpoint
obj2 = pd.Series([1, 2, 3], index=['a','b','c'])
print("\nLabel slicing obj2['b':'c'] ->", obj2['b':'c'])
obj2.loc['b':'c'] = 5
print("After assignment obj2.loc['b':'c'] = 5 ->", obj2)

# DataFrame selection examples
print("\nDataFrame selection examples:")
print("data['two'] ->", data['two'])
print("data[['three','one']] ->\n", data[['three','one']])
print("data[:2] ->\n", data[:2])
print("data[data['three']>5] ->\n", data[data["three"]>5])

# Boolean assignment modifies values
data[data < 5] = 0
print("DataFrame after boolean assignment:\n", data)

# loc selections
print("data.loc['Colorado'] ->\n", data.loc['Colorado'])
print("data.loc['Colorado',['two','three']] ->\n", data.loc['Colorado',['two','three']])

# iloc selections
print("data.iloc[2] ->\n", data.iloc[2])
print("data.iloc[2,[3,0,1]] ->\n", data.iloc[2,[3,0,1]])
print("data.iloc[[1,2],[3,0,1]] ->\n", data.iloc[[1,2],[3,0,1]])

# Boolean arrays can be used with loc but not iloc
print("data.loc[data.three >= 2] ->\n", data.loc[data.three >= 2])

# ----------------------------
# Integer Indexing Pitfalls
# ----------------------------
ser = pd.Series(np.arange(3.))
ser2 = pd.Series(np.arange(3.), index=['a','b','c'])
print("\nInteger Indexing Pitfalls:")
print(ser2.iloc[-1])   # integer position safe
print(ser2[:2])        # label-based slicing

# ----------------------------
# Chained Indexing Pitfalls
# ----------------------------
data.loc[:, "one"] = 1
data.iloc[2] = 5
data.loc[data["four"] > 5] = 3
data.loc[data.three == 5, "three"] = 6
print("\nDataFrame after chained indexing updates:\n", data)

# ----------------------------
# Arithmetic and Data Alignment
# ----------------------------
s1 = pd.Series([7.3, -2.5, 3.4, 1.5], index=["a", "c", "d", "e"])
s2 = pd.Series([-2.1, 3.6, -1.5, 4, 3.1], index=["a", "c", "e", "f", "g"])
print("\nSeries Arithmetic Alignment:")
print(s1 + s2)

# DataFrame arithmetic with missing labels
df1 = pd.DataFrame(np.arange(12.).reshape((3,4)), columns=list("abcd"))
df2 = pd.DataFrame(np.arange(20.).reshape((4,5)), columns=list("abcde"))
df2.loc[1,"b"] = np.nan
print("\nDataFrame with NaN:\n", df2)
print("df1 + df2 (NaNs appear where labels don't match):\n", df1 + df2)
print("df1.add(df2, fill_value=0) ->\n", df1.add(df2, fill_value=0))
print("df1.reindex(columns=df2.columns, fill_value=0) ->\n", df1.reindex(columns=df2.columns, fill_value=0))

# ----------------------------
# Operations Between DataFrame and Series
# ----------------------------
frame = pd.DataFrame(np.arange(12.).reshape((4,3)), columns=list("bde"),
                     index=['Utah','Ohio','Texas','Oregon'])
series = frame.iloc[0]
print("\nDataFrame- Series Operations:")
print(frame - series)

# ----------------------------
# Function Application and Mapping
# ----------------------------
print("\nFunction Application and Mapping:")
print(np.abs(frame))   # element-wise absolute value

# Applying a function along an axis
def f1(x):
    return x.max() - x.min()

print("Apply f1 along columns:\n", frame.apply(f1))          # axis=0
print("Apply f1 along rows:\n", frame.apply(f1, axis='columns')) # axis=1

def f2(x):
    return pd.Series([x.min(), x.max()], index=["min","max"])
print("Apply f2 to DataFrame:\n", frame.apply(f2))

# Mapping element-wise Python functions
def my_format(x):
    return f"{x:.2f}"

print("Map formatting to entire frame:\n", frame.map(my_format))
print("Map formatting to a single Series (column):\n", frame["e"].map(my_format))

# ----------------------------
# Sorting and Ranking
# ----------------------------
obj = pd.Series([4, 7, -3, 2], index=list('abcd'))
print("\nSorted Series:\n", obj.sort_values())

obj = pd.Series([4, np.nan, 7, np.nan, -3, 2])
print("Sort Series with NaNs first:\n", obj.sort_values(na_position='first'))

frame = pd.DataFrame({"b": [4.3, 7, -3, 2], "a": [0,1,0,1], "c": [-2,5,8,-2.5]})
print("Rank DataFrame along columns:\n", frame.rank(axis='columns'))

# Ranking methods:
# "average": default, assign average rank to ties
# "min": minimum rank to all tied entries
# "max": maximum rank to all tied entries
# "first": assign ranks in order of appearance
# "dense": like min, but ranks always increase by 1 between groups

# ----------------------------
# Axis Indexes with Duplicate Labels
# ----------------------------
obj = pd.Series(np.arange(5), index=["a","a","b","b","c"])
print("\nDuplicate Labels in Series:")
print("Is unique?", obj.index.is_unique)
print("obj['a'] ->", obj['a'])
print("obj['c'] ->", obj['c'])

df = pd.DataFrame(np.random.standard_normal((5,3)), index=["a","a","b","b","c"])
print("\nDuplicate Labels in DataFrame:")
print("df.loc['b'] ->\n", df.loc['b'])
print("df.loc['c'] ->\n", df.loc['c'])