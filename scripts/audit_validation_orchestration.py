#!/usr/bin/env python3
"""Cheap static guard for Biblaw validation orchestration.

This audit deliberately does not execute FAST, TARGETED or FULL. It protects the repository-level
contracts that keep validations bounded, observable and non-redundant after the 2026-09-08 recovery
from a session that appeared to run for hours.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
workflow = (ROOT / ".github" / "workflows" / "validate-thematic-index.yml").read_text(encoding="utf-8")
pages = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
canonical = (ROOT / "scripts" / "run_canonical_thematic_pipeline.py").read_text(encoding="utf-8")
targeted = (ROOT / "scripts" / "rebuild_thematic_derivatives.py").read_text(encoding="utf-8")
checks = (ROOT / "scripts" / "check_biblaw.py").read_text(encoding="utf-8")

# Canonical GitHub job: bounded, newest-run-wins and cheap preflight before FULL.
assert "timeout-minutes: 60" in workflow, "canonical workflow needs an explicit job timeout"
assert "cancel-in-progress: true" in workflow, "stale canonical runs must be cancelled"
assert "FAST --area thematic" in workflow, "canonical workflow must run FAST preflight before FULL"
assert workflow.index("FAST --area thematic") < workflow.index("run_canonical_thematic_pipeline.py")
assert "for attempt in 1 2 3" not in workflow, "canonical workflow must not replay FULL in a retry loop"
assert "refusing an automatic FULL replay" in workflow, "push races must fail instead of replaying FULL"
assert "result is stale" in workflow, "advanced main must invalidate stale FULL output"

# FULL runner: every child process bounded and slow steps visible.
assert "BIBLAW_STAGE_TIMEOUT_SECONDS" in canonical
assert "BIBLAW_SLOW_STEP_SECONDS" in canonical
assert "timeout=STAGE_TIMEOUT_SECONDS" in canonical
assert "Slow canonical step" in canonical
assert "canonical pipeline timings" in canonical
assert "START" in canonical and "DONE" in canonical

# TARGETED runner: independently bounded and observable.
assert "BIBLAW_TARGETED_STAGE_TIMEOUT_SECONDS" in targeted
assert "timeout=STAGE_TIMEOUT_SECONDS" in targeted
assert "Slow targeted step" in targeted
assert "START" in targeted and "DONE" in targeted

# Proportional entry point: bounded commands and explicit FAST/TARGETED/FULL modes.
assert "BIBLAW_CHECK_STEP_TIMEOUT_SECONDS" in checks
assert "timeout=CHECK_STEP_TIMEOUT_SECONDS" in checks
assert 'choices=("FAST", "TARGETED", "FULL")' in checks
assert "Slow Biblaw check step" in checks
assert "FAST is non-destructive" in checks

# Lightweight deployment validation itself must also be bounded and protect this audit.
assert "timeout-minutes: 10" in pages, "Pages validation needs a small explicit timeout"
assert "audit_validation_orchestration.py" in pages, "Pages must guard validation orchestration"

print(
    "Validation orchestration OK: FAST before FULL, bounded jobs/stages, visible timings, "
    "slow-step warnings and no automatic FULL replay loop"
)
