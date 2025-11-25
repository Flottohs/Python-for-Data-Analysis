"""
4.7 Example: Random Walks
-------------------------

Random walks are a classic illustration of using NumPy for simulations.
A simple random walk starts at 0 with steps of +1 or -1 occurring with equal probability.

We’ll implement both:
1. Pure Python single walk
2. NumPy vectorized single walk
3. Simulating many walks at once
"""

# ----------------------------
# 1. Pure Python single random walk
import random
import matplotlib.pyplot as plt

position = 0
walk = [position]
nsteps = 1000

for _ in range(nsteps):
    step = 1 if random.randint(0, 1) else -1
    position += step
    walk.append(position)

# Plot first 100 steps
plt.plot(walk[:100])
plt.title("Pure Python Random Walk (first 100 steps)")
plt.show()

# ----------------------------
# 2. NumPy vectorized single walk
import numpy as np

nsteps = 1000
rng = np.random.default_rng(seed=12345)  # fresh random generator

draws = rng.integers(0, 2, size=nsteps)   # 0 or 1
steps = np.where(draws == 0, 1, -1)       # convert 0 -> +1, 1 -> -1
walk = steps.cumsum()                      # cumulative sum = actual positions

plt.plot(walk)
plt.title("NumPy Random Walk")
plt.show()

print("Min position:", walk.min())
print("Max position:", walk.max())

# ----------------------------
# 3. First crossing time
# Find the first step where the walk reaches |10| from origin
first_cross_10 = (np.abs(walk) >= 10).argmax()
print("First crossing of ±10:", first_cross_10)

# ----------------------------
# 4. Simulating many walks at once
nwalks = 5000
nsteps = 1000

# Draw 0 or 1 for all walks
draws = rng.integers(0, 2, size=(nwalks, nsteps))
steps = np.where(draws > 0, 1, -1)

# cumulative sum along axis=1 gives each walk's positions
walks = steps.cumsum(axis=1)

print("Max across all walks:", walks.max())
print("Min across all walks:", walks.min())

# ----------------------------
# 5. Minimum crossing times to ±30
# Check which walks actually cross ±30
hits30 = (np.abs(walks) >= 30).any(axis=1)
print("Number of walks that hit ±30:", hits30.sum())

# Extract first crossing times for walks that hit ±30
crossing_times = (np.abs(walks[hits30]) >= 30).argmax(axis=1)
print("Crossing times for ±30:", crossing_times)
print("Mean crossing time:", crossing_times.mean())

# ----------------------------
# 6. Random draws for other distributions
draws_normal = 0.25 * rng.standard_normal((nwalks, nsteps))
print("Example small normal draws array:\n", draws_normal)

# Notes:
# - Vectorized approach creates array of size nwalks * nsteps.
# - Memory usage can become high for very large simulations.
# - axis=0 collapses down rows (operate per column)
# - axis=1 collapses across columns (operate per row)
