# Hybrid Quantum Optimization

Technical report and companion code for a three-layer hybrid architecture: quantum sampling (QAOA), classical refinement, and formal verification.

**DOI:** [10.5281/zenodo.22765909](https://doi.org/10.5281/zenodo.22765909)

## Authors

- Raja Ram M (main author, R&D) - Krypur Quantum R&D, Kryptur OU
- Muskan S (contributor, project infrastructure) - Data T Research Org
- Vipul Jain (contributor, digital and cloud networks) - AE Quantum Research Division
- Kalinga Swain (contributor, quantum and AI) - Zius Quantum R&D Center
- Data manager: Borel Sigma Data Center

ORCID records are linked from the formatted paper via icons, not as raw locator strings in the running text.

## Paper

- Formatted report: [`paper/Hybrid-Quantum-Optimization.html`](paper/Hybrid-Quantum-Optimization.html)
- Printable PDF: [`paper/Hybrid-Quantum-Optimization.pdf`](paper/Hybrid-Quantum-Optimization.pdf)
- Source markdown: [`paper/Hybrid-Quantum-Optimization.md`](paper/Hybrid-Quantum-Optimization.md)

## Code

| File | Role |
|---|---|
| `src/qaoa_route.py` | Cost Hamiltonian and QAOA circuit construction |
| `src/qaoa_optimizer.py` | Classical loop over variational angles |
| `src/postprocess.py` | Greedy bit-flip refinement and optimality ratios |
| `src/plot_distribution.py` | Raw versus refined sample histograms |

Hardware job records in `data/` use a generic gate-model backend label. Figures used in the paper live in `paper/figures/`.

## License

Code is released under MIT. The report text is released under CC-BY 4.0.
