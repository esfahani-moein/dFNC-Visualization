import numpy as np

def normalization(x):
    # Convert input to numpy array and flatten it for calculations
    x = np.array(x)
    
    # Calculate mean and standard deviation of the input
    a_mean = np.mean(x)
    a_std = np.std(x)
    
    # Perform z-score normalization: (x - mean) / std
    x_zscore = (x - a_mean) / a_std
    
    # Find min and max of z-scored data
    a_min = np.min(x_zscore)
    a_max = np.max(x_zscore)
    
    # Scale the z-scored data to range [-1, 1] using min-max normalization
    x_out = 2 * (x_zscore - a_min) / (a_max - a_min) - 1
    
    return x_out