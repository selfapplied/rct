"""
Extended experiments for the Bi-Laplacian Hamiltonian.

Implements the "next moves" suggested in the Tetragraphic analysis:
1. Energy decomposition for more eigenmodes
2. Valuation invariance checks
3. Scaling experiments
4. Multiple primes experiments
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict
from .bi_laplacian import BiLaplacianHamiltonian


def experiment_1_energy_decomposition(n_modes: int = 10):
    """
    Experiment 1: Decompose energy for more eigenmodes.
    
    Compute analytic and valuation energies for λ₀, λ₁, λ₂, ...
    to see if low-lying modes show balanced leakage or specialize.
    """
    print("=" * 70)
    print("EXPERIMENT 1: ENERGY DECOMPOSITION FOR MULTIPLE EIGENMODES")
    print("=" * 70)
    
    ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3], weights=[1.0, 1.0])
    
    print(f"\nAnalyzing first {n_modes} eigenmodes:")
    print("\n{:>5s} {:>12s} {:>12s} {:>12s} {:>12s} {:>10s}".format(
        "n", "λ_n", "E_∞", "E_2", "E_3", "Ratio"
    ))
    print("-" * 70)
    
    results = []
    for n in range(n_modes):
        energy = ham.decompose_energy(n)
        
        e_total = energy['total']
        e_inf = energy['analytic']
        e_2 = energy['p=2']
        e_3 = energy['p=3']
        
        # Compute ratio of analytic to total valuation energy
        e_val_total = e_2 + e_3
        ratio = e_inf / e_val_total if e_val_total > 1e-10 else float('inf')
        
        print(f"{n:5d} {e_total:12.6f} {e_inf:12.6f} {e_2:12.6f} {e_3:12.6f} {ratio:10.3f}")
        
        results.append({
            'n': n,
            'total': e_total,
            'analytic': e_inf,
            'p2': e_2,
            'p3': e_3,
            'ratio': ratio
        })
    
    # Plot energy decomposition
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Stacked bar chart
    n_vals = [r['n'] for r in results]
    e_inf_vals = [r['analytic'] for r in results]
    e_2_vals = [r['p2'] for r in results]
    e_3_vals = [r['p3'] for r in results]
    
    ax1.bar(n_vals, e_inf_vals, label='E_∞ (analytic)', alpha=0.8)
    ax1.bar(n_vals, e_2_vals, bottom=e_inf_vals, label='E_2', alpha=0.8)
    bottom = [e_inf_vals[i] + e_2_vals[i] for i in range(len(n_vals))]
    ax1.bar(n_vals, e_3_vals, bottom=bottom, label='E_3', alpha=0.8)
    
    ax1.set_xlabel('Eigenmode n', fontsize=12)
    ax1.set_ylabel('Energy', fontsize=12)
    ax1.set_title('Energy Decomposition by Mode', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Ratio plot
    ratios = [r['ratio'] for r in results if r['ratio'] < 100]  # Filter out infinities
    n_finite = [r['n'] for r in results if r['ratio'] < 100]
    
    ax2.plot(n_finite, ratios, 'o-', linewidth=2, markersize=8)
    ax2.axhline(y=1.0, color='r', linestyle='--', label='E_∞ = E_val (balanced)')
    ax2.set_xlabel('Eigenmode n', fontsize=12)
    ax2.set_ylabel('E_∞ / (E_2 + E_3)', fontsize=12)
    ax2.set_title('Analytic to Valuation Energy Ratio', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/tmp/experiment1_energy_decomposition.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved to: /tmp/experiment1_energy_decomposition.png")
    
    return results


def experiment_2_valuation_invariance():
    """
    Experiment 2: Check valuation invariance numerically.
    
    For each mode and prime p, compute ||ψ_n(px) - ψ_n(x)|| / ||ψ_n||
    to see if low modes are more invariant under prime shifts.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: VALUATION INVARIANCE")
    print("=" * 70)
    
    ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3], weights=[1.0, 1.0])
    n_modes = 10
    
    print(f"\nChecking invariance for first {n_modes} modes:")
    print("\n{:>5s} {:>15s} {:>15s}".format("n", "||ψ(2x)-ψ(x)||", "||ψ(3x)-ψ(x)||"))
    print("-" * 70)
    
    results = {'n': [], 'inv_2': [], 'inv_3': []}
    
    for n in range(n_modes):
        inv_2 = ham.check_valuation_invariance(n, 2)
        inv_3 = ham.check_valuation_invariance(n, 3)
        
        print(f"{n:5d} {inv_2:15.6f} {inv_3:15.6f}")
        
        results['n'].append(n)
        results['inv_2'].append(inv_2)
        results['inv_3'].append(inv_3)
    
    # Plot invariance vs mode number
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.plot(results['n'], results['inv_2'], 'o-', linewidth=2, markersize=8, label='p=2')
    ax.plot(results['n'], results['inv_3'], 's-', linewidth=2, markersize=8, label='p=3')
    
    ax.set_xlabel('Eigenmode n', fontsize=12)
    ax.set_ylabel('||ψ(px) - ψ(x)|| / ||ψ||', fontsize=12)
    ax.set_title('Valuation Invariance vs Mode Number', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/tmp/experiment2_valuation_invariance.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved to: /tmp/experiment2_valuation_invariance.png")
    
    return results


def experiment_3_scaling():
    """
    Experiment 3: Scaling experiment.
    
    Fix primes {2,3}, double N_t, track λ₁ and energy split ratios.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: SCALING WITH N_t")
    print("=" * 70)
    
    N_t_values = [50, 100, 200, 400]
    
    print("\nScaling N_t while keeping T = log(N_t):")
    print("\n{:>6s} {:>10s} {:>12s} {:>12s} {:>12s} {:>12s}".format(
        "N_t", "T", "λ_0", "λ_1", "E_∞/E_val", "(π/T)²"
    ))
    print("-" * 70)
    
    results = {
        'N_t': [],
        'T': [],
        'lambda_0': [],
        'lambda_1': [],
        'ratio': [],
        'theoretical': []
    }
    
    for N_t in N_t_values:
        T = np.log(N_t)
        ham = BiLaplacianHamiltonian(N_t=N_t, T=T, primes=[2, 3], weights=[1.0, 1.0])
        
        eigenvalues = ham.get_eigenvalues(5)
        energy_1 = ham.decompose_energy(1)
        
        e_inf = energy_1['analytic']
        e_val = energy_1['p=2'] + energy_1['p=3']
        ratio = e_inf / e_val if e_val > 1e-10 else float('inf')
        theoretical = (np.pi / T)**2
        
        print(f"{N_t:6d} {T:10.5f} {eigenvalues[0]:12.8f} {eigenvalues[1]:12.6f} {ratio:12.3f} {theoretical:12.6f}")
        
        results['N_t'].append(N_t)
        results['T'].append(T)
        results['lambda_0'].append(eigenvalues[0])
        results['lambda_1'].append(eigenvalues[1])
        results['ratio'].append(ratio)
        results['theoretical'].append(theoretical)
    
    # Plot scaling behavior
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # λ_1 vs N_t
    ax1.plot(results['N_t'], results['lambda_1'], 'o-', linewidth=2, markersize=10, label='λ_1')
    ax1.set_xlabel('N_t', fontsize=12)
    ax1.set_ylabel('λ_1', fontsize=12)
    ax1.set_title('First Excited Eigenvalue vs Grid Size', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Ratio vs N_t
    ax2.plot(results['N_t'], results['ratio'], 's-', linewidth=2, markersize=10, label='E_∞/E_val')
    ax2.axhline(y=1.0, color='r', linestyle='--', label='Balanced (1:1)')
    ax2.set_xlabel('N_t', fontsize=12)
    ax2.set_ylabel('E_∞ / E_val', fontsize=12)
    ax2.set_title('Energy Ratio vs Grid Size', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/tmp/experiment3_scaling.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved to: /tmp/experiment3_scaling.png")
    
    return results


def experiment_4_multiple_primes():
    """
    Experiment 4: Add more primes.
    
    Try P = {2,3,5} with equal weights and observe if ψ₁'s energy
    splits into ~4 roughly equal parts (analytic + 3 valuations).
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 4: MULTIPLE PRIMES")
    print("=" * 70)
    
    prime_sets = [
        [2, 3],
        [2, 3, 5],
        [2, 3, 5, 7]
    ]
    
    results = []
    
    for primes in prime_sets:
        print(f"\n--- Primes: {primes} ---")
        
        weights = [1.0] * len(primes)
        ham = BiLaplacianHamiltonian(N_t=100, primes=primes, weights=weights)
        
        energy_1 = ham.decompose_energy(1)
        
        print(f"λ_1 = {energy_1['total']:.6f}")
        print(f"E_∞ = {energy_1['analytic']:.6f}")
        
        val_energies = []
        for p in primes:
            e_p = energy_1[f'p={p}']
            val_energies.append(e_p)
            print(f"E_{p} = {e_p:.6f}")
        
        # Check if balanced
        all_energies = [energy_1['analytic']] + val_energies
        mean_energy = np.mean(all_energies)
        std_energy = np.std(all_energies)
        cv = std_energy / mean_energy if mean_energy > 0 else 0
        
        print(f"\nMean energy per channel: {mean_energy:.6f}")
        print(f"Std deviation: {std_energy:.6f}")
        print(f"Coefficient of variation: {cv:.3f}")
        
        results.append({
            'primes': primes,
            'energies': all_energies,
            'mean': mean_energy,
            'std': std_energy,
            'cv': cv
        })
    
    # Plot energy distribution for different prime sets
    fig, axes = plt.subplots(1, len(prime_sets), figsize=(15, 5))
    
    if len(prime_sets) == 1:
        axes = [axes]
    
    for i, (result, ax) in enumerate(zip(results, axes)):
        labels = ['E_∞'] + [f'E_{p}' for p in result['primes']]
        colors = ['blue'] + ['red', 'green', 'orange', 'purple', 'brown'][:len(result['primes'])]
        
        bars = ax.bar(labels, result['energies'], color=colors[:len(labels)], alpha=0.7)
        ax.axhline(y=result['mean'], color='black', linestyle='--', linewidth=2, label='Mean')
        
        ax.set_ylabel('Energy', fontsize=12)
        ax.set_title(f"Primes: {result['primes']}\nCV={result['cv']:.3f}", fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        # Rotate x-axis labels
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('/tmp/experiment4_multiple_primes.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved to: /tmp/experiment4_multiple_primes.png")
    
    return results


def run_all_experiments():
    """
    Run all experiments and generate comprehensive report.
    """
    print("\n" + "=" * 70)
    print("RUNNING ALL BI-LAPLACIAN EXPERIMENTS")
    print("=" * 70)
    
    exp1_results = experiment_1_energy_decomposition(n_modes=10)
    exp2_results = experiment_2_valuation_invariance()
    exp3_results = experiment_3_scaling()
    exp4_results = experiment_4_multiple_primes()
    
    print("\n" + "=" * 70)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 70)
    print("\nGenerated visualizations:")
    print("  - /tmp/experiment1_energy_decomposition.png")
    print("  - /tmp/experiment2_valuation_invariance.png")
    print("  - /tmp/experiment3_scaling.png")
    print("  - /tmp/experiment4_multiple_primes.png")
    
    return {
        'exp1': exp1_results,
        'exp2': exp2_results,
        'exp3': exp3_results,
        'exp4': exp4_results
    }


if __name__ == "__main__":
    results = run_all_experiments()
