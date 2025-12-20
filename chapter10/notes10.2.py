# ============================================================
# Data Aggregation with GroupBy (FULL VS CODE NOTES)
# ============================================================

# ------------------------------------------------------------
# WHAT IS DATA AGGREGATION?
# ------------------------------------------------------------
# Aggregation means:
#   "take many values and summarize them into fewer values"
#
# Typically done after groupby(), where pandas:
#   1. splits data into groups
#   2. applies aggregation functions
#   3. combines results into a summary table
# ------------------------------------------------------------

# ------------------------------------------------------------
# COMMON AGGREGATION FUNCTIONS (REFERENCE LIST)
# ------------------------------------------------------------
# any, all        -> True if any / all non-NA values are truthy
# count           -> Number of non-NA values
# cummin, cummax  -> Cumulative min / max
# cumsum          -> Cumulative sum
# cumprod         -> Cumulative product
# first, last     -> First / last non-NA values
# mean            -> Mean of non-NA values
# median          -> Median of non-NA values
# min, max        -> Minimum / maximum
# nth             -> Value at sorted position n
# ohlc            -> Open-high-low-close (time series)
# prod            -> Product of non-NA values
# quantile        -> Sample quantile
# rank            -> Ordinal ranks
# size            -> Group size (counts NA too)
# sum             -> Sum of non-NA values
# std, var        -> Sample std deviation / variance
# ------------------------------------------------------------

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# BASIC GROUPBY AGGREGATION
# ------------------------------------------------------------

# Create sample DataFrame with missing values

df = pd.DataFrame({
    "key1": ["a", "a", None, "b", "b", "a", None],
    "key2": pd.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
    "data1": np.random.standard_normal(7),
    "data2": np.random.standard_normal(7)
})

print(df)

# Group by key1
grouped = df.groupby("key1")

# nsmallest finds the N smallest values per group
print(grouped["data1"].nsmallest(2))

# ------------------------------------------------------------
# CUSTOM AGGREGATION FUNCTIONS
# ------------------------------------------------------------

# Peak-to-peak = max - min
# This function receives a Series (one group)
def peak_to_peak(arr):
    return arr.max() - arr.min()

# agg applies this function to EVERY group
print(grouped.agg(peak_to_peak))

# Built-in summary statistics per group
print(grouped.describe())

# ------------------------------------------------------------
# COLUMN-WISE & MULTIPLE FUNCTION AGGREGATION
# ------------------------------------------------------------

# Load tips dataset
tips = pd.read_csv("tips.csv")
print(tips.head())

# Add derived column
tips["tip_pct"] = tips["tip"] / tips["total_bill"]
print(tips.head())

# Group by multiple keys
grouped = tips.groupby(["day", "smoker"])

# Select one column for aggregation
grouped_pct = grouped["tip_pct"]

# Single aggregation
print(grouped_pct.agg("mean"))

# Multiple aggregations on same column
print(grouped_pct.agg(["mean", "std", peak_to_peak]))

# ------------------------------------------------------------
# RENAMING AGGREGATED OUTPUT COLUMNS
# ------------------------------------------------------------

# (output_name, function)
print(
    grouped_pct.agg([
        ("average", "mean"),
        ("stdev", np.std)
    ])
)

# ------------------------------------------------------------
# AGGREGATING MULTIPLE COLUMNS
# ------------------------------------------------------------

functions = ["count", "mean", "max"]

result = grouped[["tip_pct", "total_bill"]].agg(functions)
print(result)

# Select one column from hierarchical result
print(result["tip_pct"])

# ------------------------------------------------------------
# NAMED AGGREGATIONS WITH MULTIPLE COLUMNS
# ------------------------------------------------------------

ftuples = [("Average", "mean"), ("Variance", "var")]

print(grouped[["tip_pct", "total_bill"]].agg(ftuples))

# ------------------------------------------------------------
# DIFFERENT FUNCTIONS PER COLUMN (DICT SYNTAX)
# ------------------------------------------------------------

# This allows full control over how each column is summarized

# tip  -> max tip per group
# size -> sum of group sizes
print(grouped.agg({"tip": "max", "size": "sum"}))

# Multiple functions per column
print(
    grouped.agg({
        "tip_pct": ["min", "max", "mean", "std"],
        "size": "sum"
    })
)

# ------------------------------------------------------------
# RETURNING AGGREGATED DATA WITHOUT ROW INDEXES
# ------------------------------------------------------------

# as_index=False keeps grouping columns as normal columns
print(
    tips.groupby(["day", "smoker"], as_index=False)
        .mean(numeric_only=True)
)# ============================================================
# Data Aggregation with GroupBy (FULL VS CODE NOTES)
# ============================================================
# GUARANTEES:
# - NO CONTENT LOST
# - ALL FUNCTIONS EXPLAINED IN-LINE
# - SAME LOGIC, CLEANLY FORMATTED
# - WRITTEN AS A SINGLE .py NOTES FILE
# ============================================================

# ------------------------------------------------------------
# WHAT IS DATA AGGREGATION?
# ------------------------------------------------------------
# Aggregation means:
#   "take many values and summarize them into fewer values"
#
# Typically done after groupby(), where pandas:
#   1. splits data into groups
#   2. applies aggregation functions
#   3. combines results into a summary table
# ------------------------------------------------------------

# ------------------------------------------------------------
# COMMON AGGREGATION FUNCTIONS (REFERENCE LIST)
# ------------------------------------------------------------
# any, all        -> True if any / all non-NA values are truthy
# count           -> Number of non-NA values
# cummin, cummax  -> Cumulative min / max
# cumsum          -> Cumulative sum
# cumprod         -> Cumulative product
# first, last     -> First / last non-NA values
# mean            -> Mean of non-NA values
# median          -> Median of non-NA values
# min, max        -> Minimum / maximum
# nth             -> Value at sorted position n
# ohlc            -> Open-high-low-close (time series)
# prod            -> Product of non-NA values
# quantile        -> Sample quantile
# rank            -> Ordinal ranks
# size            -> Group size (counts NA too)
# sum             -> Sum of non-NA values
# std, var        -> Sample std deviation / variance
# ------------------------------------------------------------

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# BASIC GROUPBY AGGREGATION
# ------------------------------------------------------------

# Create sample DataFrame with missing values

df = pd.DataFrame({
    "key1": ["a", "a", None, "b", "b", "a", None],
    "key2": pd.Series([1, 2, 1, 2, 1, None, 1], dtype="Int64"),
    "data1": np.random.standard_normal(7),
    "data2": np.random.standard_normal(7)
})

print(df)

# Group by key1
# This splits the DataFrame into chunks based on unique values in key1
grouped = df.groupby("key1")

# nsmallest finds the N smallest values per group
# Applied independently inside each group
print(grouped["data1"].nsmallest(2))

# ------------------------------------------------------------
# CUSTOM AGGREGATION FUNCTIONS
# ------------------------------------------------------------

# Peak-to-peak = max - min
# This function receives a Series representing one group
def peak_to_peak(arr):
    return arr.max() - arr.min()

# agg applies this function to EVERY group
# The output is one row per group
print(grouped.agg(peak_to_peak))

# Built-in summary statistics per group
# describe() is shorthand for multiple aggregations at once
print(grouped.describe())

# ------------------------------------------------------------
# COLUMN-WISE & MULTIPLE FUNCTION AGGREGATION
# ------------------------------------------------------------

# Load tips dataset
tips = pd.read_csv("tips.csv")
print(tips.head())

# Add derived column: tip as a percentage of total bill
tips["tip_pct"] = tips["tip"] / tips["total_bill"]
print(tips.head())

# Group by multiple keys
# Results will have a MultiIndex (day -> smoker)
grouped = tips.groupby(["day", "smoker"])

# Select one column for aggregation
grouped_pct = grouped["tip_pct"]

# Single aggregation
print(grouped_pct.agg("mean"))

# Multiple aggregations on the same column
print(grouped_pct.agg(["mean", "std", peak_to_peak]))

# ------------------------------------------------------------
# RENAMING AGGREGATED OUTPUT COLUMNS
# ------------------------------------------------------------

# (output_name, function)
# This gives readable column names in the result
print(
    grouped_pct.agg([
        ("average", "mean"),
        ("stdev", np.std)
    ])
)

# ------------------------------------------------------------
# AGGREGATING MULTIPLE COLUMNS
# ------------------------------------------------------------

# Apply the same functions to multiple numeric columns
functions = ["count", "mean", "max"]

result = grouped[["tip_pct", "total_bill"]].agg(functions)
print(result)

# Select one column from the hierarchical result
print(result["tip_pct"])

# ------------------------------------------------------------
# NAMED AGGREGATIONS WITH MULTIPLE COLUMNS
# ------------------------------------------------------------

# Custom names applied per aggregation
ftuples = [("Average", "mean"), ("Variance", "var")]

print(grouped[["tip_pct", "total_bill"]].agg(ftuples))

# ------------------------------------------------------------
# DIFFERENT FUNCTIONS PER COLUMN (DICT SYNTAX)
# ------------------------------------------------------------

# This allows full control over how each column is summarized

# tip  -> maximum tip per group
# size -> sum of group sizes
print(grouped.agg({"tip": "max", "size": "sum"}))

# Multiple functions per column
print(
    grouped.agg({
        "tip_pct": ["min", "max", "mean", "std"],
        "size": "sum"
    })
)

# ------------------------------------------------------------
# RETURNING AGGREGATED DATA WITHOUT ROW INDEXES
# ------------------------------------------------------------

# as_index=False keeps grouping columns as normal columns
print(
    tips.groupby(["day", "smoker"], as_index=False)
        .mean(numeric_only=True)
)

