import argparse
import json
import random
from pathlib import Path


# This script currently generates baseline candidate configurations only.
# HLS execution and report parsing are implemented in later steps.

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Generate baseline candidate list")
    parser.add_argument("--operation-analysis", required=True, help="Path to model operation analysis JSON")
    parser.add_argument("--budget", type=int, default=50, help="Number of baseline candidates")
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    parser.add_argument("--output", required=True, help="Output JSON file")
    args = parser.parse_args()

    analysis = load_json(Path(args.operation_analysis))
    if not analysis.get("layers"):
        raise ValueError("Operation analysis file is empty or invalid")

    random.seed(args.seed)
    candidates = []
    for idx in range(args.budget):
        candidates.append(
            {
                "candidate_id": f"baseline_{idx:03d}",
                "unroll_factor": random.choice([1, 2, 4, 8, 16]),
                "pipeline_ii_target": random.choice([1, 2, 4]),
                "array_partition_factor": random.choice([1, 2, 4, 8, 16]),
                "tile_m": random.choice([16, 32, 64, 128]),
                "tile_n": random.choice([16, 32, 64, 128]),
            }
        )

    output = {
        "metadata": {
            "seed": args.seed,
            "budget": args.budget,
            "operation_analysis_source": args.operation_analysis,
        },
        "candidates": candidates,
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote {len(candidates)} baseline candidates to {output_path}")


if __name__ == "__main__":
    main()
