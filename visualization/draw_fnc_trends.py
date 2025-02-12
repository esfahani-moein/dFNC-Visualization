import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def draw_fnc_trends(Bar_range, FNC_Corr_HC, FNC_Corr_SZ, Comp_ind1, Comp_ind2, output_path):
    # Convert inputs to numpy arrays if they aren't already
    FNC_Corr_HC = np.array(FNC_Corr_HC)
    FNC_Corr_SZ = np.array(FNC_Corr_SZ)
    
    # Calculate means and standard errors
    mean_HC = np.mean(FNC_Corr_HC, axis=0)
    mean_SZ = np.mean(FNC_Corr_SZ, axis=0)
    
    se_HC = stats.sem(FNC_Corr_HC, axis=0)
    se_SZ = stats.sem(FNC_Corr_SZ, axis=0)
    
    # Create figure
    plt.figure(figsize=(12, 6))
    
    # Plot bars
    x = np.arange(len(Bar_range))
    width = 0.35
    
    plt.bar(x - width/2, mean_HC, width, label='HC', color='blue', yerr=se_HC, capsize=5)
    plt.bar(x + width/2, mean_SZ, width, label='SZ', color='red', yerr=se_SZ, capsize=5)
    
    # Customize plot
    plt.xlabel('Time Windows')
    plt.ylabel('Correlation')
    plt.title(f'Component {Comp_ind1} to Component {Comp_ind2}')
    plt.xticks(x, Bar_range)
    plt.legend()
    
    # Add grid
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # Statistical analysis
    t_stats = []
    p_values = []
    
    for i in range(len(Bar_range)):
        t_stat, p_val = stats.ttest_ind(FNC_Corr_HC[:, i], FNC_Corr_SZ[:, i])
        t_stats.append(t_stat)
        p_values.append(p_val)
    
    return np.array(t_stats), np.array(p_values)

# Example usage:
if __name__ == "__main__":
    Bar_range = np.array([1, 2, 3, 4, 5])
    # Example data - replace with your actual data
    FNC_Corr_HC = np.random.randn(20, 5)  # 20 subjects, 5 time windows
    FNC_Corr_SZ = np.random.randn(20, 5)  # 20 subjects, 5 time windows
    Comp_ind1 = 1
    Comp_ind2 = 2
    output_path = "fnc_trends.png"
    
    t_stats, p_values = draw_fnc_trends(Bar_range, FNC_Corr_HC, FNC_Corr_SZ, 
                                      Comp_ind1, Comp_ind2, output_path)