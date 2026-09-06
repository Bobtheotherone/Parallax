# Run record template

Do not fill evidence fields with predictions. Use `NOT_RUN` until a real tool result
exists. This provenance record is not itself enforced by the intseq interpreter.

```json
{
  "run_id": "REPLACE",
  "task_contract_sha256": "COMPUTE",
  "capsule_sha256": "COMPUTE_OR_NOT_APPLICABLE",
  "program_sha256": "COMPUTE_OR_NOT_APPLICABLE",
  "pack_file_sha256": "COMPUTE_OR_NOT_APPLICABLE",
  "runtime_source_sha256": "COMPUTE_OR_NOT_APPLICABLE",
  "environment": "RECORD_ACTUAL",
  "model_and_decoder": "RECORD_ACTUAL_OR_NO_MODEL_CALL",
  "mode_and_reason": "REPLACE",
  "stage": "INTAKE",
  "outcome": "NOT_FINISHED",
  "evidence": {
    "parsing": "NOT_RUN",
    "capsule_and_types": "NOT_RUN",
    "expansion": "NOT_RUN",
    "execution": "NOT_RUN",
    "public_tests": "NOT_RUN",
    "held_out_tests": "NOT_RUN",
    "bounded_exhaustive_tests": "NOT_RUN",
    "formal_proof": "NOT_RUN",
    "native_backend": "NOT_RUN",
    "performance": "NOT_RUN"
  },
  "commands_exit_statuses_and_logs": [],
  "attempt_costs_including_failures": [],
  "unresolved_obligations": []
}
```

## Extension for development or benchmark episodes

Keep the original fields above; use only the following additional fields that
apply. The experiment operator freezes these before scored trials.

```text
run_id:
track: development-pilot | development-comparison | representation-comparison
spec_path_and_version:
baseline_commit_and_dirty_state:
completion_commit_or_preserved_patch:
arm_and_treatment:
model_provider_version_and_decoder:
context_sources_and_identities:
task_family_and_split:
prior_exposure_and_contamination_limits:
public_oracle_identity:
final_oracle_identity_and_custodian:
final_oracle_access_controls_and_limitations:
acceptance_policy_and_reviewer:
repetitions_seed_and_order:
budget_caps_and_enforcement:
actual_usage_by_stage_including_retries_review_and_failures:
missing_usage_fields:
cold_setup_and_warm_reuse_accounting:
stopping_and_infrastructure_retry_policy:
preregistered_metrics_analysis_and_exclusions:
commands_environment_exits_and_raw_log_locations:
acceptance_criteria_results:
review_findings_dispositions_and_independence:
terminal_state_and_reason:
remaining_obligations:
```

A public development pilot is not a held-out comparison. Keep final/private
oracle data outside candidate access; record custody rather than publishing
secrets. Never populate expected output as though it were captured output.
