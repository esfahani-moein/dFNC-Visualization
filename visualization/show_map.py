import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def show_map(map_data, save_path=None, 
                       range_val=None, cmap='jet', font_size=14,
                       show_grid=True, show_boundaries=True,
                       title_size=14, label_rotation=30, dpi=300,
                       figsize=(10, 8), boundary_width=2.0,plot_title='Network Connectivity Map'):
    
    
    current_dir = Path(__file__).parent
    excel_path = current_dir / "cmp" / "ICNs_v2.xlsx"

    df = pd.read_excel(excel_path)
    T = df.values
    icn_idx = df.columns.get_loc('Label')
    
    network_info = [
        ('Visual', 'VI'),
        ('Cerebellar', 'CB'),
        ('Temporal', 'TM'),
        ('Subcortical', 'SC'),
        ('Sensorimotor', 'SM'),
        ('Higher Cognition', 'HC')  
    ]
    
    networks = {}
    all_indices = []
    positions = []
    labels = []
    boundaries = [0]
    current_pos = 0
    
    for name, label in network_info:
        idx = np.where([name.lower() in str(x).lower() for x in T[:, icn_idx]])[0]
        if len(idx) > 0:
            networks[name] = T[idx, 0].astype(int) - 1
            size = len(networks[name])
            all_indices.extend(networks[name])
            positions.append(current_pos + size/2)
            labels.append(label)
            current_pos += size
            boundaries.append(current_pos)
    
       
    plt.figure(figsize=figsize)
    im = plt.imshow(map_data, cmap=cmap, aspect='equal')
    
    if range_val is not None:
        plt.clim(range_val[0], range_val[1])
    else:
        max_val = np.max(np.abs(map_data))
        plt.clim(-max_val, max_val)
    
    if show_boundaries:
        for boundary in boundaries:
            plt.axvline(x=boundary-0.5, color='black', linewidth=boundary_width)
            plt.axhline(y=boundary-0.5, color='black', linewidth=boundary_width)
    
    if show_grid:
        plt.grid(True, which='minor', color='gray', linestyle='-', linewidth=0.1)
    
    plt.xticks(positions, labels, rotation=label_rotation, 
              fontsize=font_size, fontweight='bold')
    plt.yticks(positions, labels, fontsize=font_size, fontweight='bold')
    
    plt.title(plot_title, pad=20, 
             fontsize=title_size, fontweight='bold')
    
    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=font_size-2)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=dpi)

    plt.show() 
       
    return None
