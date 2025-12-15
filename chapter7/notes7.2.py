# Data Transformation in pandas

import pandas as pd
import numpy as np

# ----------------------------
# Removing Duplicates
# ----------------------------

data = pd.DataFrame({
    "k1": ["one", "two"] * 3 + ["two"], 
    "k2": [1, 1, 2, 3, 3, 4, 4]
})

print(data.duplicated())  # Boolean Series indicating duplicate rows
print(data.drop_duplicates())  # Drop duplicate rows

data["v1"] = range(7)
print(data)

# Drop duplicates based on a single column
print(data.drop_duplicates(subset=["k1"]))  
# Removes rows with same value in k1, keeps first occurrence by default
print(data)

# Drop duplicates based on multiple columns, keep last occurrence
print(data.drop_duplicates(["k1", "k2"], keep="last"))  
# Removes duplicates where both k1 and k2 match, keeps last

# ----------------------------
# Transforming Data Using a Function or Mapping
# ----------------------------

data = pd.DataFrame({
    "food": ["bacon", "pulled pork", "bacon", "pastrami", 
             "corned beef", "bacon", "pastrami", "honey ham", "nova lox"], 
    "ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6]
})

print(data)

# Mapping food to type of animal
meat_to_animal = {
    "bacon": "pig",
    "pulled pork": "pig",
    "pastrami": "cow",
    "corned beef": "cow",
    "honey ham": "pig",
    "nova lox": "salmon"
}

# Using Series.map to transform values according to a dictionary
data["animal"] = data["food"].map(meat_to_animal)
print(data)

# Equivalent using a function
def get_animal(x):
    return meat_to_animal[x]

data['food'].map(get_animal)
print(data)

# ----------------------------
# Replacing Values
# ----------------------------

data = pd.Series([1., -999., 2., -999., -1000., 3.])
print(data)

# Replace specific values with NaN
print(data.replace(-999, np.nan))

# Replace multiple values with different replacements
print(data.replace([-999, -1000], [np.nan, 0]))

# Using a dictionary mapping
print(data.replace({-999: np.nan, -1000: 0}))

# ----------------------------
# Renaming Axis Indexes
# ----------------------------

data = pd.DataFrame(np.arange(12).reshape((3, 4)), 
                    index=["Ohio", "Colorado", "New York"], 
                    columns=["one", "two", "three", "four"])
print(data)

# Transform index with map
def transform(x):
    return x[:4].upper()  # first 4 letters, uppercase

data.index = data.index.map(transform)
print(data)

# Rename index and columns
print(data.rename(index=str.title, columns=str.upper))
print(data.rename(index={"OHIO": "INDIANA"}, columns={"three": "peekaboo"}))

# ----------------------------
# Discretization and Binning
# ----------------------------

ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]

# Cut ages into bins
age_categories = pd.cut(ages, bins)
print(age_categories)  # Interval categories

# Categorical codes
print(age_categories.codes)  # Integer codes starting from 0

# Unique categories
print(age_categories.categories)
print(age_categories.categories[0])

# Frequency count per category
print(pd.value_counts(age_categories))

# Change bin closure side
print(pd.cut(ages, bins, right=False))

# Assign labels to bins
group_names = ["Youth", "YoungAdult", "MiddleAged", "Senior"]
print(pd.cut(ages, bins, labels=group_names))

# For continuous data with equal-sized bins
data = np.random.uniform(size=20)
print(pd.cut(data, 4, precision=2))  # 4 groups, 2 decimal precision

# Quantile-based discretization
data = np.random.standard_normal(1000)
quartiles = pd.qcut(data, 4, precision=2)  # roughly equal-sized bins
print(pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.]).value_counts())

# ----------------------------
# Detecting and Filtering Outliers
# ----------------------------

data = pd.DataFrame(np.random.standard_normal((1000, 4)))
print(data.describe())

col = data[2]
print(col[col.abs() > 3])  # Rows where column 2 > 3 in absolute value

# Filter rows with any extreme value
print(data[(data.abs() > 3).any(axis="columns")])

# Clip values to [-3, 3] without using np.clip
data[data.abs() > 3] = np.sign(data) * 3  # sign gives -1 or 1
print(data.describe())
print(np.sign(data).head())

# ----------------------------
# Permutation and Random Sampling
# ----------------------------

df = pd.DataFrame(np.arange(5 * 7).reshape((5, 7)))
print(df)

# Random permutation of row indices
sampler = np.random.permutation(5)
print(sampler)

# Use permutation to reorder rows
print(df.take(sampler))
print(df.iloc[sampler])

# Permute columns
column_sampler = np.random.permutation(7)
print(df.take(column_sampler, axis='columns'))

# Random sample of rows without replacement
print(df.sample(n=3))

# Random sample with replacement from a Series
choices = pd.Series([5, 7, -1, 6, 4])
print(choices.sample(n=10, replace=True))

# ----------------------------
# Computing Indicator/Dummy Variables
# ----------------------------

df = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"], "data1": range(6)})
print(df)

# Create dummy variables (1/0)
print(pd.get_dummies(df["key"]))

# Add prefix to dummy columns
dummies = pd.get_dummies(df["key"], prefix="key")
print(dummies)

# Merge dummy variables with original DataFrame
df_with_dummy = df[["data1"]].join(dummies)
print(df_with_dummy)

# ----------------------------
# Combining with discretization
# ----------------------------

np.random.seed(12345)
values = np.random.uniform(size=10)
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]

# Use get_dummies with cut to create categorical dummy variables
print(pd.get_dummies(pd.cut(values, bins)))

