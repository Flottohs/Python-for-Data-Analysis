# 5.3 Summarizing and Computing Descriptive Statistics

import pandas as pd
import numpy as np

# -------------------------------
# Summarizing and Computing Descriptive Statistics
# -------------------------------

df = pd.DataFrame(
    [[1.4, np.nan],
     [7.1, -4.5],
     [np.nan, np.nan],
     [0.75, -1.3]],
    index=["a", "b", "c", "d"],
    columns=["one", "two"]
)

print(df)

# sum over rows (default axis = index)
print(df.sum())

# sum over columns
print(df.sum(axis='columns'))
print(df.sum(axis='index'))

# skipna=False includes NaN in computation (so result becomes NaN)
print(df.sum(axis="index", skipna=False))
print(df.sum(axis="columns", skipna=False))

print(df.mean(axis="columns"))

# axis: “index” means reduce row-wise, “columns” means reduce column-wise
# skipna: ignore missing values (default True)
# level: for MultiIndex, reduce by specific level

# Index of maximum value in each column
print(df.idxmax())

# Cumulative sum
print(df.cumsum())

# Summary statistics (count, mean, std, min, 25%, 50%, 75%, max)
print(df.describe())

# describe() also works with non-numeric data:
obj = pd.Series(["a", "a", "b", "c"] * 4)
print(obj)
print(obj.describe())

"""
count      Number of non-NA values
describe   Compute set of summary statistics
min, max   Compute min and max
argmin, argmax   Integer index of min/max (Series only)
idxmin, idxmax   Label index of min/max
quantile         Compute quantiles
sum              Sum of values
mean             Average
median           Median
mad              Mean absolute deviation
prod             Product
var              Variance
std              Standard deviation
skew             Skewness (3rd moment)
kurt             Kurtosis (4th moment)
cumsum           Cumulative sum
cummin/max       Cumulative min / max
cumprod          Cumulative product
diff             First difference
pct_change       Percent changes
"""

# -------------------------------
# Correlation and Covariance
# -------------------------------

price = pd.read_pickle("examples/yahoo_price.pkl")
volume = pd.read_pickle("examples/yahoo_volume.pkl")

# Percent changes of prices (returns)
returns = price.pct_change()
print(returns.tail())

"""
Example output:
Date           AAPL      GOOG     IBM       MSFT    
2016-10-17 -0.000680 0.001837 0.002072 -0.003483
2016-10-18 -0.000681 0.019616 -0.026168 0.007690
2016-10-19 -0.002979 0.007846 0.003583 -0.002255
2016-10-20 -0.000512 -0.005652 0.001719 -0.004867
2016-10-21 -0.003930 0.003011 -0.012474 0.042096
"""

# Correlation between MSFT and IBM
print(returns['MSFT'].corr(returns['IBM']))

# Covariance between MSFT and IBM
print(returns['MSFT'].cov(returns['IBM']))


# -------------------------------
# EXPLANATION:
# -------------------------------
# 1️⃣ Correlation (corr):
#     • Measures how two variables move together, normalized between -1 and 1.
#     •  1  → perfect positive relationship
#     • -1  → perfect negative relationship
#     •  0  → no linear relationship
#
# 2️⃣ Covariance (cov):
#     • Measures joint variability, not normalized.
#     • Positive → move together
#     • Negative → move opposite
#     • Magnitude depends on scale, so harder to interpret directly.

# Full correlation matrix
print(returns.corr())

"""
Example correlation matrix:
          AAPL      GOOG       IBM      MSFT
AAPL  1.000000  0.407919  0.386817  0.389695
GOOG  0.407919  1.000000  0.405099  0.465919
IBM   0.386817  0.405099  1.000000  0.499764
MSFT  0.389695  0.465919  0.499764  1.000000
"""

# Full covariance matrix
print(returns.cov())

"""
Example covariance matrix:
          AAPL      GOOG       IBM      MSFT
AAPL  0.000277  0.000107  0.000078  0.000095
GOOG  0.000107  0.000251  0.000078  0.000108
IBM   0.000078  0.000078  0.000146  0.000089
MSFT  0.000095  0.000108  0.000089  0.000215
"""

# Correlation of each column with IBM
print(returns.corrwith(returns['IBM']))

"""
AAPL    0.386817
GOOG    0.405099
IBM     1.000000
MSFT    0.499764
"""

# Correlation of returns with trading volume
print(returns.corrwith(volume))

"""
AAPL   -0.075565
GOOG   -0.007067
IBM    -0.204849
MSFT   -0.092950
"""


# -------------------------------
# Unique Values, Value Counts, and Membership
# -------------------------------

obj = pd.Series(["c", "a", "d", "a", "a", "b", "b", "c", "c"])

# Unique values (order preserved)
uniques = obj.unique()
print(uniques)

print(obj.value_counts())

# value_counts also works on NumPy arrays
print(pd.value_counts(obj.to_numpy(), sort=False))

print(obj)

mask = obj.isin(['b', 'c'])
print(mask)

"""
Boolean mask:
0 True
1 False
2 False
3 False
4 False
5 True
6 True
7 True
8 True
"""

print(obj[mask])

"""
Filtered values:
0 c
5 b
6 b
7 c
8 c
"""

to_match = pd.Series(["c", "a", "b", "b", "c", "a"])
unique_vals = pd.Series(["c", "b", "a"])

indices = pd.Index(unique_vals).get_indexer(to_match)
print(indices)

"""
isin         → Boolean check for membership
get_indexer  → Map values to integer positions in another array
unique       → Unique values in order observed
value_counts → Frequency of each unique value
"""

data = pd.DataFrame({
    "Qu1": [1, 3, 4, 3, 4],
    "Qu2": [2, 3, 1, 2, 3],
    "Qu3": [1, 5, 2, 4, 4]
})

print(data)

print(data["Qu1"].value_counts().sort_index())

"""
1    1
3    2
4    2
"""

result = data.apply(pd.value_counts).fillna(0)#must use pd.value_count instead of value_count as value_count is a series method, but not a function method, so it must be specified as pd
print(result)

"""
Value counts table:
    Qu1  Qu2  Qu3
1   1.0  1.0  1.0
2   0.0  2.0  1.0
3   2.0  2.0  0.0
4   2.0  0.0  2.0
5   0.0  0.0  1.0
"""

data = pd.DataFrame({"a": [1, 1, 1, 2, 2],
                     "b": [0, 0, 1, 0, 0]})

print(data.value_counts())

"""
DataFrame.value_counts treats each row as a full tuple:

a  b
1  0    2
2  0    2
1  1    1
dtype: int64

Meaning:
- Combination (a=1, b=0) appears 2 times
- Combination (a=2, b=0) appears 2 times
- Combination (a=1, b=1) appears 1 time
"""