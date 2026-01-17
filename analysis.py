import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Load results
    results_dir = 'results'
    all_benchmarks = []

    for filename in os.listdir(results_dir):
        if filename.startswith('results_') and filename.endswith('.json'):
            with open(os.path.join(results_dir, filename), 'r') as f:
                data = json.load(f)
                if 'benchmarks' in data:
                    all_benchmarks.extend(data['benchmarks'])

    df = pd.DataFrame(all_benchmarks)
    
    # Create figures directory
    os.makedirs('figures', exist_ok=True)
    
    # Generate dynamic color palette
    unique_methods = df['method'].unique()
    colors = plt.cm.tab20(range(len(unique_methods)))
    color_map = dict(zip(unique_methods, colors))
    
    # Plot 1: Execution Time
    avg_time = df.groupby('method')['time'].mean().sort_values()
    plt.figure(figsize=(12, 8))
    palette = [color_map.get(method, '#888888') for method in avg_time.index]
    ax = sns.barplot(data=df, x='n', y='time', hue='method', hue_order=avg_time.index, palette=palette, edgecolor='black', linewidth=0.5, legend=False)
    ax.set_axisbelow(True)
    
    # Add labels on bars
    for i, container in enumerate(ax.containers):
        method_name = avg_time.index[i]
        ax.bar_label(container, labels=[f'{method_name}\n{v:.3f}' for v in container.datavalues], rotation=90, fontsize=6, padding=3)
    
    plt.title('Execution Time per Method by N')
    plt.ylabel('Time (s)')
    plt.yscale('log')
    plt.ylim(bottom=ax.get_ylim()[0], top=ax.get_ylim()[1] * 3)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/execution_time.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 2: Speedup Factor
    baseline = df[df['method'] == 'Vanilla Python'].set_index('n')['time']
    df['speedup'] = df.apply(lambda row: baseline[row['n']] / row['time'] if row['n'] in baseline else None, axis=1)
    
    avg_speedup = df.groupby('method')['speedup'].mean().sort_values()
    plt.figure(figsize=(12, 8))
    palette = [color_map.get(method, '#888888') for method in avg_speedup.index]
    ax = sns.barplot(data=df, x='n', y='speedup', hue='method', hue_order=avg_speedup.index, palette=palette, edgecolor='black', linewidth=0.5, legend=False)
    ax.set_axisbelow(True)
    
    # Add labels on bars
    for i, container in enumerate(ax.containers):
        method_name = avg_speedup.index[i]
        ax.bar_label(container, labels=[f'{method_name}\n{v:.2f}x' for v in container.datavalues], rotation=90, fontsize=6, padding=3)
    
    plt.title('Speedup Factor vs Vanilla Python')
    plt.ylabel('Speedup (x)')
    plt.yscale('log')
    plt.ylim(bottom=ax.get_ylim()[0], top=ax.get_ylim()[1] * 3)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figures/speedup_factor.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Analysis complete. Figures saved to 'figures/' directory.")

if __name__ == "__main__":
    main()