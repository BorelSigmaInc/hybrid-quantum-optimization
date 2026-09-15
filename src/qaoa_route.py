# src/quantum/qaoa_route.py
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import QAOAAnsatz
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator

def build_cost_hamiltonian(n_qubits: int = 4) -> SparsePauliOp:
    """Penalize adjacent qubits being equal."""
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

def run_simulation(circuit: QuantumCircuit, params: list, shots: int = 1024) -> dict:
    bound = circuit.assign_parameters(params)
    sim = AerSimulator()
    compiled = transpile(bound, sim)
    result = sim.run(compiled, shots=shots).result()
    return result.get_counts()

if __name__ == "__main__":
    n = 4
    reps = 1
    circuit = build_qaoa_circuit(n, reps=reps)
    print(f"QAOA circuit: {n} qubits, reps {reps}, depth {circuit.depth()}, gates {circuit.size()}")

    # QAOA with reps=1 has 2 free parameters: gamma, beta
    params = [0.5, 0.5]  # placeholder; later replaced by classical optimizer
    print(f"Binding parameters: gamma={params[0]}, beta={params[1]}")

    counts = run_simulation(circuit, params, shots=1024)
    print("Top 5 measurement outcomes:")
    for bitstring, count in sorted(counts.items(), key=lambda x: -x[1])[:5]:
        penalty = sum(1 for i in range(len(bitstring) - 1) if bitstring[i] == bitstring[i+1])
        print(f"  {bitstring}: {count}  (penalty={penalty})")

    best = max(counts, key=counts.get)
    best_penalty = sum(1 for i in range(len(best) - 1) if best[i] == best[i+1])
    print(f"Most frequent solution: {best}  (penalty={best_penalty})")
