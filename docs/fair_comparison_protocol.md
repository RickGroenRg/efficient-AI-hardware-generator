# Fair Comparison Protocol (Baseline vs AI)

## Comparison Rule
Baseline search and AI-guided search must be compared under equal evaluation opportunity.

## Fixed Budget
- Candidate budget: 50 candidates for baseline and 50 candidates for AI.
- Both methods must use the same evaluator backend.

## Shared Inputs
Both methods must use:
- Same benchmark specification.
- Same objective and feasibility constraints.
- Same operation-analysis artifact from the Python model.
- Same search-space bounds.

## Disallowed Practices
- No method-specific relaxed constraints.
- No separate metric parser for AI.
- No manual pruning that is not also applied to both methods.

## Required Reporting
For each method report:
- Best feasible latency.
- Median feasible latency.
- Feasibility rate.
- Time to first feasible candidate.
- Number of invalid proposals rejected before synthesis.
