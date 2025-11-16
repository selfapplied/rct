"""
Tests for the Bi-Laplacian Hamiltonian implementation.
"""

import numpy as np
import pytest
from src.quantum.bi_laplacian import BiLaplacianHamiltonian


class TestBiLaplacianHamiltonian:
    """Test suite for BiLaplacianHamiltonian class."""
    
    def test_initialization(self):
        """Test basic initialization."""
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3])
        
        assert ham.N_t == 50
        assert ham.primes == [2, 3]
        assert len(ham.weights) == 2
        assert ham.H.shape == (50, 50)
    
    def test_custom_weights(self):
        """Test initialization with custom weights."""
        weights = [0.5, 1.5]
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3], weights=weights)
        
        assert ham.weights == weights
    
    def test_weight_length_mismatch(self):
        """Test that mismatched weights and primes raises error."""
        with pytest.raises(ValueError):
            BiLaplacianHamiltonian(N_t=50, primes=[2, 3], weights=[1.0])
    
    def test_hamiltonian_hermitian(self):
        """Test that Hamiltonian is Hermitian (real symmetric)."""
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3])
        
        # Check if H is symmetric (Hermitian for real matrices)
        assert np.allclose(ham.H, ham.H.T), "Hamiltonian should be symmetric"
    
    def test_ground_state_zero_energy(self):
        """Test that ground state has near-zero energy."""
        ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3])
        eigenvalues = ham.get_eigenvalues(5)
        
        # Ground state should have energy very close to 0
        assert abs(eigenvalues[0]) < 1e-10, f"Ground state energy = {eigenvalues[0]}, expected ≈ 0"
    
    def test_eigenvalues_real(self):
        """Test that all eigenvalues are real."""
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3])
        eigenvalues = ham.get_eigenvalues()
        
        assert np.all(np.isreal(eigenvalues)), "All eigenvalues should be real"
    
    def test_eigenvalues_ordered(self):
        """Test that eigenvalues are returned in ascending order."""
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3])
        eigenvalues = ham.get_eigenvalues(10)
        
        # Check if sorted
        assert np.all(eigenvalues[:-1] <= eigenvalues[1:]), "Eigenvalues should be sorted"
    
    def test_eigenvectors_normalized(self):
        """Test that eigenvectors are normalized."""
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3])
        
        for i in range(5):
            psi = ham.get_eigenstate(i)
            norm = np.linalg.norm(psi)
            assert abs(norm - 1.0) < 1e-10, f"Eigenvector {i} norm = {norm}, expected 1.0"
    
    def test_ground_state_constant(self):
        """Test that ground state is approximately constant (uniform)."""
        ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3])
        psi_0 = ham.get_eigenstate(0)
        
        # Ground state should be constant up to numerical precision
        # All elements should have similar magnitude
        magnitudes = np.abs(psi_0)
        assert np.std(magnitudes) < 0.01, "Ground state should be approximately constant"
    
    def test_ground_state_shift_invariant(self):
        """Test that ground state is invariant under prime shifts."""
        ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3])
        
        for p in ham.primes:
            inv = ham.check_valuation_invariance(0, p)
            assert inv < 1e-10, f"Ground state should be invariant under shift by {p}, got {inv}"
    
    def test_energy_decomposition_sums(self):
        """Test that energy decomposition components sum to total energy."""
        ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3])
        
        for n in range(5):
            energy = ham.decompose_energy(n)
            
            computed_sum = energy['analytic']
            for p in ham.primes:
                computed_sum += energy[f'p={p}']
            
            assert abs(computed_sum - energy['total']) < 1e-10, \
                f"Energy components don't sum to total for mode {n}"
    
    def test_analytic_energy_matches_theory(self):
        """Test that first excited state analytic energy matches (π/T)²."""
        N_t = 100
        T = np.log(N_t)
        ham = BiLaplacianHamiltonian(N_t=N_t, T=T, primes=[2, 3])
        
        energy = ham.decompose_energy(1)
        theoretical = (np.pi / T)**2
        
        # Should match to within 1% relative error
        rel_error = abs(energy['analytic'] - theoretical) / theoretical
        assert rel_error < 0.01, \
            f"Analytic energy = {energy['analytic']}, theoretical = {theoretical}, rel_error = {rel_error}"
    
    def test_multiple_primes(self):
        """Test that system works with more primes."""
        primes_list = [[2], [2, 3], [2, 3, 5], [2, 3, 5, 7]]
        
        for primes in primes_list:
            ham = BiLaplacianHamiltonian(N_t=50, primes=primes)
            eigenvalues = ham.get_eigenvalues(3)
            
            # Check that we get reasonable results
            assert eigenvalues[0] < 1e-10, "Ground state should have ~0 energy"
            assert eigenvalues[1] > 0, "First excited state should have positive energy"
            assert eigenvalues[2] >= eigenvalues[1], "Eigenvalues should be ascending"
    
    def test_shift_operator(self):
        """Test that shift operator shifts correctly."""
        ham = BiLaplacianHamiltonian(N_t=10, primes=[2, 3])
        
        # Test shift by 2
        # S_p psi[i] = psi[(i + p) mod N_t], which is like roll(-p)
        S_2 = ham._build_shift_operator(2)
        test_vec = np.arange(10)
        shifted = S_2 @ test_vec
        expected = np.roll(test_vec, -2)
        
        assert np.allclose(shifted, expected), "Shift operator should shift indices correctly"
    
    def test_different_grid_sizes(self):
        """Test that system works with different grid sizes."""
        for N_t in [20, 50, 100, 200]:
            ham = BiLaplacianHamiltonian(N_t=N_t, primes=[2, 3])
            eigenvalues = ham.get_eigenvalues(3)
            
            assert abs(eigenvalues[0]) < 1e-8, f"Ground state energy should be ~0 for N_t={N_t}"
            assert eigenvalues[1] > 0, f"First excited state should be positive for N_t={N_t}"


class TestEnergyDecomposition:
    """Test energy decomposition functionality."""
    
    def test_valuation_energies_positive(self):
        """Test that valuation energies are non-negative."""
        ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3])
        
        for n in range(5):
            energy = ham.decompose_energy(n)
            
            for p in ham.primes:
                e_p = energy[f'p={p}']
                assert e_p >= -1e-10, f"Valuation energy E_{p} should be non-negative, got {e_p}"
    
    def test_energy_scales_with_mode(self):
        """Test that energy generally increases with mode number."""
        ham = BiLaplacianHamiltonian(N_t=100, primes=[2, 3])
        
        energies = [ham.decompose_energy(n)['total'] for n in range(10)]
        
        # Most should be increasing (allowing for some degeneracies)
        increases = sum(1 for i in range(len(energies)-1) if energies[i+1] >= energies[i] - 1e-10)
        assert increases >= 7, "Energy should generally increase with mode number"


class TestVisualization:
    """Test visualization functions (check they run without error)."""
    
    def test_plot_eigenstate(self):
        """Test that plotting eigenstate doesn't crash."""
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3])
        
        # Should not raise an exception
        fig = ham.plot_eigenstate(1, filename=None, show_grid=True)
        assert fig is not None
    
    def test_plot_spectrum(self):
        """Test that plotting spectrum doesn't crash."""
        ham = BiLaplacianHamiltonian(N_t=50, primes=[2, 3])
        
        # Should not raise an exception
        fig = ham.plot_eigenvalue_spectrum(n_max=10, filename=None)
        assert fig is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
