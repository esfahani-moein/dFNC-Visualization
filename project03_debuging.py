import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
from pathlib import Path
import visualization as vis

##
beta_samples = np.random.beta(0.15, 0.15, size=5460)  # Even more extreme U-shape
var1 = 2 * beta_samples - 1  # Scale to [-1, 1]
# Verify the extremes
print(f"Min value: {var1.min():.3f}")
print(f"Max value: {var1.max():.3f}")


##
map_data = vis.vec2mat(var1)

change_order = vis.getOrderedMap(map_data)

