# ============================================================
# 10.5 Pivot Tables and Cross-Tabulation

import pandas as pd
import numpy as np
from io import StringIO

# ------------------------------------------------------------
# WHAT IS A PIVOT TABLE?
# ------------------------------------------------------------
# A pivot table:
# - reshapes data into a grid (rows x columns)
# - shows summary statistics (mean, count, sum, etc.)
# - is essentially a shortcut for groupby + unstack
# ------------------------------------------------------------

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

tips = pd.read_csv('tips.csv')
print(tips.head())

# Create derived column: tip percentage
tips['tip_pct'] = tips['tip'] / tips['total_bill']

# ------------------------------------------------------------
# BASIC PIVOT TABLE
# ------------------------------------------------------------

# Default aggfunc is mean
# Rows: day, smoker
# Values: selected numeric columns
print(
    tips.pivot_table(
        index=["day", "smoker"],
        values=["size", "tip", "tip_pct", "total_bill"]
    )
)

# ------------------------------------------------------------
# PIVOT TABLE WITH ROWS + COLUMNS
# ------------------------------------------------------------

# Put smoker in columns
# Put time and day in rows
print(
    tips.pivot_table(
        index=["time", "day"],
        columns="smoker",
        values=["tip_pct", "size"]
    )
)

# ------------------------------------------------------------
# ADDING TOTALS (MARGINS)
# ------------------------------------------------------------

# margins=True adds "All" rows and columns
# These represent aggregates over the entire axis
print(
    tips.pivot_table(
        index=["time", "day"],
        columns="smoker",
        values=["tip_pct", "size"],
        margins=True
    )
)

# ------------------------------------------------------------
# CHANGING AGGREGATION FUNCTION
# ------------------------------------------------------------

# aggfunc=len counts number of rows per group
# This produces a frequency table (cross-tab style)
print(
    tips.pivot_table(
        index=["time", "smoker"],
        columns="day",
        values="tip_pct",
        aggfunc=len,
        margins=True
    )
)

# ------------------------------------------------------------
# HANDLING MISSING COMBINATIONS
# ------------------------------------------------------------

# fill_value replaces NaN values in the result table
print(
    tips.pivot_table(
        index=["time", "size", "smoker"],
        columns="day",
        values="tip_pct",
        fill_value=0
    )
)

# ------------------------------------------------------------
# PIVOT TABLE ARGUMENT SUMMARY
# ------------------------------------------------------------
# values        -> columns to aggregate (default: all numeric)
# index         -> row group keys
# columns       -> column group keys
# aggfunc       -> aggregation function (mean by default)
# fill_value    -> value to replace missing entries
# dropna        -> drop columns with all NA values
# margins       -> add totals (All)
# margins_name  -> name of totals label (default: 'All')
# observed      -> show only observed categorical values
# ------------------------------------------------------------

# ------------------------------------------------------------
# CROSS-TABULATION (crosstab)
# ------------------------------------------------------------

# Crosstab computes FREQUENCIES (counts)
# It is a special case of pivot tables

raw_data = """Sample Nationality Handedness
1 USA Right-handed
2 Japan Left-handed
3 USA Right-handed
4 Japan Right-handed
5 Japan Left-handed
6 Japan Right-handed
7 USA Right-handed
8 USA Left-handed
9 Japan Right-handed
10 USA Right-handed"""

# Read text data into DataFrame
data = pd.read_table(StringIO(raw_data), sep="\s+")
print(data)

# Basic crosstab
print(
    pd.crosstab(
        data["Nationality"],
        data["Handedness"],
        margins=True
    )
)

# ------------------------------------------------------------
# MULTI-DIMENSIONAL CROSSTAB
# ------------------------------------------------------------

# First argument can be a list of arrays / Series
print(
    pd.crosstab(
        [tips["time"], tips["day"]],
        tips["smoker"],
        margins=True
    )
)

