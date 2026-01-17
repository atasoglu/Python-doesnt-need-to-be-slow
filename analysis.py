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
    
    # Plot 1: Execution Time (ordered by performance)
    avg_time = df.groupby('method')['time'].mean().sort_values()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='n', y='time', hue='method', hue_order=avg_time.index)
    plt.title('Execution Time per Method by N')
    plt.ylabel('Time (s)')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('figures/execution_time.png', dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 2: Speedup Factor (ordered by speedup)
    baseline = df[df['method'] == 'Vanilla Python'].set_index('n')['time']
    df['speedup'] = df.apply(lambda row: baseline[row['n']] / row['time'] if row['n'] in baseline else None, axis=1)
    
    avg_speedup = df.groupby('method')['speedup'].mean().sort_values()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='n', y='speedup', hue='method', hue_order=avg_speedup.index)
    plt.title('Speedup Factor vs Vanilla Python')
    plt.ylabel('Speedup (x)')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('figures/speedup_factor.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Analysis complete. Figures saved to 'figures/' directory.")

if __name__ == "__main__":
    main()