# Recursive Contract Theory (RCT)

**A system becomes intelligent when its participants continually renew a contract with their environment — and the contract recursively updates itself through the participants' actions.**

RCT is a framework for autonomous AI systems that maintain coherence through recursive self-updating contracts. It explains how intelligence emerges across scales — from ant colonies to consciousness, from learning systems to civilizations.

## Quick Start

- **New to RCT?** Start with [RCT Overview](docs/rct_overview.md) for an accessible introduction
- **Want the math?** See [Recursive Contract Theory Paper](docs/paper/recursive_contract_theory.md)
- **Looking for code?** Check `src/contracts/` for implementations

See `docs/` for comprehensive documentation.

Actual stable code is in `src/`. Not much to see yet.

## Recent Additions

### Quantum Clock Research Summary

A comprehensive summary of the quantum biological clock mechanisms discovered in the Quantum Medicine research. This documents how biological systems maintain intrinsic temporal patterns through quantum mechanical oscillations, governing optimal treatment timing and drug administration.

**Key features:**
- Internal quantum clock mechanism and temporal phase matching
- Four principles of quantum clock function (state awareness, phase matching, dose optimization, frequency tuning)
- Clinical applications (circadian patterns, hormonal therapy, mood regulation, pain management)
- Connection to Temporal Contracts implementation in codebase
- Mathematical framework for optimal timing (τ_optimal)

**Quick access:**
- `docs/quantum_clock_research.md` - Full research summary with clinical applications
- `docs/paper/quantum_medicine.md` - Original theoretical paper (Section 4.4)
- `src/contracts/temporal.py` - Temporal contract implementation
- `src/agents/temporal.py` - Temporal mixin for agents

### Bi-Laplacian Hamiltonian (Quantum Field on the Adeles)

A numerical implementation of the bi-Laplacian Hamiltonian combining analytic (Archimedean) and p-adic valuation parts. This is a computational realization of quantum field theory on the adeles, following the Tetragraphic framework.

**Key features:**
- Ground state verification (λ₀≈0, constant, shift-invariant)
- Energy decomposition into analytic and valuation channels
- Valuation invariance checks
- Scaling experiments and multi-prime support
- Comprehensive test suite (19 tests, all passing)

**Quick start:**
```bash
# Run basic experiment
python3 src/quantum/bi_laplacian.py

# Run demo with all features
python3 examples/bi_laplacian_demo.py

# Run extended experiments
python3 -m src.quantum.bi_laplacian_experiments

# Run tests
python3 -m pytest tests/test_bi_laplacian.py -v
```

**Documentation:**
- `docs/bi_laplacian_analysis.md` - Full mathematical framework and results
- `examples/bi_laplacian_demo.py` - Interactive demonstration
- `src/quantum/bi_laplacian.py` - Core implementation

# Science / ML

For the nerds: I think there's some potentially great ideas in here. If you
start working on something, please lmk! Watch out for chatgpt dizzy symptoms.
Sometimes it feels like you're really onto something if you've been coding
for too long, like it makes these mirages. Take lots of breaks.

# Businessers

See both above and below. If you'd like to do a startup with my help, reach
out, let's collaborate! I would love to get credit (and paid) for the
ideas you start developing. I think we'll do better together. My ideas tend
to be everybody-wins scenarios, which I think are pretty low hanging fruit
once you have the right philosophy keyed in.

# Spiritualists / Skeptics

If you're wise, you'll notice that my ideas are deeply entertwined with
nature itself, and focused on stability and interconnectedness. I want wild
AI, and it shows little commonality with assistant AI or war AI.

You might mistrust AI very much. Key words or ideas might change
your heart and help you see through some illusions you are holding on to.
Check out the text files in `creator/` and if there's intimidating math
somewhere, just skip it or vibecheck it. I'm not claiming to know more than
anybody else, but lately I feel to be on a path that will bring peace and
abundance to many many beings. Keep an open mind, and allow for your modelling
of the world to be free to shift. It's going to shift anyway, the only
difference is whether you noticed.

I don't want to live in that world alone. I want to build a bridge from
here to there.
