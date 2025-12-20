# ============================================================
# 10.3 Apply: General Split-Apply-Combine (FULL VS CODE NOTES)
# ============================================================

# ------------------------------------------------------------
# CORE IDEA: split-apply-combine
# ------------------------------------------------------------
# GroupBy.apply is the MOST general groupby operation in pandas.
#
# What apply does:
# 1. SPLIT the data into groups
# 2. APPLY a function to each group
# 3. COMBINE the results back together
#
# The function you pass can return:
# - a DataFrame
# - a Series
# - a scalar
# Pandas figures out how to glue the results back together.
# ------------------------------------------------------------

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# BASIC APPLY EXAMPLE (TOP-N PER GROUP)
# ------------------------------------------------------------

# Load tipping dataset
tips = pd.read_csv('tips.csv')

# Create a derived column: tip percentage
tips["tip_pct"] = tips["tip"] / tips["total_bill"]

# Define a function that returns the top N rows by a column
# IMPORTANT:
# - This function receives ONE GROUP AT A TIME (a DataFrame)
# - It returns a DataFrame

def top(df, n=5, column="tip_pct"):
    return df.sort_values(column, ascending=False)[:n]

# Apply function to the ENTIRE DataFrame (no grouping)
print(top(tips, n=6))

# ------------------------------------------------------------
# APPLY WITH GROUPBY
# ------------------------------------------------------------

# Steps happening here:
# 1. tips is split by smoker
# 2. top() is run on each group
# 3. Results are concatenated
#
# Result has a HIERARCHICAL INDEX:
# - outer level: group key (smoker)
# - inner level: original row index

print(tips.groupby("smoker").apply(top, include_groups=False))

# ------------------------------------------------------------
# APPLY WITH MULTIPLE GROUP KEYS AND ARGUMENTS
# ------------------------------------------------------------

print(
    tips.groupby(["smoker", "day"]).apply(
        top,
        n=1,
        column="total_bill",
        include_groups=False
    )
)

# ------------------------------------------------------------
# APPLY VS BUILT-IN GROUPBY METHODS
# ------------------------------------------------------------

# Built-in methods like describe are just optimized versions
# of apply under the hood

result = tips.groupby("smoker")["tip_pct"].describe()
print(result)

# Unstack moves smoker from index into columns
print(result.unstack('smoker'))

# Equivalent manual apply version

def f(group):
    return group.describe()

# ------------------------------------------------------------
# SUPPRESSING GROUP KEYS
# ------------------------------------------------------------

# By default, apply adds group keys to the index
# group_keys=False removes them

print(tips)
print(
    tips.groupby("smoker", group_keys=False)
        .apply(top, include_groups=False)
)

# ------------------------------------------------------------
# QUANTILE AND BUCKET ANALYSIS
# ------------------------------------------------------------

frame = pd.DataFrame({
    "data1": np.random.standard_normal(1000),
    "data2": np.random.standard_normal(1000)
})

print(frame.head())

# pd.cut splits data into FIXED-WIDTH bins
quartiles = pd.cut(frame['data1'], 4)
print(quartiles.head(10))

# Define a function returning a DataFrame of stats

def get_stats(group):
    return pd.DataFrame({
        "min": group.min(),
        "max": group.max(),
        "count": group.count(),
        "mean": group.mean()
    })

# Group by the categorical bins
grouped = frame.groupby(quartiles, observed=False)
print(grouped.apply(get_stats))

# Equivalent using agg (more efficient)
print(grouped.agg(["min", "max", "count", "mean"]))

# ------------------------------------------------------------
# QUANTILE-BASED BUCKETS (EQUAL-SIZED GROUPS)
# ------------------------------------------------------------

# pd.qcut splits data into groups with equal counts
quartiles_samp = pd.qcut(frame["data1"], 4, labels=False)
print(quartiles_samp.head())

grouped = frame.groupby(quartiles_samp)
print(grouped.apply(get_stats))

# ------------------------------------------------------------
# FILLING MISSING VALUES WITH GROUP-SPECIFIC LOGIC
# ------------------------------------------------------------

# Simple example: fill NA with global mean
s = pd.Series(np.random.standard_normal(6))
s[::2] = np.nan
print(s)
print(s.fillna(s.mean()))

# ------------------------------------------------------------
# GROUP-SPECIFIC FILLING
# ------------------------------------------------------------

states = [
    "Ohio", "New York", "Vermont", "Florida",
    "Oregon", "Nevada", "California", "Idaho"
]

group_key = [
    "East", "East", "East", "East",
    "West", "West", "West", "West"
]

# Create Series with missing values
data = pd.Series(np.random.standard_normal(8), index=states)
print(data)

data[["Vermont", "Nevada", "Idaho"]] = np.nan
print(data)

print(data.groupby(group_key).size())
print(data.groupby(group_key).count())
print(data.groupby(group_key).mean())

# Fill NA with group mean

def fill_mean(group):
    return group.fillna(group.mean())

print(data.groupby(group_key).apply(fill_mean))

# Fill NA with predefined values per group
fill_values = {"East": 0.5, "West": -1}

def fill_func(group):
    print('\n')
    return group.fillna(fill_values[group.name])

print(data.groupby(group_key).apply(fill_func))

# ------------------------------------------------------------
# RANDOM SAMPLING AND PERMUTATION
# ------------------------------------------------------------

# Construct a deck of cards
suits = ["H", "S", "C", "D"]
card_val = (list(range(1, 11)) + [10] * 3) * 4

base_names = ["A"] + list(range(2, 11)) + ["J", "K", "Q"]
cards = []
for suit in suits:
    cards.extend(str(num) + suit for num in base_names)

deck = pd.Series(card_val, index=cards)
print(deck.head())

# Draw random cards

def draw(deck, n=5):
    return deck.sample(n)

print(draw(deck))

# Group by suit and draw cards per group

def get_suit(card):
    return card[-1]

print(deck.groupby(get_suit).apply(draw, n=2))
print(deck.groupby(get_suit, group_keys=False).apply(draw, n=2))

# ------------------------------------------------------------
# GROUP WEIGHTED AVERAGE AND CORRELATION
# ------------------------------------------------------------

df = pd.DataFrame({
    "category": ["a", "a", "a", "a", "b", "b", "b", "b"],
    "data": np.random.standard_normal(8),
    "weights": np.random.uniform(size=8)
})

print(df)

grouped = df.groupby("category")

# Weighted average per group

def get_wavg(group):
    return np.average(group["data"], weights=group["weights"])

print(grouped.apply(get_wavg, include_groups=False))

# ------------------------------------------------------------
# GROUP-WISE CORRELATION (STOCK DATA)
# ------------------------------------------------------------

close_px = pd.read_csv(
    "examples/stock_px.csv",
    parse_dates=True,
    index_col=0
)

print(close_px.info())
print(close_px.tail(4))

# Compute daily returns
rets = close_px.pct_change().dropna()

# Correlation with SPX

def spx_corr(group):
    return group.corrwith(group["SPX"])

# Group by year

def get_year(x):
    return x.year

by_year = rets.groupby(get_year)
print(by_year.apply(spx_corr))

# Correlation between AAPL and MSFT

def corr_aapl_msft(group):
    return group["AAPL"].corr(group["MSFT"])

print(by_year.apply(corr_aapl_msft))

# ------------------------------------------------------------
# GROUP-WISE LINEAR REGRESSION
# ------------------------------------------------------------

import statsmodels.api as sm

# This function runs an OLS regression PER GROUP
# Returns regression parameters (beta + intercept)

def regress(data, yvar=None, xvars=None):
    Y = data[yvar]
    X = data[xvars]
    X["intercept"] = 1.
    result = sm.OLS(Y, X).fit()
    return result.params

print(by_year.apply(regress, yvar="AAPL", xvars=["SPX"]))
