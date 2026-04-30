# Model Operation Analysis Contract

## Purpose
Translate a Python software model into required hardware-unit demand before any hardware exploration.

## Mandatory Rule
This analysis is required for every experiment run. If the analysis fails or produces incomplete output, the run is invalid.

## Input
- Python file containing model definition.
- Model class name.
- Model input shape.

## Output
JSON artifact with:
- metadata:
  - model_file
  - model_class
  - input_shape
  - analyzer_version
- layers: list of per-layer records
  - layer_name
  - module_type
  - operation_type
  - mapped_hardware_unit
  - operation_count
  - notes
- totals:
  - operation_type_totals
  - hardware_unit_totals

## Mapping Expectations
Minimum supported operation classes:
- MAC class: matrix multiply and convolution-like multiply-accumulate operations.
- Add class: bias and residual additions.
- Non-linear class: activation functions (ReLU, Tanh, Sigmoid, GELU).
- Normalization class: LayerNorm and BatchNorm style ops.
- Pooling class: MaxPool and AvgPool style ops.
- Data-movement class: reshape, flatten, transpose, and memory transfer related operations.

## Unsupported Operations
Unsupported operations must be explicitly listed in output with a reason. Silent drops are not allowed.

## Quality Gates
- Deterministic results for fixed model and shape.
- No negative counts.
- Sum of per-layer counts must match totals.
