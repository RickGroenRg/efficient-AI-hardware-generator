# Benchmark Specification (v1)

## Goal
Establish a reproducible latency-first proof of concept for AI-guided hardware design-space exploration using a small fully connected neural network.

## Fixed Workload (v1)
- Model family: Fully connected network for inference only.
- Input shape: [1, 128]
- Hidden layers: [128, 64]
- Output shape: [1, 10]
- Batch size: 1
- Datatype: float32

## Target Platform Scope
- Board class: Xilinx PYNQ-Z2 or ZedBoard class.
- Phase 1 implementation scope: Vitis HLS only.
- Vivado and board deployment are deferred to later phases.

## Primary Objective
Minimize end-to-end inference latency under hard feasibility constraints.

## Feasibility Constraints
- Candidate must pass model-operation analysis.
- Candidate must pass HLS C synthesis.
- Candidate metrics must include latency, LUT, FF, BRAM, DSP, and estimated clock.
- Candidate must satisfy resource limits defined in configs/objective.yaml.

## Mandatory Pre-Evaluation Step
Before any baseline or AI candidate is evaluated, run software model analysis from a Python model and generate operation counts mapped to hardware units.

Required output artifact fields:
- layer_name
- operation_type
- mapped_hardware_unit
- operation_count
- notes

## Acceptance Criteria
- Baseline and AI both use identical search-space bounds.
- Baseline and AI both evaluate equal candidate counts.
- Comparison output must include best feasible latency, median feasible latency, and feasibility rate.
