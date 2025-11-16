# Examples

This directory contains example scripts demonstrating various features of the RCT framework.

## Bi-Laplacian Hamiltonian Demo

**File:** `bi_laplacian_demo.py`

Comprehensive demonstration of the Bi-Laplacian Hamiltonian implementation, showing:

1. **Basic Usage**
   - Creating a Hamiltonian
   - Computing eigenvalues
   - Getting eigenstates
   - Decomposing energy
   - Checking valuation invariance

2. **Visualization**
   - Plotting eigenvalue spectrum
   - Plotting ground state
   - Plotting excited states

3. **Parameter Sweeps**
   - Varying grid size (N_t)
   - Varying number of primes
   - Varying weights

4. **Extended Experiments**
   - Energy decomposition for multiple modes
   - Valuation invariance analysis
   - Scaling behavior
   - Multiple primes analysis

### Running the Demo

```bash
cd /home/runner/work/rct/rct
python3 examples/bi_laplacian_demo.py
```

### Expected Output

The demo will:
- Print detailed analysis to console
- Generate 7 visualization plots in `/tmp/`:
  - `demo_spectrum.png`
  - `demo_psi0.png`
  - `demo_psi1.png`
  - `experiment1_energy_decomposition.png`
  - `experiment2_valuation_invariance.png`
  - `experiment3_scaling.png`
  - `experiment4_multiple_primes.png`

### Sample Output

```
======================================================================
BASIC USAGE DEMO
======================================================================

1. Creating Hamiltonian...
   Grid points: 100
   Period T: 4.60517
   Primes: [2, 3]

2. Computing eigenvalues...
   First 5 eigenvalues:
     λ_0 = 0.000000
     λ_1 = 0.527403
     λ_2 = 0.527403
     λ_3 = 2.106220
     λ_4 = 2.106220

4. Decomposing energy for ψ_1...
   Total energy:    0.527403
   Analytic (E_∞):  0.465228
   E_2:             0.032824
   E_3:             0.029351
   Theoretical (π/T)²: 0.465381
   Match: 0.033%
```

## More Information

For detailed documentation on the Bi-Laplacian implementation, see:
- `docs/bi_laplacian_analysis.md` - Complete analysis and theory
- `src/quantum/bi_laplacian.py` - Core implementation
- `tests/test_bi_laplacian.py` - Test suite
