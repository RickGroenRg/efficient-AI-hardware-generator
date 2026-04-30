import argparse
import json
from pathlib import Path


# Placeholder orchestrator.
# In next implementation steps this will call an AI policy to propose candidates,
# then pass them to the shared evaluator used by baseline.

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="AI-guided candidate orchestration placeholder")
    parser.add_argument("--operation-analysis", required=True, help="Path to model operation analysis JSON")
    parser.add_argument("--budget", type=int, default=50, help="Number of AI candidates")
    parser.add_argument("--output", required=True, help="Output JSON file")
    args = parser.parse_args()

    analysis = load_json(Path(args.operation_analysis))
    if not analysis.get("layers"):
        raise ValueError("Operation analysis file is empty or invalid")

    output = {
        "metadata": {
            "budget": args.budget,
            "operation_analysis_source": args.operation_analysis,
            "status": "placeholder",
        },
        "candidates": [],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print("AI search orchestrator placeholder created output file")


if __name__ == "__main__":
    main()
