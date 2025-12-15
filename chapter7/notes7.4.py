# -------------------------------------------------------------------
# 7.X  STRING MANIPULATION
# -------------------------------------------------------------------
# Python provides many native string operations. pandas builds on top
# of these and adds vectorized .str methods for Series of strings.
# This section covers both standard Python string methods and
# pandas' vectorized string tools, along with regular expressions.
# -------------------------------------------------------------------

# ----------------------------
# Python Built-In String Methods
# ----------------------------

val = "a,b, guido"

# split() → splits based on a delimiter
val.split(",")

# split is often combined with strip() to remove whitespace
pieces = [x.strip() for x in val.split(",")]
print(pieces)

# Unpack into variables
first, second, third = pieces
print(first + "::" + second + "::" + third)

# Join strings with a delimiter
"::".join(pieces)

# Membership check
print("guido" in val)

# index() → returns starting index of substring, errors if not found
print(val.index(","))

# find() → like index but returns -1 if not found (safer)
print(val.find(":"))

# -------------------------------------------------------------------
# Common Python string functions:
# -------------------------------------------------------------------
# count()        : number of non-overlapping occurrences
# endswith()     : checks string ending
# startswith()   : checks beginning
# join()         : join sequence into one string
# index()        : find substring (errors if not found)
# find()         : find substring (returns -1 if not found)
# rfind()        : find last occurrence
# replace()      : replace substring
# strip()        : remove whitespace (both sides)
# rstrip()       : right strip
# lstrip()       : left strip
# split()        : split into list by delimiter
# lower()        : lowercase
# upper()        : uppercase
# casefold()     : aggressive lowercase (for comparisons)
# ljust()/rjust(): pad left/right side with spaces
# -------------------------------------------------------------------

# ----------------------------
#  REGULAR EXPRESSIONS (re module)
# ----------------------------

import re

text = "foo bar\t baz \tqux"

# \s+ → one or more whitespace characters
print(re.split(r"\s+", text))

regex = re.compile(r"\s+")
print(regex.split(text))
print(regex.findall(text))  # find all matches of the pattern

# ---------------------------------------------------------------
# Email matching example
# ---------------------------------------------------------------

text = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com"""

pattern = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
regex = re.compile(pattern, flags=re.IGNORECASE)

print(regex.findall(text))

# search() → find first match anywhere
m = regex.search(text)
print(m)
print(text[m.start():m.end()])  # extract matched substring

# match() → only matches at the beginning of the string
print(regex.match(text))  # None

# sub() → replace matches
print(regex.sub("REDACTED", text))

# ---------------------------------------------------------------
# Capturing groups with parentheses
# ---------------------------------------------------------------

pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"
regex = re.compile(pattern, flags=re.IGNORECASE)

m = regex.match("wesm@bright.net")
print(m.groups())  # ('wesm', 'bright', 'net')

print(regex.findall(text))  # returns list of tuples

# Backreferences in replacement string using \1, \2, \3
print(regex.sub(r"Username: \1, Domain: \2, Suffix: \3", text))

# ---------------------------------------------------------------
# Regex method summary:
# ---------------------------------------------------------------
# findall() → list of all matches
# finditer() → iterator over matches
# match() → match only at start
# search() → match anywhere
# split() → split using regex pattern
# sub(), subn() → replace occurrences using regex groups
# ---------------------------------------------------------------

# ----------------------------
# pandas String Operations (.str)
# ----------------------------

import numpy as np
import pandas as pd

data = {
    "Dave": "dave@google.com",
    "Steve": "steve@gmail.com",
    "Rob": "rob@gmail.com",
    "Wes": np.nan,
}

data = pd.Series(data)
print(data)
print(data.isna())

# pandas .str.contains supports regex by default
print(data.str.contains("gmail"))

# Some .str methods require extension string dtype
data_as_string_ext = data.astype("string")
print(data_as_string_ext)
print(data_as_string_ext.str.contains("gmail"))

pattern = r"([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})"

# findall per element → returns list for each row
print(data.str.findall(pattern, flags=re.IGNORECASE))

matches = data.str.findall(pattern, flags=re.IGNORECASE).str[0]
print(matches)

# Extract specific captured group
print(matches.str.get(1))  # domain

# Slice each string
print(data.str[:5])

# extract() → DataFrame with columns = regex groups
print(data.str.extract(pattern, flags=re.IGNORECASE))

# ---------------------------------------------------------------
# pandas .str method summary:
# ---------------------------------------------------------------
# cat           : join strings element-wise
# contains      : pattern match → boolean
# count         : count occurrences
# extract       : extract regex groups → DataFrame
# endswith / startswith
# findall       : list of occurrences per row
# get           : index into each string
# isalpha, isdigit, islower, isupper, isnumeric, etc.
# join          : join elements inside each string
# len           : length of each string
# lower / upper : change case
# match         : re.match for each element
# pad, center   : add whitespace
# repeat        : x → xx → xxx ...
# replace       : regex replace
# slice         : string slicing
# split         : split using delimiter or regex
# strip/lstrip/rstrip
# ---------------------------------------------------------------
