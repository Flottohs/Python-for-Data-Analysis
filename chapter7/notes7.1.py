# ============================================================
# 7.x Handling Missing Values
# ============================================================

import numpy as np
import pandas as pd

# ------------------------------------------------------------
# Recognizing Missing Data
# ------------------------------------------------------------
# pandas uses two markers for missing values:
# - np.nan (float-based missing value)
# - pd.NA (nullable dtype missing value)
# Both are treated as "missing"/NA.

float_data = pd.Series([1.2, -3.5, np.nan, 0])
print(float_data)

# isna() → True where value is missing
print(float_data.isna())

string_data = pd.Series(["aardvark", np.nan, None, "avocado"])
print(string_data)
print(string_data.isna())

# Nullable dtypes (Float64, Int64, boolean, string) also support missing values:
float_data = pd.Series([1, 2, None], dtype="float64")
print(float_data.isna())

# ------------------------------------------------------------
# Key Methods for Missing Data
# ------------------------------------------------------------
# isna()     → Boolean mask of missing entries
# notna()    → Opposite of isna()
# dropna()   → Remove missing data
# fillna()   → Fill missing values with another value or method (ffill / bfill)

# ------------------------------------------------------------
# Filtering Out Missing Data
# ------------------------------------------------------------

data = pd.Series([1, np.nan, 3.5, np.nan, 7])
print(data)

# Remove NA values
print(data.dropna())

# DataFrame example
data = pd.DataFrame([
    [1., 6.5, 3.],
    [1., np.nan, np.nan],
    [np.nan, np.nan, np.nan],
    [np.nan, 6.5, 3.]
])
print(data)

# Drops rows containing ANY NaNs
print(data.dropna())

# Drop rows only if ALL values are missing
print(data.dropna(how="all"))

# Add a completely empty column
data[4] = np.nan
print(data)

# ------------------------------------------------------------
# More Complex Missing Data Patterns
# ------------------------------------------------------------

df = pd.DataFrame(np.random.standard_normal((7, 3)))
print(df)

# Insert missing values
df.iloc[:4, 1] = np.nan
print(df)

df.iloc[:2, 2] = np.nan
print(df)

# Drop all rows with any NaNs
print(df.dropna())

# thresh → keep rows with at least N non-NA values
print(df.dropna(thresh=2))   # require ≥ 2 non-NA entries

# Repeat checks to verify no data is lost
print(df)
df.iloc[:4, 1] = np.nan
print(df)
df.iloc[:2, 2] = np.nan
print(df)
print(df.dropna())
print(df.dropna(thresh=2))  # keep rows with ≥2 valid values

# ------------------------------------------------------------
# Filling In Missing Data
# ------------------------------------------------------------

# Fill with a scalar
print(df.fillna(0))

# Fill specific columns with specific values
print(df.fillna({1: 0.5, 2: 0}))

# Example for forward filling
df = pd.DataFrame(np.random.standard_normal((6, 3)))
print(df)

df.iloc[2:, 1] = np.nan
df.iloc[4:, 2] = np.nan
print(df)

# Forward fill (propagate last valid value downward)
print(df.fillna(method="ffill"))

# limit → fill only up to 2 consecutive NA values
print(df.fillna(method="ffill", limit=2))

# Fill using a statistic
data = pd.Series([1., np.nan, 3.5, np.nan, 7])
print(data)

# Replace NaN with the mean of the Series
print(data.fillna(data.mean()))

# ------------------------------------------------------------
# fillna() Arguments Summary
# ------------------------------------------------------------
# value:  scalar or dict specifying fill value(s)
# method: "ffill" (forward fill) | "bfill" (backward fill)
# axis:   fill across rows or columns
# limit:  maximum number of consecutive fills allowed