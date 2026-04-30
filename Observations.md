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
- owner:

### Inputs
- model file:
- model class:
- input shape:
- operation analysis artifact:
- search budget:
- seed:

### Constraints
- max_lut:
- max_ff:
- max_bram:
- max_dsp:

### Outcome Summary
- feasible candidates:
- best latency:
- median feasible latency:
- feasibility rate:
- time to first feasible:

### Issues
- invalid candidates and reasons:
- unsupported operations found:
- toolchain failures:

### Actions
- corrective actions:
- next experiment changes:

