import numpy as np
import pandas as pd
from pathlib import Path

def getOrderedMap(map_matrix):
    
    current_dir = Path(__file__).parent
    excel_path = current_dir / "cmp" / "ICNs_v2.xlsx"
    
    
    tbl = pd.read_excel(excel_path)

    sim = np.array(map_matrix)
    if sim.shape != (105,105):
        raise ValueError("Input matrix must be (105,105)")
    
    # Get the order and sort it
    leafOrder = tbl['new_order'].values
    leafOrder = np.argsort(leafOrder)
    
    # Reorder the matrix using the sorted indices
    sim = sim[leafOrder][:, leafOrder]

    if sim.shape != (105,105):
        raise ValueError("Input matrix must be (105,105)")
    
    orderedMap = sim
    return orderedMap