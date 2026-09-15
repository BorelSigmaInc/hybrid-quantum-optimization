# src/quantum/qaoa_optimizer.py
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator

def build_cost_hamiltonian(n_qubits: int = 4) -> SparsePauliOp:
    pauli_list = []
    for i in range(n_qubits - 1):
        label = ["I"] * n_qubits
        label[i] = "Z"
        label[i + 1] = "Z"
        pauli_list.append(("".join(reversed(label)), 1.0))
    return SparsePauliOp.from_list(pauli_list)

def build_qaoa_circuit(n_qubits: int = 4, reps: int = 1) -> QuantumCircuit:
    cost = build_cost_hamiltonian(n_qubits)
    ansatz = QAOAAnsatz(cost_operator=cost, reps=reps)
    ansatz.measure_all()
    return ansatz

def energy_from_counts(counts: dict, n_qubits: int) -> float:
    total = sum(counts.values())
    e = 0.0
    for bitstring, count in counts.items():
        penalty = sum(1 for i in range(len(bitstring) - 1) if bitstring[i] == bitstring[i + 1])
        e += penalty * count
    return e / total

def run_qaoa(params, circuit, sim, shots=1024):
    bound = circuit.assign_parameters(params)
    compiled = transpile(bound, sim)
    result = sim.run(compiled, shots=shots).result()
    return result.get_counts()

if __name__ == "__main__":
    n = 4
    reps = 1
    circuit = build_qaoa_circuit(n, reps=reps)
    sim = AerSimulator()

    print(f"QAOA circuit: {n} qubits, reps {reps}, depth {circuit.depth()}, gates {circuit.size()}")

    history = []
    def objective(params):
        counts = run_qaoa(params, circuit, sim, shots=512)
        e = energy_from_counts(counts, n)
        history.append((list(params), e))
        return e

    x0 = [0.5, 0.5]
    print(f"Starting parameters: gamma={x0[0]}, beta={x0[1]}")
    res = minimize(objective, x0, method="COBYLA", options={"maxiter": 20, "rhobeg": 0.3})

    print(f"\nOptimizer finished: {res.nfev} evaluations")
    print(f"Optimal parameters: gamma={res.x[0]:.4f}, beta={res.x[1]:.4f}")
    print(f"Optimal energy: {res.fun:.4f}")

    print("\nEnergy trajectory (first 10):")
    for i, (p, e) in enumerate(history[:10]):
        print(f"  iter {i:02d}: gamma={p[0]:.3f}, beta={p[1]:.3f}, energy={e:.4f}")

    best_counts = run_qaoa(res.x, circuit, sim, shots=1024)
    print("\nTop 5 outcomes at optimal parameters:")
    for bitstring, count in sorted(best_counts.items(), key=lambda x: -x[1])[:5]:
        penalty = sum(1 for i in range(len(bitstring) - 1) if bitstring[i] == bitstring[i + 1])
        print(f"  {bitstring}: {count}  (penalty={penalty})")
