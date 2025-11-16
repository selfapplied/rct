"""
Bi-Laplacian Hamiltonian on the Adeles

This module implements the bi-Laplacian Hamiltonian combining:
- Analytic part (periodic Laplacian on a circle)
- Valuation parts (prime p-adic shifts)

Following the Tetragraphic framework for quantum field on the adeles.
"""

import numpy as np
from scipy.linalg import eigh
from typing import List, Tuple, Dict, Optional
import matplotlib.pyplot as plt


class BiLaplacianHamiltonian:
    """
    Bi-Laplacian Hamiltonian: H_N = L_D + sum_p w_p H_p

    where:
    - L_D is the discrete Laplacian (analytic part)
    - H_p = (S_p - I)^dagger (S_p - I) / (log p)^2 for each prime p
    - S_p is the shift operator by p positions
    """

    def __init__(
        self,
        N_t: int = 100,
        T: Optional[float] = None,
        primes: List[int] = None,
        weights: Optional[List[float]] = None
    ):
        """
        Initialize the Bi-Laplacian Hamiltonian.

        Args:
            N_t: Number of grid points in the analytic direction
            T: Half-period for periodic boundary conditions (defaults to log(N_t))
            primes: List of primes for valuation parts (default: [2, 3])
            weights: Weights for each prime (default: all 1s)
        """
        self.N_t = N_t
        self.T = T if T is not None else np.log(N_t)
        self.primes = primes if primes is not None else [2, 3]
        self.weights = weights if weights is not None else [1.0] * len(self.primes)

        if len(self.weights) != len(self.primes):
            raise ValueError("Length of weights must match length of primes")

        # Build the Hamiltonian
        self.H = self._build_hamiltonian()

        # Store eigenvalues and eigenvectors (computed on demand)
        self._eigenvalues = None
        self._eigenvectors = None

    def _build_laplacian(self) -> np.ndarray:
        """
        Build the discrete Laplacian operator with periodic boundary conditions.

        Returns negative of second-order finite difference approximation:
        L_D[i,j] = -(psi[i-1] - 2*psi[i] + psi[i+1]) / h^2

        This gives positive eigenvalues for the Laplacian operator.
        """
        h = 2 * self.T / self.N_t
        L_D = np.zeros((self.N_t, self.N_t))

        for i in range(self.N_t):
            L_D[i, i] = 2.0 / h**2
            L_D[i, (i + 1) % self.N_t] = -1.0 / h**2
            L_D[i, (i - 1) % self.N_t] = -1.0 / h**2

        return L_D

    def _build_shift_operator(self, p: int) -> np.ndarray:
        """
        Build shift operator S_p that shifts indices by p positions.

        S_p psi[i] = psi[(i + p) mod N_t]
        """
        S_p = np.zeros((self.N_t, self.N_t))
        for i in range(self.N_t):
            S_p[i, (i + p) % self.N_t] = 1.0
        return S_p

    def _build_prime_hamiltonian(self, p: int) -> np.ndarray:
        """
        Build the prime valuation Hamiltonian:
        H_p = (S_p - I)^dagger (S_p - I) / (log p)^2
        """
        S_p = self._build_shift_operator(p)
        identity = np.eye(self.N_t)
        D_p = S_p - identity

        # H_p = D_p^dagger D_p / (log p)^2
        H_p = (D_p.conj().T @ D_p) / (np.log(p)**2)

        return H_p

    def _build_hamiltonian(self) -> np.ndarray:
        """
        Build the full bi-Laplacian Hamiltonian:
        H_N = L_D + sum_p w_p H_p
        """
        # Start with the Laplacian (analytic part)
        H = self._build_laplacian()

        # Add prime valuation parts
        for p, w in zip(self.primes, self.weights):
            H_p = self._build_prime_hamiltonian(p)
            H += w * H_p

        return H

    def compute_spectrum(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute eigenvalues and eigenvectors of the Hamiltonian.

        Returns:
            eigenvalues: Array of eigenvalues (sorted ascending)
            eigenvectors: Array of eigenvectors (columns)
        """
        if self._eigenvalues is None or self._eigenvectors is None:
            # Use scipy's eigh for Hermitian matrices (real symmetric in this case)
            self._eigenvalues, self._eigenvectors = eigh(self.H)

        return self._eigenvalues, self._eigenvectors

    def get_eigenvalues(self, n: Optional[int] = None) -> np.ndarray:
        """
        Get the first n eigenvalues (or all if n is None).
        """
        eigenvalues, _ = self.compute_spectrum()
        return eigenvalues[:n] if n is not None else eigenvalues

    def get_eigenstate(self, n: int) -> np.ndarray:
        """
        Get the n-th eigenstate (eigenfunction).
        """
        _, eigenvectors = self.compute_spectrum()
        return eigenvectors[:, n]

    def compute_analytic_energy(self, psi: np.ndarray) -> float:
        """
        Compute the analytic (Laplacian) energy contribution:
        E_infty(psi) = <psi | L_D | psi>
        """
        L_D = self._build_laplacian()
        return np.real(psi.conj().T @ L_D @ psi)

    def compute_valuation_energy(self, psi: np.ndarray, p: int) -> float:
        """
        Compute the valuation energy contribution for prime p:
        E_p(psi) = <psi | H_p | psi>
        """
        H_p = self._build_prime_hamiltonian(p)
        return np.real(psi.conj().T @ H_p @ psi)

    def decompose_energy(self, n: int) -> Dict[str, float]:
        """
        Decompose the energy of eigenstate n into analytic and valuation parts.

        Returns dictionary with keys:
        - 'total': Total energy (eigenvalue)
        - 'analytic': E_infty contribution
        - 'p' for each prime p: E_p contribution
        """
        eigenvalues, _ = self.compute_spectrum()
        psi_n = self.get_eigenstate(n)

        result = {
            'total': eigenvalues[n],
            'analytic': self.compute_analytic_energy(psi_n)
        }

        for p, w in zip(self.primes, self.weights):
            result[f'p={p}'] = w * self.compute_valuation_energy(psi_n, p)

        return result

    def check_valuation_invariance(self, n: int, p: int) -> float:
        """
        Check valuation invariance: ||psi(px) - psi(x)||

        Returns the normalized difference as a measure of non-invariance.
        """
        psi = self.get_eigenstate(n)
        S_p = self._build_shift_operator(p)
        psi_shifted = S_p @ psi

        diff_norm = np.linalg.norm(psi_shifted - psi)
        psi_norm = np.linalg.norm(psi)

        return diff_norm / psi_norm if psi_norm > 0 else 0.0

    def plot_eigenstate(
        self,
        n: int,
        filename: Optional[str] = None,
        show_grid: bool = True
    ):
        """
        Plot the n-th eigenstate.

        Args:
            n: Index of eigenstate to plot
            filename: If provided, save plot to this file
            show_grid: Whether to show grid lines
        """
        psi = self.get_eigenstate(n)
        t_grid = np.linspace(-self.T, self.T, self.N_t)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Real part
        ax1.plot(t_grid, np.real(psi), 'b-', linewidth=2, label='Real part')
        ax1.set_xlabel('t', fontsize=12)
        ax1.set_ylabel(f'Re(ψ_{{{n}}})', fontsize=12)
        ax1.set_title(f'Eigenstate ψ_{{{n}}} - Real Part', fontsize=14)
        ax1.grid(show_grid, alpha=0.3)
        ax1.legend()

        # Imaginary part
        ax2.plot(t_grid, np.imag(psi), 'r-', linewidth=2, label='Imaginary part')
        ax2.set_xlabel('t', fontsize=12)
        ax2.set_ylabel(f'Im(ψ_{{{n}}})', fontsize=12)
        ax2.set_title(f'Eigenstate ψ_{{{n}}} - Imaginary Part', fontsize=14)
        ax2.grid(show_grid, alpha=0.3)
        ax2.legend()

        plt.tight_layout()

        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')

        return fig

    def plot_eigenvalue_spectrum(
        self,
        n_max: int = 20,
        filename: Optional[str] = None
    ):
        """
        Plot the eigenvalue spectrum.
        """
        eigenvalues = self.get_eigenvalues(n_max)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(range(len(eigenvalues)), eigenvalues, 'bo-', markersize=8, linewidth=2)
        ax.set_xlabel('Eigenvalue index n', fontsize=12)
        ax.set_ylabel('λ_n', fontsize=12)
        ax.set_title(f'Bi-Laplacian Eigenvalue Spectrum (first {n_max} modes)', fontsize=14)
        ax.grid(True, alpha=0.3)

        # Annotate first few eigenvalues
        for i in range(min(5, len(eigenvalues))):
            ax.annotate(
                f'λ_{{{i}}}={eigenvalues[i]:.4f}',
                xy=(i, eigenvalues[i]),
                xytext=(10, 10),
                textcoords='offset points',
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5)
            )

        plt.tight_layout()

        if filename:
            plt.savefig(filename, dpi=150, bbox_inches='tight')

        return fig


def run_basic_experiment():
    """
    Run the basic experiment as described in the problem statement.
    """
    print("=" * 70)
    print("BI-LAPLACIAN HAMILTONIAN - BASIC EXPERIMENT")
    print("=" * 70)

    # Setup matching the problem statement
    N_t = 100
    T = np.log(N_t)
    primes = [2, 3]
    weights = [1.0, 1.0]

    print("\nParameters:")
    print(f"  N_t = {N_t}")
    print(f"  T = {T:.5f}")
    print(f"  Primes: {primes}")
    print(f"  Weights: {weights}")

    # Build Hamiltonian
    ham = BiLaplacianHamiltonian(N_t=N_t, T=T, primes=primes, weights=weights)

    # Compute spectrum
    print("\n" + "-" * 70)
    print("EIGENVALUE SPECTRUM")
    print("-" * 70)

    eigenvalues = ham.get_eigenvalues(20)
    print("\nFirst 20 eigenvalues:")
    for i, lam in enumerate(eigenvalues):
        print(f"  λ_{i:2d} = {lam:12.8f}")

    # Energy decomposition for first excited state
    print("\n" + "-" * 70)
    print("ENERGY DECOMPOSITION FOR ψ_1 (first excited state)")
    print("-" * 70)

    energy_decomp = ham.decompose_energy(1)
    print(f"\nTotal energy (λ_1):     {energy_decomp['total']:.8f}")
    print(f"Analytic part (E_∞):    {energy_decomp['analytic']:.8f}")
    print(f"Valuation part (E_2):   {energy_decomp['p=2']:.8f}")
    print(f"Valuation part (E_3):   {energy_decomp['p=3']:.8f}")

    sum_valuations = energy_decomp['p=2'] + energy_decomp['p=3']
    print(f"\nSum of valuations:      {sum_valuations:.8f}")
    print(f"Total - Analytic:       {energy_decomp['total'] - energy_decomp['analytic']:.8f}")

    # Check theoretical prediction
    theoretical_first_mode = (np.pi / T)**2
    print(f"\nTheoretical (π/T)²:     {theoretical_first_mode:.8f}")
    print(f"Analytic - Theoretical: {energy_decomp['analytic'] - theoretical_first_mode:.8f}")

    # Energy ratios
    print("\n" + "-" * 70)
    print("ENERGY RATIO ANALYSIS")
    print("-" * 70)

    ratio_analytic = energy_decomp['analytic']
    ratio_2 = energy_decomp['p=2']
    ratio_3 = energy_decomp['p=3']

    print("\nEnergy split (unnormalized):")
    print(f"  Analytic : p=2 : p=3 = {ratio_analytic:.3f} : {ratio_2:.3f} : {ratio_3:.3f}")

    total_energy = ratio_analytic + ratio_2 + ratio_3
    print("\nEnergy split (normalized to 1:1:1 comparison):")
    if total_energy > 0:
        norm_analytic = ratio_analytic / (total_energy / 3)
        norm_2 = ratio_2 / (total_energy / 3)
        norm_3 = ratio_3 / (total_energy / 3)
        print(f"  Analytic : p=2 : p=3 = {norm_analytic:.3f} : {norm_2:.3f} : {norm_3:.3f}")

    # Valuation invariance
    print("\n" + "-" * 70)
    print("VALUATION INVARIANCE CHECK")
    print("-" * 70)

    for p in primes:
        inv = ham.check_valuation_invariance(1, p)
        print(f"\n||ψ_1({p}x) - ψ_1(x)|| / ||ψ_1|| = {inv:.6f}")

    # Compare to ground state
    print("\nFor ground state (ψ_0):")
    for p in primes:
        inv = ham.check_valuation_invariance(0, p)
        print(f"  ||ψ_0({p}x) - ψ_0(x)|| / ||ψ_0|| = {inv:.6f}")

    return ham


if __name__ == "__main__":
    ham = run_basic_experiment()

    # Create visualizations
    print("\n" + "=" * 70)
    print("GENERATING VISUALIZATIONS")
    print("=" * 70)

    print("\nGenerating eigenvalue spectrum plot...")
    ham.plot_eigenvalue_spectrum(n_max=20, filename='/tmp/bi_laplacian_spectrum.png')
    print("  Saved to: /tmp/bi_laplacian_spectrum.png")

    print("\nGenerating ψ_0 (ground state) plot...")
    ham.plot_eigenstate(0, filename='/tmp/bi_laplacian_psi0.png')
    print("  Saved to: /tmp/bi_laplacian_psi0.png")

    print("\nGenerating ψ_1 (first excited state) plot...")
    ham.plot_eigenstate(1, filename='/tmp/bi_laplacian_psi1.png')
    print("  Saved to: /tmp/bi_laplacian_psi1.png")

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)
