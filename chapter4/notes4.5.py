"""
NumPy File I/O Notes
Chapter: Saving and Loading Arrays
"""

import numpy as np

# ----------------------------
# Saving a single array to disk
arr = np.arange(10)  # create a simple array
np.save('my_array.npy', arr)  
# Saves in NumPy's binary format (.npy)
# If the filename doesn't end with .npy, the extension is added automatically

# Loading the array back
arr_loaded = np.load('my_array.npy')
print("Loaded array:", arr_loaded)

# ----------------------------
# Saving multiple arrays in an uncompressed archive
np.savez("array_archive.npz", a=arr, b=arr)
# Use keyword arguments to store multiple arrays
# Each array can be accessed by the keyword name when loading

arch = np.load("array_archive.npz")
print("Array 'b' from archive:", arch["b"])

# ----------------------------
# Saving multiple arrays in a compressed archive
np.savez_compressed("arrays_compressed.npz", a=arr, b=arr)
# Useful if arrays contain lots of repeating or compressible data
# The compressed archive still allows individual arrays to be accessed by name

# ----------------------------
# Notes Summary:
"""
1. np.save(filename, array) - Save a single array to disk in binary .npy format.
2. np.load(filename) - Load a .npy file back into a NumPy array.
3. np.savez(filename, a=arr1, b=arr2) - Save multiple arrays into an uncompressed .npz archive.
4. np.savez_compressed(filename, a=arr1, b=arr2) - Save multiple arrays into a compressed .npz archive.
5. When loading a .npz file, the object behaves like a dictionary. Access arrays using the keyword names.
6. NumPy's binary format is fast and efficient; for text/tabular data, pandas is often preferred.
"""
