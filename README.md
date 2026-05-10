# Efficient AI Hardware Generator

Repository for a reproducible proof of concept that tests whether AI-guided design-space exploration can speed up hardware generation for neural-network inference while improving key hardware metrics.

## Research Goal
Investigate whether AI can reduce hardware design time by generating better candidate designs under fixed constraints.

Primary v1 metrics:
- Inference latency
- Throughput
- Hardware resource usage (LUT, FF, BRAM, DSP)

Deferred metrics (later phase):
- Measured power
- Energy per inference

## Critical Rule
Every experiment must start with software-model operation analysis from a Python model.

This mandatory step must:
1. Analyze the model operations per layer.
2. Count operations by type.
3. Map operation demand to required hardware units, including MAC, ADD, NON_LINEAR, NORMALIZATION, POOLING, and DATA_MOVEMENT.

No baseline or AI search run is valid if this artifact is missing.

## Scope of v1
- Workload A (smoke test): simple fully connected network.
- Workload B (representative test): larger fully connected network or small Conv2d block.
- Target platform class: PYNQ-Z2 or ZedBoard class.
- Tool flow in phase 1: Vitis HLS only.
- Comparison rule: baseline and AI must evaluate equal candidate counts.

## Scope Tiers
### Tier A: HLS-only exploration
- HLS synthesis metrics are used for optimization and comparison.
- No claims about board-level power or final deployed performance.

### Tier B: implementation realism
- Vivado implementation is included for top candidates.
- Timing closure and resource feasibility are verified post-implementation.

### Tier C: board validation
- On-board runtime and power measurements are collected.
- Energy and power claims are only valid in this tier.

## Fixed Targets and Acceptance Gates
The following gates define v1 completion criteria.

1. Reproducibility gate:
- Same manifest and seed must reproduce feasibility outcomes.
- Re-run latency variation target: within 2 percent on identical toolchain.

2. Fairness gate:
- Baseline and AI must use identical search space, constraints, and evaluator.
- Candidate budgets must be equal, default 50 vs 50.

3. Feasibility gate:
- Minimum feasible-candidate rate target: 70 percent for each method.

4. Performance gate:
- Report both best feasible latency and median feasible latency.
- AI improvement target for median feasible latency: at least 10 percent versus baseline under equal budget.

5. Runtime gate:
- Total wall-time per 50-candidate run must be recorded.
- Time-to-first-feasible candidate must be reported.

## Repository Structure
- docs: project contracts and evaluation protocols.
- configs: search space, objective constraints, hardware-unit taxonomy.
- scripts: operation analysis and exploration orchestration scripts.
- experiments/manifests: reproducible run definitions.
- experiments/results: generated outputs and summaries.
- src/kernels: hardware kernel sources (next step).
- src/testbench: testbench sources (next step).

## Current Implemented Artifacts
- scripts/analyze_model_ops.py: analyzes a Python model and writes operation and hardware-unit counts.
- scripts/sample_model.py: simple FC model for analyzer validation.
- scripts/run_baseline.py: baseline candidate generation scaffold using operation-analysis artifact.
- scripts/run_ai_search.py: AI orchestration placeholder using the same artifact contract.
- docs/model_operation_analysis.md: mandatory analysis contract.

## Quick Start
1. Create a Python environment and install dependencies.
2. Run model operation analysis.
3. Generate baseline candidate set.

Example commands:

```powershell
python -m pip install -r requirements.txt
python scripts/analyze_model_ops.py --model-file scripts/sample_model.py --model-class SimpleFCNet --input-shape 1,128 --output experiments/results/sample_model_ops.json
python scripts/run_baseline.py --operation-analysis experiments/results/sample_model_ops.json --budget 50 --output experiments/results/baseline_candidates.json
```

## Execution Plan
### Phase 0: Contracts and Reproducibility
- Freeze benchmark definition.
- Freeze fairness protocol.
- Freeze model-operation analysis contract.

### Phase 0.5: Benchmark Hardening
- Freeze Workload A and Workload B definitions.
- Freeze target clock and resource limits.
- Verify that unsupported operations are explicitly reported.

### Phase 1: Deterministic Baseline Pipeline
- Add HLS evaluator and report parser.
- Connect baseline candidates to synthesis and metrics extraction.

### Phase 2: AI-Guided Search
- Add AI candidate proposal path.
- Reuse the exact same evaluator and parser as baseline.

### Phase 3: Validation and Readout
- Aggregate results, compare baseline vs AI, and report limitations.

### Phase 4: Hardware Validation
- Deploy selected candidates to board.
- Measure runtime and power on hardware.
- Report estimate-versus-measured gaps.

## Notes
- Vivado implementation and FPGA on-board measurements are intentionally deferred until HLS-only flow is stable.
- Model optimizations such as quantization and pruning are out of scope for the first proof of concept.
- Energy and power claims are out of scope until hardware validation is completed

