# BIBLAW-045 — Question-aware Psalm ranking

Reference: `ef146f9df8a36859f0661f98f07a5cacf78a2a1b` (mission 044).

## Root cause
`js/biblaw.js` previously sorted all thematic results solely by editorial importance, then psalm number and record ID. The complete user question was discarded when choosing a theme in a suggestion/ambiguity panel. Therefore, the question about what happens after death displayed the same ordering as the general Mort theme.

## General correction
A small deterministic `js/question-psalm-ranker.js` ranks only **specific questions**, using normalized question notions not already represented by the canonical theme label. It searches for these notions in **the existing indexed editorial teaching and the canonically indexed verses** of each Psalm. Editorial relations and original ranking remain unchanged; ties preserve baseline ordering. No AI API, no new theological assertions, no Mort-specific rules or forced record IDs.

The selected full question is preserved through the suggestion and ambiguity choices. The production Pages allow-list now includes the new JS module. Generic `Mort` keeps the existing baseline ranking.

## Measured before/after (fixed audit 044 labels)
The audit 044 marked 5 directly responsive Psalms among the first 20. Benchmark `scripts/benchmark_045_question_psalm_ranking.js` uses only these established labels, not generated scores, as ground truth.

| Metric | Before | After |
|---|---:|---:|
| Direct A in first 5 | 2 | 3 |
| Direct A in first 10 | 2 | 3 |
| Book 03 Psalm 005 | 1 | 12 |
| Book 19 Psalm 121 | 5 | 1 |
| Book 22 Psalm 155 | 13 | 2 |
| Book 22 Psalm 159 | 14 | 13 |
| Book 21 Psalm 161 | 15 | 3 |

**Important limitation:** the reranker scores all 161 existing Mort relationships, including 141 outside the reviewed 044 top-20 sample. Those newly promoted results have **not** been human-classified as A/B/C/D; the increase in known direct answers is measurable but does not establish precision of all other results. The baseline Psalm 005 drops to rank 12; this remains an important quality concern.

## Validation
- Q120 theme-engine benchmark, Q8 existing audit, original general Mort order.
- Chromium smoke checks specific after-death question and questions on sagesse, amour, colère, duplicate Psalm IDs and general Mort order.
- Production Pages asset allow-list includes the new script.
- No canonical corpus, Gold, occurrence search or theme relations changed.
- PR is not merged or deployed.
