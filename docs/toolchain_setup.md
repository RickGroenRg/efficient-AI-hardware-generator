# Toolchain Setup (Phase 1)

## Host Environment
- OS: Windows
- Python: 3.10 or newer
- Vitis HLS: pinned version to be finalized before formal runs

## Python Dependencies
- torch
- pyyaml

## Setup Steps
1. Create virtual environment.
2. Install Python dependencies.
3. Validate model-operation analyzer runs on sample model.
4. Validate configuration files load correctly.

## Preflight Checks
- Python import checks for torch and yaml.
- Paths for scripts, configs, and experiments folders exist.
- Output write permissions for experiments/results.

## Reproducibility Requirements
- Record Python version and package versions in each experiment manifest.
- Record Vitis HLS version used for synthesis.
- Keep random seeds fixed in baseline and AI search runs.
