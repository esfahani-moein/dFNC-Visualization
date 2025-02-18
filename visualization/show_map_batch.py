import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.axes_grid1 import make_axes_locatable

def show_map_batch(map_data_list, plot_titles=None, save_path=None, 
                  range_val=None, cmap='jet', font_size=14,
                  show_grid=True, show_boundaries=True,
                  title_size=14, dpi=300, boundary_width=2.0,
                  rows=2, cols=3, figsize=None, label_rotation=30,
                  single_colorbar=False):
    """
    Create a grid of network connectivity maps in a single figure.
    
    Args:
        map_data_list (list): List of matrices to plot
        plot_titles (list): List of titles for each subplot
        save_path (str): Path to save the figure
        range_val (tuple): Color scale range (min, max)
        cmap (str): Colormap name
        font_size (int): Size of tick labels
        show_grid (bool): Whether to show grid lines
        show_boundaries (bool): Whether to show network boundaries
        title_size (int): Size of subplot titles
        dpi (int): DPI for saved figure
        boundary_width (float): Width of boundary lines
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        figsize (tuple): Figure size (width, height) in inches
        label_rotation (int): Rotation angle for x-axis labels
        single_colorbar (bool): Whether to use a single colorbar for all plots
    """
    # Auto-calculate figure size if not provided
    if figsize is None:
        figsize = (5.5 * cols + (0.5 if single_colorbar else 0), 4.5 * rows)

    # Read network information
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
    
    # Calculate network positions
    networks = {}
    positions = []
    labels = []
    boundaries = [0]
    current_pos = 0
    
    for name, label in network_info:
        idx = np.where([name.lower() in str(x).lower() for x in T[:, icn_idx]])[0]
        if len(idx) > 0:
            networks[name] = T[idx, 0].astype(int) - 1
            size = len(networks[name])
            positions.append(current_pos + size/2)
            labels.append(label)
            current_pos += size
            boundaries.append(current_pos)

    # Create figure with proper layout
    fig = plt.figure(figsize=figsize)
    if single_colorbar:
        # Create grid with space for colorbar
        gs = fig.add_gridspec(rows, cols + 1, 
                            width_ratios=[1]*cols + [0.05],
                            left=0.1, right=0.95,
                            bottom=0.1, top=0.9,
                            wspace=0.3, hspace=0.4)
    else:
        # Create standard grid
        gs = fig.add_gridspec(rows, cols,
                            left=0.1, right=0.95,
                            bottom=0.1, top=0.9,
                            wspace=0.3, hspace=0.4)

    # Generate default titles if none provided
    if plot_titles is None:
        plot_titles = [f'Map {i+1}' for i in range(len(map_data_list))]

    # Find global color limits if using single colorbar
    if single_colorbar and range_val is None:
        max_val = max(np.max(np.abs(data)) for data in map_data_list)
        range_val = (-max_val, max_val)

    # Create subplots for each map
    for idx, map_data in enumerate(map_data_list):
        if idx >= rows * cols:
            print(f"Warning: Only showing first {rows*cols} maps")
            break
            
        ax = fig.add_subplot(gs[idx // cols, idx % cols])
        
        # Plot the map
        im = ax.imshow(map_data, cmap=cmap, aspect='equal')
        
        # Set color limits
        if range_val is not None:
            im.set_clim(range_val[0], range_val[1])
        elif not single_colorbar:
            max_val = np.max(np.abs(map_data))
            im.set_clim(-max_val, max_val)
        
        # Add boundaries
        if show_boundaries:
            for boundary in boundaries:
                ax.axvline(x=boundary-0.5, color='black', linewidth=boundary_width)
                ax.axhline(y=boundary-0.5, color='black', linewidth=boundary_width)
        
        # Add grid
        if show_grid:
            ax.grid(True, which='minor', color='gray', linestyle='-', linewidth=0.1)
        
        # Set ticks and labels
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=label_rotation, 
                          fontsize=font_size, fontweight='bold')
        ax.set_yticks(positions)
        ax.set_yticklabels(labels, fontsize=font_size, fontweight='bold')
        
        # Set title
        ax.set_title(plot_titles[idx], pad=10, 
                    fontsize=title_size, fontweight='bold')
        
        # Add individual colorbars if not using single colorbar
        if not single_colorbar:
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar = plt.colorbar(im, cax=cax)
            cbar.ax.tick_params(labelsize=font_size-2)

    # Add single colorbar if specified
    if single_colorbar:
        cax = fig.add_subplot(gs[:, -1])
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.tick_params(labelsize=font_size-2)


    # Save figure if path provided
    if save_path:
        try:
            plt.savefig(save_path, bbox_inches='tight', dpi=dpi)
        except Exception as e:
            print(f"Error saving figure: {e}")

    plt.show()
    return None