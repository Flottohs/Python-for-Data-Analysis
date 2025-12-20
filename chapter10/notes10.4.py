# ============================================================
# 10.4 Group Transforms and “Unwrapped” GroupBys
# ============================================================

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# SETUP DATA
# ------------------------------------------------------------

# Create a simple DataFrame
# Each key ('a', 'b', 'c') appears multiple times
# value is a simple increasing sequence

df = pd.DataFrame({
    'key': ['a', 'b', 'c'] * 4,
    'value': np.arange(12.)
})

print(df)

# Create a GroupBy object
# We are grouping the 'value' column by 'key'
g = df.groupby('key')['value']

# ------------------------------------------------------------
# AGGREGATION (.agg / built-in reductions)
# ------------------------------------------------------------

# mean() COLLAPSES data
# Output has ONE value per group
print(g.mean())

# ------------------------------------------------------------
# TRANSFORM: SAME SHAPE AS ORIGINAL DATA
# ------------------------------------------------------------

# transform() must return the SAME LENGTH as each group
# Results are broadcast back to the original rows

# Custom function that computes group mean
def get_mean(group):
    return group.mean()

# Each value is replaced by its group's mean
print(g.transform(get_mean))

# apply() also works here, but does NOT guarantee same shape
print(g.apply(get_mean))

# Built-in string shortcuts are faster than custom functions
print(g.transform('mean'))

# ------------------------------------------------------------
# ELEMENT-WISE TRANSFORMS
# ------------------------------------------------------------

# transform can modify values element-by-element

def times_two(group):
    return group * 2

print(g.transform(times_two))

# ------------------------------------------------------------
# RANKING WITHIN GROUPS
# ------------------------------------------------------------

# Rank values INSIDE each group
# ascending=False => largest value gets rank 1

def get_ranks(group):
    return group.rank(ascending=False)

print(g.transform(get_ranks))

# ------------------------------------------------------------
# NORMALIZATION WITHIN GROUPS (Z-SCORE)
# ------------------------------------------------------------

# (value - group_mean) / group_std

def normalize(x):
    return (x - x.mean()) / x.std()

# transform guarantees same output shape
print(g.transform(normalize))

# apply gives the same numbers here,
# but this is NOT always guaranteed
print(g.apply(normalize))

# ------------------------------------------------------------
# FAST PATH: "UNWRAPPED" GROUP OPERATIONS
# ------------------------------------------------------------

# Built-in aggregations like 'mean' and 'std'
# have optimized implementations
print(g.transform('mean'))

# Manual normalization WITHOUT apply()
# This is an "unwrapped" group operation
normalized = (
    df['value'] - g.transform('mean')
) / g.transform('std')

print(normalized)

# ------------------------------------------------------------
# WHY UNWRAPPED OPERATIONS ARE IMPORTANT
# ------------------------------------------------------------
# Instead of:
#   g.apply(custom_function)
#
# We use:
#   vectorized math + groupby reductions
#
# Benefits:
#   - faster
#   - clearer
#   - more predictable output
# ------------------------------------------------------------

# ------------------------------------------------------------
# FINAL COMPARISON SUMMARY
# ------------------------------------------------------------
# .agg()       -> COLLAPSES data (one row per group)
# .transform() -> SAME SHAPE as original (broadcasted)
# .apply()     -> MOST FLEXIBLE, but SLOWEST
# ------------------------------------------------------------
