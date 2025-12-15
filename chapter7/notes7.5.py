# ============================================================
# 7.5 Categorical Data — FULL NOTES (clean, detailed, VS Code format)
# ============================================================

import pandas as pd
import numpy as np
import time

# ------------------------------------------------------------
# Background and Motivation
# ------------------------------------------------------------
# Many datasets contain repeated string labels (like "apple", "orange").
# Repeated strings are inefficient: each string is stored in memory separately.
# A better representation is "categorical encoding":
#   - store a list of unique values (categories)
#   - store the data as integer codes referencing those categories.

values = pd.Series(['apple', 'orange', 'apple', 'apple'] * 2)
print(values)

# Unique categories present in the data
print(pd.unique(values))

# Count frequencies
print(pd.value_counts(values))

# Example: Representing using integer codes instead of strings
values = pd.Series([0, 1, 0, 0] * 2)
dim = pd.Series(['apple', 'orange'])

print(values)
print(dim)

# Convert integer codes back to strings using .take()
print(dim.take(values))

# Terminology:
# - "categories" / "levels": the unique set of string values
# - "codes": the integer representation for each element
# - "categorical representation": storing (codes + categories)

# ------------------------------------------------------------
# Categorical Extension Type in pandas
# ------------------------------------------------------------

fruits = ['apple', 'orange', 'apple', 'apple'] * 2
N = len(fruits)
rng = np.random.default_rng(seed=12345)

df = pd.DataFrame(
    {
        'fruit': fruits,
        'basket_id': np.arange(N),
        'count': rng.integers(3, 15, size=N),
        'weight': rng.uniform(0, 4, size=N),
    },
    columns=['basket_id', 'fruit', 'count', 'weight']
)

print(df)

# Convert a column to pandas categorical type
fruit_cat = df['fruit'].astype('category')
print(fruit_cat)

# Access the underlying Categorical object
c = fruit_cat.array
print(type(c))

# Categorical attributes:
print(c.categories)  # unique values
print(c.codes)       # integer codes 0,1,...

# Dictionary form: code -> category name
print(dict(enumerate(c.categories)))

# Assigning the converted column back to the DataFrame:
df['fruit'] = df['fruit'].astype('category')
print(df['fruit'])

# Creating a Categorical manually from a list
my_categories = pd.Categorical(['foo', 'bar', 'baz', 'foo', 'bar'])
print(my_categories)

# Creating from codes manually (external encoded data)
categories = ['foo', 'bar', 'baz']
codes = [0, 1, 2, 0, 0, 1]

print('\n' * 15)
my_cats_2 = pd.Categorical.from_codes(codes, categories)
print(my_cats_2)

# Creating an ordered categorical
ordered_cat = pd.Categorical.from_codes(codes, categories, ordered=True)
print(ordered_cat)

# Convert an unordered categorical to ordered
print(my_cats_2.as_ordered())

# ------------------------------------------------------------
# Computations with Categoricals
# ------------------------------------------------------------
# Categories behave mostly like arrays of strings, but faster for groupby and memory.

rng = np.random.default_rng(seed=12345)
draws = rng.standard_normal(1000)
print(draws[:5])

# Use qcut to perform quartile binning — returns a categorical
bins = pd.qcut(draws, 4)
print(bins)

# Add labels instead of interval ranges
bins = pd.qcut(draws, 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
print(bins)
print(bins.codes[:10])

# Turn bins into a Series for groupby
bins = pd.Series(bins, name='quartile')
print(bins)

# Group values by quartile, compute count/min/max
results = (
    pd.Series(draws)
      .groupby(bins, observed=False)
      .agg(['count', 'min', 'max'])
      .reset_index()
)
print(results['quartile'])

# ------------------------------------------------------------
# Performance and Memory Benefits
# ------------------------------------------------------------

N = 10_000_000
labels = pd.Series(['foo', 'bar', 'baz', 'qux'] * (N // 4))

categories = labels.astype('category')

print("label memory")
print(labels.memory_usage(deep=True))

print("category memory")
print(categories.memory_usage(deep=True))

# Timing comparisons

# Convert to categorical
start = time.time()
categories = labels.astype('category')
end = time.time()
print(f"Time to convert to categorical: {end - start:.3f} seconds")

# Value counts on raw strings
start = time.time()
counts_labels = labels.value_counts()
end = time.time()
print(f"Value counts on labels: {end - start:.3f} seconds")

# Value counts on categoricals
start = time.time()
counts_categories = categories.value_counts()
end = time.time()
print(f"Value counts on categories: {end - start:.3f} seconds")

print(f"Memory usage - labels: {labels.memory_usage(deep=True)} bytes")
print(f"Memory usage - categories: {categories.memory_usage(deep=True)} bytes")

# ------------------------------------------------------------
# Categorical Methods
# ------------------------------------------------------------

s = pd.Series(['a', 'b', 'c', 'd'] * 2)
cat_s = s.astype('category')
print(cat_s)

# Access codes and categories
print(cat_s.cat.codes)
print(cat_s.cat.categories)

# Expand categories — even ones not used in data
actual_categories = ['a', 'b', 'c', 'd', 'e']
cat_s2 = cat_s.cat.set_categories(actual_categories)
print(cat_s2)

# value_counts respects the extra unused category 'e'
print(cat_s.value_counts())
print(cat_s2.value_counts())

# Remove categories not present in filtered data
cat_s3 = cat_s[cat_s.isin(['a', 'b'])]
print(cat_s3)
print(cat_s3.cat.remove_unused_categories())

# Common Categorical Methods:
# ------------------------------------------------------------
# add_categories: add new empty categories to the end
# as_ordered: mark categories as ordered
# as_unordered: mark categories as unordered
# remove_categories: remove certain categories (removed values become NaN)
# remove_unused_categories: drop categories not observed in data
# rename_categories: rename categories (must keep same number)
# reorder_categories: reorder categories and optionally make ordered
# set_categories: replace entire category set (can add/remove)

# ------------------------------------------------------------
# Creating Dummy Variables (One-Hot Encoding)
# ------------------------------------------------------------

cat_s = pd.Series(['a', 'b', 'c', 'd'] * 2, dtype='category')

# Convert categorical to one-hot encoded DataFrame
print(pd.get_dummies(cat_s))