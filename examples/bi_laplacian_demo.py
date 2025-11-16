#!/usr/bin/env python3
"""
Demonstration script for the Bi-Laplacian Hamiltonian implementation.

This script shows how to use the BiLaplacianHamiltonian class to:
1. Build and analyze the spectrum
2. Decompose energy into analytic and valuation parts
3. Check valuation invariance
4. Visualize eigenstates
5. Run extended experiments
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.quantum.bi_laplacian import BiLaplacianHamiltonian


def demo_basic_usage():
    """Demonstrate basic usage of the BiLaplacianHamiltonian class."""
    print("=" * 70)
    print("BASIC USAGE DEMO")
    print("=" * 70)

    # Create a Hamiltonian with N_t=100 grid points and primes {2, 3}
    print("\n1. Creating Hamiltonian...")
    ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3], weights=[1.0, 1.0])
    print(f"   Grid points: {ham.N_t}")
    print(f"   Period T: {ham.T:.5f}")
    print(f"   Primes: {ham.primes}")

    # Compute first 10 eigenvalues
    print("\n2. Computing eigenvalues...")
    eigenvalues = ham.get_eigenvalues(10)
    print("   First 5 eigenvalues:")
    for i in range(5):
        print(f"     λ_{i} = {eigenvalues[i]:.6f}")

    # Get an eigenstate
    print("\n3. Getting eigenstate ψ_1...")
    psi_1 = ham.get_eigenstate(1)
    print(f"   Shape: {psi_1.shape}")
    print(f"   Norm: {np.linalg.norm(psi_1):.10f}")

    # Decompose energy
    print("\n4. Decomposing energy for ψ_1...")
    energy = ham.decompose_energy(1)
    print(f"   Total energy:    {energy['total']:.6f}")
    print(f"   Analytic (E_∞):  {energy['analytic']:.6f}")
    print(f"   E_2:             {energy['p=2']:.6f}")
    print(f"   E_3:             {energy['p=3']:.6f}")

    # Check theoretical prediction
    theoretical = (np.pi / ham.T)**2
    print(f"   Theoretical (π/T)²: {theoretical:.6f}")
    print(f"   Match: {abs(energy['analytic'] - theoretical) / theoretical * 100:.3f}%")

    # Check valuation invariance
    print("\n5. Checking valuation invariance...")
    for p in ham.primes:
        inv = ham.check_valuation_invariance(1, p)
        print(f"   ||ψ_1({p}x) - ψ_1(x)|| / ||ψ_1|| = {inv:.6f}")

    print("\n   For ground state ψ_0:")
    for p in ham.primes:
        inv = ham.check_valuation_invariance(0, p)
        print(f"   ||ψ_0({p}x) - ψ_0(x)|| / ||ψ_0|| = {inv:.6f}")

    return ham


def demo_visualization(ham):
    """Demonstrate visualization capabilities."""
    print("\n" + "=" * 70)
    print("VISUALIZATION DEMO")
    print("=" * 70)

    # Plot spectrum
    print("\n1. Plotting eigenvalue spectrum...")
    ham.plot_eigenvalue_spectrum(n_max=20, filename='/tmp/demo_spectrum.png')
    print("   Saved to: /tmp/demo_spectrum.png")

    # Plot eigenstates
    print("\n2. Plotting ground state (ψ_0)...")
    ham.plot_eigenstate(0, filename='/tmp/demo_psi0.png')
    print("   Saved to: /tmp/demo_psi0.png")

    print("\n3. Plotting first excited state (ψ_1)...")
    ham.plot_eigenstate(1, filename='/tmp/demo_psi1.png')
    print("   Saved to: /tmp/demo_psi1.png")


def demo_parameter_sweep():
    """Demonstrate parameter sweep over different configurations."""
    print("\n" + "=" * 70)
    print("PARAMETER SWEEP DEMO")
    print("=" * 70)

    print("\n1. Varying grid size (N_t)...")
    for N_t in [50, 100, 200]:
        ham = BiLaplacianHamiltonian(N_t=N_t, primes=[2, 3])
        eigenvalues = ham.get_eigenvalues(3)
        print(f"   N_t={N_t:3d}: λ_0={eigenvalues[0]:.8f}, λ_1={eigenvalues[1]:.6f}")

    print("\n2. Varying number of primes...")
    for primes in [[2], [2, 3], [2, 3, 5], [2, 3, 5, 7]]:
        ham = BiLaplacianHamiltonian(N_t=100, primes=primes)
        eigenvalues = ham.get_eigenvalues(3)

        n_channels = 1 + len(primes)  # analytic + valuation channels
        print(f"   Primes {primes}: λ_1={eigenvalues[1]:.4f}, "
              f"{n_channels} channels")

    print("\n3. Varying weights...")
    for w in [0.5, 1.0, 2.0]:
        ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3], weights=[w, w])
        eigenvalues = ham.get_eigenvalues(3)
        print(f"   w={w:.1f}: λ_0={eigenvalues[0]:.8f}, λ_1={eigenvalues[1]:.6f}")


def demo_extended_experiments():
    """Demonstrate how to run extended experiments."""
    print("\n" + "=" * 70)
    print("EXTENDED EXPERIMENTS DEMO")
    print("=" * 70)

    from src.quantum import bi_laplacian_experiments

    print("\n1. Energy decomposition for multiple modes...")
    results = bi_laplacian_experiments.experiment_1_energy_decomposition(n_modes=5)
    print(f"   Computed energy for {len(results)} modes")

    print("\n2. Valuation invariance analysis...")
    results = bi_laplacian_experiments.experiment_2_valuation_invariance()
    print(f"   Analyzed {len(results['n'])} modes")

    print("\n3. Scaling behavior...")
    results = bi_laplacian_experiments.experiment_3_scaling()
    print(f"   Tested {len(results['N_t'])} grid sizes")

    print("\n4. Multiple primes analysis...")
    results = bi_laplacian_experiments.experiment_4_multiple_primes()
    print(f"   Tested {len(results)} prime configurations")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("BI-LAPLACIAN HAMILTONIAN DEMONSTRATION")
    print("=" * 70)
    print("\nThis script demonstrates the key features of the")
    print("BiLaplacianHamiltonian implementation.")

    # Basic usage
    ham = demo_basic_usage()

    # Visualization
    demo_visualization(ham)

    # Parameter sweep
    demo_parameter_sweep()

    # Extended experiments
    demo_extended_experiments()

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - /tmp/demo_spectrum.png")
    print("  - /tmp/demo_psi0.png")
    print("  - /tmp/demo_psi1.png")
    print("  - /tmp/experiment1_energy_decomposition.png")
    print("  - /tmp/experiment2_valuation_invariance.png")
    print("  - /tmp/experiment3_scaling.png")
    print("  - /tmp/experiment4_multiple_primes.png")
    print("\nFor more information, see docs/bi_laplacian_analysis.md")


if __name__ == "__main__":
    main()
