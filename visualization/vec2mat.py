import numpy as np

def vec2mat(vec, full=True, fill_nan=False):
    """Convert correlation vector(s) to correlation matrix/matrices.
    
    Args:
        vec (numpy.ndarray): Input vector or 2D array of shape [p x (n*(n-1)/2)]
        full (bool): If True, returns symmetric matrix by mirroring lower triangle
        fill_nan (bool): If True, initializes matrix with NaN instead of zeros
    
    Returns:
        numpy.ndarray: Correlation matrix/matrices matching MATLAB's ordering
    """
    
    # Case 1: Single vector input
    if vec.ndim == 1:
        N = len(vec)
        # Calculate matrix dimension using quadratic formula
        n = int(0.5 + np.sqrt(1 + 8*N)/2)
        
        # Initialize output matrix
        mat = np.full((n, n), np.nan) if fill_nan else np.zeros((n, n))
        
        # Fill the lower triangle in MATLAB's order
        idx = 0
        for col in range(n):
            for row in range(col + 1, n):
                mat[row, col] = vec[idx]
                idx += 1
        
        if full:
            # Make symmetric by adding transpose (excluding diagonal)
            mat = mat + mat.T
            
    # Case 2: Multiple vectors as rows
    elif vec.ndim == 2:
        p, N = vec.shape
        # Calculate matrix dimension
        n = int(0.5 + np.sqrt(1 + 8*N)/2)
        
        # Initialize 3D array for multiple matrices
        mat = np.zeros((p, n, n))
        
        # Process each vector
        for i in range(p):
            temp_mat = np.zeros((n, n))
            # Fill the lower triangle in MATLAB's order
            idx = 0
            for col in range(n):
                for row in range(col + 1, n):
                    temp_mat[row, col] = vec[i, idx]
                    idx += 1
            
            if full:
                # Make symmetric by adding transpose (excluding diagonal)
                mat[i] = temp_mat + temp_mat.T
            else:
                mat[i] = temp_mat
                
    return mat