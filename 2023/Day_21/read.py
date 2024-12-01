import pickle
import matplotlib.pyplot as plt
import numpy as np


def save(filename, *args):
    # Get global dictionary
    glob = globals()
    d = {}
    for v in args:
        # Copy over desired values
        d[v] = glob[v]
    with open(filename, 'wb') as f:
        # Put them in the file
        pickle.dump(d, f)


def load(filename):
    # Get global dictionary
    glob = globals()
    with open(filename, 'rb') as f:
        for k, v in pickle.load(f).items():
            # Set each global variable to the value from the file
            glob[k] = v


load("record")


plt.plot(plots_per_trail_length)

# plt.plot(np.diff(plots_per_trail_length[1::2]))

plt.show()