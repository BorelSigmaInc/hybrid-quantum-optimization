# plot_distribution.py
"""
Plot raw vs refined QAOA distributions from the latest refined record.
Saves a PNG to data/quantum/.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

QUANTUM_DIR = Path(__file__).resolve().parents[1] / "data"


def penalty(b: str) -> int:
    return sum(1 for i in range(len(b) - 1) if b[i] == b[i + 1])


def main():
    files = sorted(QUANTUM_DIR.glob("*_refined.json"))
    if not files:
        raise SystemExit("No refined JSON found. Run postprocess.py first.")
    data = json.loads(files[-1].read_text())

    raw = data["counts"]
    refined = data["refined_counts"]

    raw_items = sorted(raw.items(), key=lambda x: -x[1])[:30]
    ref_items = sorted(refined.items(), key=lambda x: -x[1])[:30]

    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    labels_r = [b for b, _ in raw_items]
    vals_r = [c for _, c in raw_items]
    colors_r = ["#2ca02c" if penalty(b) == 0 else "#1f77b4" for b in labels_r]
    axes[0].bar(range(len(labels_r)), vals_r, color=colors_r)
    axes[0].set_xticks(range(len(labels_r)))
    axes[0].set_xticklabels(labels_r, rotation=90, fontsize=6)
    axes[0].set_title(f"Raw QPU Distribution (top 30 of 256) - ratio {data['raw_optimality_ratio']:.2%}")
    axes[0].set_ylabel("Shots")

    labels_f = [b for b, _ in ref_items]
    vals_f = [c for _, c in ref_items]
    colors_f = ["#2ca02c" if penalty(b) == 0 else "#d62728" for b in labels_f]
    axes[1].bar(range(len(labels_f)), vals_f, color=colors_f)
    axes[1].set_xticks(range(len(labels_f)))
    axes[1].set_xticklabels(labels_f, rotation=90, fontsize=7)
    axes[1].set_title(f"Refined Distribution (26 attractors) - ratio {data['refined_optimality_ratio']:.2%}")
    axes[1].set_ylabel("Shots")

    plt.tight_layout()
    out = QUANTUM_DIR / f"distribution_{data['job_id']}.png"
    plt.savefig(out, dpi=140)
    print(f"Saved plot: {out}")
    print(f"Raw support: {len(raw)}  Refined support: {len(refined)}")
    print(f"Raw ratio: {data['raw_optimality_ratio']:.2%}  Refined ratio: {data['refined_optimality_ratio']:.2%}")


if __name__ == "__main__":
    main()
