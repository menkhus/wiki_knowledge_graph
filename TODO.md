# TODO

Status as of 2026-07-20. Resumed on this machine, now confirmed `arm64`
(Apple Silicon) — the Intel/`torch` blocker no longer applies.

## Done

- [x] Phase 1 — scaffolding + rate-limit-aware client
      (`config.py`, `sparql_client.py`, `entity_fetch.py`, `cli.py ping`).
      Tested (7/7 passing, mocked HTTP via `responses`). Verified live:
      `wikidata-kg ping` succeeds against real WDQS + entity-fetch endpoints.
- [x] Phase 2 — grounding-fetch capability, core logic
      (`relation_map.py`, `query_fragments.py`, `neighborhood.py`,
      `kg_json_writer.py`). Verified live end-to-end:
      `fetch_neighborhood("Q7259", hops=1, limit=30)` (Ada Lovelace) →
      `write_kg_json(...)` produced a valid `ada_lovelace_kg.json`
      (31 nodes, 30 edges, ~12s) with correct schema and freeform
      relationship strings (e.g. `place_of_birth`).
- [x] Phase 5 — cross-repo end-to-end proof, run 2026-07-20 on `arm64`:
      1. `ada_lovelace_kg.json` (root=Q7259, 31 nodes) was already staged in
         `auto_knowledge_graph/knowledge_graph/` from the 2026-07-15 session
         — no re-fetch needed.
      2. Installed embedding deps into `auto_knowledge_graph/.venv`
         (`uv pip install --python .venv/bin/python sentence-transformers
         faiss-cpu`) — torch 2.13.0 arm64 wheel resolved cleanly, no
         platform blocker.
      3. `kg_embeddings.py --build --kg-dir knowledge_graph`: node count
         went from a baseline 26 (pre-existing index, predates the Ada
         Lovelace file) to **57** after rebuild. Four 0-byte placeholder
         `*_kg.json` files skipped with a warning as designed, not a bug.
      4. `kg_embeddings.py "who is Ada Lovelace" --kg-dir knowledge_graph
         --with-edges` (note: `query` is a **positional** arg, not `--query`
         — TODO.md's earlier draft had this wrong): top hit "Ada Lovelace"
         scored 0.795; edges rendered as freeform strings
         (`place_of_birth`, `instance_of`, `sex_or_gender`, not forced into
         the 6-value `RelationType` enum).
      5. Control: moved `ada_lovelace_kg.json` aside, rebuilt (back to 26
         nodes), reran the identical query — top score dropped to 0.160 on
         unrelated architecture-doc nodes, zero Ada Lovelace content.
         Confirms the new content is actually driving the step-4 result,
         not coincidence. File restored, index rebuilt to 57 nodes
         afterward (current on-disk state).
      Acceptance met: no manual JSON editing needed at any step.
- [x] Deferred Phase 2 mocked tests, written 2026-07-20:
      `tests/test_neighborhood.py` (5 tests — `fetch_neighborhood` exercised
      via an injectable `FakeSparqlClient` subclass + a monkeypatched
      `fetch_entities`, no HTTP mocking needed; covers single/multi-hop,
      dedup of already-visited QIDs, and early frontier exhaustion) and
      `tests/test_kg_json_writer.py` (11 tests — schema shape, label
      collision fallback, dangling-edge filtering, slugify edge cases).
      Dev deps (`responses`, `pytest`) reinstalled via
      `uv pip install --python .venv/bin/python -e ".[dev]"` — the repo's
      own `.venv` didn't have them despite `pyproject.toml` listing the
      `dev` extra. Full suite: 23/23 passing.

## Next (in order)

- [ ] Phase 3 — DSL/vocabulary-probe capability (`vocab_probe.py`,
      `wikidata-kg vocab` subcommand).
- [ ] Phase 4 — CLI unification, README/CLAUDE.md updates. `examples/
      ml_neighborhood_demo.md` recording the Phase 5 run is now written
      (see below) — fold into Phase 4 docs pass.

## Known issues / decisions made during Phase 1-2 (don't relitigate these)

- **Label fallback:** not every Wikidata entity has an `en` label (e.g. Q42
  Douglas Adams has none — only language-specific labels plus `mul`,
  Wikidata's "multilingual" value). `entity_fetch.py` falls back
  `en` → `mul`. Full multi-language support beyond this is still out of
  scope for v1.
- **maxlag:** WikibaseIntegrator's default `maxlag=5` on entity fetch caused
  real, observed compounding backoff (5s → 54s+) under live Wikidata
  replication lag. Fixed by passing `maxlag=0` in `entity_fetch.py` — this
  is a read-only connector, so there's no edit to protect a lagged replica
  from, and the edit-bot-oriented default doesn't apply.
- **Q7259 is Ada Lovelace, not Q2539** (Q2539 is "machine learning" —
  caught via live test after an earlier mistaken assumption). Any doc or
  script referencing Q2539 as Ada Lovelace is wrong and should be fixed.
- **No `torch` wheel for macOS x86_64 (Intel) on Python 3.13** — was
  confirmed blocking on the original Intel development machine (no
  `macosx_x86_64` wheel existed, only `macosx_14_0_arm64` and Linux).
  **Resolved 2026-07-20**: current machine is `arm64`; `uv pip install
  --python .venv/bin/python sentence-transformers faiss-cpu` in
  `auto_knowledge_graph` resolved torch 2.13.0 and friends with no issue.
  Leaving this entry for history — if this ever runs on an Intel machine
  again, the blocker will resurface.
- **Freeform relationship strings are intentional, not a bug** —
  `relation_map.py` maps Wikidata PIDs to real semantic labels
  (`instance_of`, `subclass_of`, ...) rather than forcing them into
  `auto_knowledge_graph`'s 6-value epistemic `RelationType` enum. Nothing
  downstream validates against that enum; forcing the mapping would discard
  real information for no benefit. Don't "fix" this back toward the enum.
- **CLI-only, no MCP server** — deliberate choice (MCP's per-server schema
  cost was judged not worth it for this connector's scope). Don't add an
  MCP wrapper without a fresh decision to do so.

## Reference

Full design rationale, phase-by-phase plan detail, and the researched
background (Wikidata extraction mechanics, `auto_knowledge_graph`'s exact
consumer interface) are in `notes/reference.md` and the session's plan
history. This file is the actionable, resumable summary; `notes/` has the
"why."
