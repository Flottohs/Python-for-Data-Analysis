# ============================================================
# 8.3 Reshaping with Hierarchical Indexing (FULL VS CODE NOTES)
# ============================================================


# ------------------------------------------------------------
# Core idea:
# Hierarchical (MultiIndex) structures allow pandas to reshape
# data in a predictable, reversible way.
#
# There are TWO fundamental reshaping operations:
#   1. stack()   -> columns go INTO the index (wide -> long)
#   2. unstack() -> index levels move INTO columns (long -> wide)
# ------------------------------------------------------------

import pandas as pd
import numpy as np

# NOTE on future_stack:
# future_stack=True enforces the *new* pandas behavior where
# rows consisting only of NA values are NEVER introduced.
# This avoids subtle bugs and is now the recommended usage.

# ------------------------------------------------------------
# BASIC STACK / UNSTACK EXAMPLE
# ------------------------------------------------------------

# Create a simple DataFrame with NAMED index and columns
# Naming levels is important for clarity when stacking/unstacking

data = pd.DataFrame(
    np.arange(6).reshape((2, 3)),
    index=pd.Index(["Ohio", "Colorado"], name="state"),
    columns=pd.Index(["one", "two", "three"], name="number")
)

print(data)

# ------------------------------------------------------------
# stack(): COLUMNS -> ROWS
# ------------------------------------------------------------

# stack moves the column labels into the index
# Result is a Series with a MultiIndex (state, number)

result = data.stack(future_stack=True)
print(result)

# ------------------------------------------------------------
# unstack(): ROWS -> COLUMNS
# ------------------------------------------------------------

# unstack with no arguments reverses stack completely
print(result.unstack())

# unstack(level=0) moves ONLY the first index level (state)
# into the columns
print(result.unstack(level=0))

# ------------------------------------------------------------
# STACKING WITH PARTIALLY OVERLAPPING INDEXES
# ------------------------------------------------------------

# Two Series with overlapping but NOT identical indexes
s1 = pd.Series([0, 1, 2, 3], index=["a", "b", "c", "d"], dtype="Int64")
s2 = pd.Series([4, 5, 6], index=["c", "d", "e"], dtype="Int64")

# Concatenate with keys to create a hierarchical index
# Outer level identifies the source Series

data2 = pd.concat([s1, s2], keys=["one", "two"])

print(data2)

# unstack creates a DataFrame
# Missing combinations become NaN
print(data2.unstack())

# ------------------------------------------------------------
# RESTACKING BEHAVIOR WITH MISSING VALUES
# ------------------------------------------------------------

# future_stack=True DROPS rows that would be all-NA
print(data2.unstack().stack(future_stack=True))

# dropna=False FORCES pandas to keep all combinations
# (including NA values)
print(data2.unstack().stack(dropna=False))

# ------------------------------------------------------------
# STACKING / UNSTACKING DATAFRAMES
# ------------------------------------------------------------

# Build a DataFrame from the stacked result
# Column index is also named ("side")

df = pd.DataFrame(
    {"left": result, "right": result + 5},
    columns=pd.Index(["left", "right"], name="side")
)

print(df)

# unstack(level='state'):
# - Moves the 'state' index level into the columns
# - Produces hierarchical columns
print(df.unstack(level="state"))

# This chain shows a FULL reshape cycle:
# 1. state -> columns
# 2. side  -> back into index
print(
    df
    .unstack(level="state")
    .stack(level="side", future_stack=True)
)

# ------------------------------------------------------------
# PIVOTING: LONG -> WIDE (REAL DATA EXAMPLE)
# ------------------------------------------------------------

# Load macroeconomic data
data = pd.read_csv("PFDA/chapter8/data/macrodata.csv")

# Keep only relevant columns
data = data.loc[:, ["year", "quarter", "realgdp", "infl", "unemp"]]
print(data.head())

# ------------------------------------------------------------
# CREATE A PERIOD-BASED TIME INDEX
# ------------------------------------------------------------

# PeriodIndex represents time spans (quarters here)
periods = pd.PeriodIndex(
    year=data.pop("year"),
    quarter=data.pop("quarter"),
    name="date"
)

print(periods)

# Convert periods to timestamps for time-series indexing
data.index = periods.to_timestamp("D")
print(data.head())

# ------------------------------------------------------------
# WIDE FORMAT DATA
# ------------------------------------------------------------

# Each variable is its own column
# Columns are named for later stacking

data = data.reindex(columns=["realgdp", "infl", "unemp"])
data.columns.name = "item"
print(data.head())

# ------------------------------------------------------------
# CONVERT WIDE -> LONG USING stack()
# ------------------------------------------------------------

# stack moves columns into the index
# reset_index flattens it back into columns
# rename gives the stacked values a meaningful name

long_data = (
    data
    .stack()
    .reset_index()
    .rename(columns={0: "value"})
)

print(long_data.head())

# ------------------------------------------------------------
# LONG FORMAT EXPLANATION
# ------------------------------------------------------------
# Each row = ONE observation
# Columns:
#   - date  : when the measurement was taken
#   - item  : which variable (realgdp, infl, unemp)
#   - value : the actual number
#
# This format is:
#   - database-friendly
#   - flexible
#   - easy to extend with new variables
# ------------------------------------------------------------

# ------------------------------------------------------------
# pivot(): LONG -> WIDE
# ------------------------------------------------------------

pivoted = long_data.pivot(
    index="date",
    columns="item",
    values="value"
)

print(pivoted.head())

# ------------------------------------------------------------
# PIVOTING WITH MULTIPLE VALUE COLUMNS
# ------------------------------------------------------------

# Add a second value column
long_data["value2"] = np.random.standard_normal(len(long_data))
print(long_data[:10])

# Omitting values= creates hierarchical columns
pivoted = long_data.pivot(index="date", columns="item")
print(pivoted.head())

# Select a single top-level column
print(pivoted["value"].head())

# ------------------------------------------------------------
# pivot == set_index + unstack
# ------------------------------------------------------------

unstacked = (
    long_data
    .set_index(["date", "item"])
    .unstack(level="item")
)

print(unstacked.head())

# ------------------------------------------------------------
# PIVOTING WIDE -> LONG USING melt()
# ------------------------------------------------------------

# melt is the INVERSE of pivot
# It merges multiple columns into one

# Example DataFrame
df = pd.DataFrame({
    "key": ["foo", "bar", "baz"],
    "A": [1, 2, 3],
    "B": [4, 5, 6],
    "C": [7, 8, 9]
})

print(df)

# id_vars specify which columns identify groups
melted = pd.melt(df, id_vars=["key"])
print(melted)

# melt + pivot restores original structure
reshaped = melted.pivot(
    index="key",
    columns="variable",
    values="value"
)

print(reshaped)

# reset_index moves index back into a column
print(reshaped.reset_index())

# ------------------------------------------------------------
# melt WITH SELECTED VALUE COLUMNS
# ------------------------------------------------------------

print(pd.melt(df, id_vars="key", value_vars=["A", "B"]))

# melt WITHOUT ID VARIABLES
print(pd.melt(df, value_vars=["A", "B", "C"]))

# melt INCLUDING NON-NUMERIC DATA
print(pd.melt(df, value_vars=["key", "A", "B"]))


