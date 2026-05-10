# Observations and Experiment Log

## Purpose
Track decisions, risks, and experiment outcomes in a reproducible way.

## Decision Log
### 2026-04-30
- v1 target board class: PYNQ-Z2 or ZedBoard.
- phase 1 scope: Vitis HLS only.
- primary objective: latency-first.
- fairness rule: equal number of evaluated candidates for baseline and AI.
- mandatory pre-step: analyze Python model operations and map to hardware units.

## Experiment Entry Template
### Experiment ID
- id:
- date:
- time of test:
- owner:

### Inputs
- model file: scripts/sample_model.py
- model class: SimpleFCNet
- input shape: 1,128
- operation analysis artifact: experiments/results/sample_model_ops.json
- search budget: 50
- seed: 7

### Method
- method name: baseline
- method type: deterministic baseline pipeline
- evaluator flow: phase 1 Vitis HLS only (Vivado and FPGA deferred)
- candidate generation policy: fixed-budget candidate evaluation (equal candidate count for baseline and AI)

### Optimization Strategy and Configuration
- primary objective: latency-first
- optimization strategy: explore hardware candidates under fixed constraints
- search space config:
- objective config:
- hardware-unit taxonomy config:
- key design parameters:
- HLS directives or pragma configuration:

### Hardware and Toolchain
- hardware testing performed: no (phase 1 scope)
- hardware platform: Vitis HLS analysis flow
- FPGA board or target device: PYNQ-Z2 or ZedBoard class
- host machine:
- Vitis HLS version:
- Vivado version:
- Python version:
- dependency versions:

### Constraints
- max_lut:
- max_ff:
- max_bram:
- max_dsp:

### Runtime and Execution
- total run-time:
- average time per candidate:
- synthesis time per candidate:
- number of candidates evaluated:
- number of candidates rejected before evaluation:

### Outcome Summary
- feasible candidates:
- best latency:
- median feasible latency:
- feasibility rate:
- time to first feasible:
- best candidate id:
- output artifacts:

### Issues
- invalid candidates and reasons:
- unsupported operations found:
- toolchain failures:

### Reproducibility Notes
- exact commands used:
	- python -m pip install -r requirements.txt
	- python scripts/analyze_model_ops.py --model-file scripts/sample_model.py --model-class SimpleFCNet --input-shape 1,128 --output experiments/results/sample_model_ops.json
	- python scripts/run_baseline.py --operation-analysis experiments/results/sample_model_ops.json --budget 50 --output experiments/results/baseline_candidates.json
- manifest file:
- result files:
- environment variables or paths:
- code revision or commit:
- assumptions and caveats:
- additional notes:

### Actions
- corrective actions:
- next experiment changes:

