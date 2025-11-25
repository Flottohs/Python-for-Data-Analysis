"""
Python for Data Analysis – NumPy Random Number Generation
Author: Your Name
Description: Notes and examples from Wes McKinney's book "Python for Data Analysis", Chapter 4.2
"""

# ----------------------------
# Import NumPy
import numpy as np
from random import normalvariate

# ----------------------------
# Pseudorandom Numbers with NumPy
# Generate a 4x4 array of samples from the standard normal distribution (mean=0, variance=1)
samples = np.random.standard_normal(size=(4, 4))
print("4x4 standard normal samples:\n", samples)

# ----------------------------
# Comparison with Python's random module
N = 1_000_000
samples_python = [normalvariate(0, 1) for _ in range(N)]
print("\nFirst 5 samples from Python random module:", samples_python[:5])

# Using NumPy for 1 million standard normal samples (faster and more concise)
samples_numpy = np.random.standard_normal(N)
print("\nFirst 5 samples from NumPy standard normal:", samples_numpy[:5])

# ----------------------------
# Using a NumPy Random Generator (rng) with a seed for reproducibility
rng = np.random.default_rng(seed=12345)
print("\nRandom Generator object type:", type(rng))

# Generate 10 samples from standard normal distribution using rng
print("\n10 standard normal samples from seeded rng:", rng.standard_normal(10))

# Generate a 2x3 array of standard normal samples
data = rng.standard_normal((2, 3))
print("\n2x3 standard normal samples from seeded rng:\n", data)

# ----------------------------
# Notes on RNG
# - Seed: determines the initial state; allows reproducible results for testing/debugging
# - rng is isolated from other code using numpy.random

# ----------------------------
# Common NumPy RNG Methods:
# permutation: Return a random permutation of a sequence
# shuffle: Randomly permute a sequence in place
# uniform: Draw samples from a uniform distribution
# integers: Draw random integers from a given low-to-high range
# standard_normal: Draw samples from normal distribution (mean=0, std=1)
# binomial: Draw samples from a binomial distribution
# normal: Draw samples from a normal (Gaussian) distribution
# beta: Draw samples from a beta distribution
# chisquare: Draw samples from a chi-square distribution
# gamma: Draw samples from a gamma distribution
