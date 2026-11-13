# Temporal Splits Strategy

- Splits must be time-based, never random.
- Use `train_test` as a hint but define explicit cutoffs per turbine.
- Train on earlier time range, validate on a later window, test on the
  prediction tail containing the event.
- Prevent leakage: exclude event intervals and future timestamps from
  training features.
- Evaluate generalization across turbines (leave-one-turbine-out) and across
  farms only after schema equivalence is established.
- Record cutoffs and turbine ids for reproducibility.
