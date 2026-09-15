# postprocess.py
"""
Classical post-processing for QPU QAOA results.

Loads the most recent scaled-run JSON, applies greedy bit-flip refinement,
and writes a sibling *_refined.json file with both raw and refined metrics.
"""
import json
from pathlib import Path

QUANTUM_DIR = Path(__file__).resolve().parents[1] / "data"


def penalty(bitstring: str) -> int:
    return sum(1 for i in range(len(bitstring) - 1) if bitstring[i] == bitstring[i + 1])


def greedy_refine(bitstring: str) -> str:
    best = bitstring
    best_p = penalty(best)
    improved = True
    while improved:
        improved = False
        for i in range(len(best)):
            flipped = list(best)
            flipped[i] = "1" if flipped[i] == "0" else "0"
            cand = "".join(flipped)
            p = penalty(cand)
            if p < best_p:
                best, best_p = cand, p
                improved = True
                break
    return best


def main():
    files = sorted(QUANTUM_DIR.glob("run_scaled_*.json"))
    files = [f for f in files if "_refined" not in f.name]
    if not files:
        raise SystemExit("No scaled run JSON found. Place a run_scaled_*.json record in data/ first.")

    latest = files[-1]
    data = json.loads(latest.read_text())
    counts = data["counts"]
    total = sum(counts.values())

    raw_optimal = sum(c for b, c in counts.items() if penalty(b) == 0)
    raw_ratio = raw_optimal / total

    refined_counts = {}
    refined_optimal = 0
    for b, c in counts.items():
        rb = greedy_refine(b)
        refined_counts[rb] = refined_counts.get(rb, 0) + c
        if penalty(rb) == 0:
            refined_optimal += c
    refined_ratio = refined_optimal / total

    enriched = dict(data)
    enriched.update({
        "source_file": latest.name,
        "raw_optimality_ratio": raw_ratio,
        "refined_optimality_ratio": refined_ratio,
        "refinement_improvement_pp": (refined_ratio - raw_ratio) * 100,
        "refined_counts": refined_counts,
    })

    out = QUANTUM_DIR / f"{latest.stem}_refined.json"
    out.write_text(json.dumps(enriched, indent=2))

    print(f"Loaded: {latest.name}")
    print(f"Qubits: {data['num_qubits']}, depth: {data['depth']}, gates: {data['gates']}")
    print(f"Total shots: {total}")
    print(f"Raw optimality ratio:     {raw_ratio:.2%}  ({raw_optimal} shots)")
    print(f"Refined optimality ratio: {refined_ratio:.2%}  ({refined_optimal} shots)")
    print(f"Improvement: +{(refined_ratio - raw_ratio) * 100:.2f} percentage points")
    print(f"Saved refined record: {out.name}")


if __name__ == "__main__":
    main()
