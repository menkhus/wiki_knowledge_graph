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
- [x] Phase 3 — DSL/vocabulary-probe capability, written 2026-07-20:
      `vocab_probe.py` (`build_subtree_query`, `probe_vocabulary`) +
      `wikidata-kg vocab <qid>` subcommand. Given a class QID, enumerates its
      `wdt:P31/wdt:P279*` subtree (reusing `query_fragments.subtree_member_clause`,
      which was already built anticipating this) and tallies which
      properties actually occur on members — a discovery tool for growing
      `relation_map.py`'s PID table from real usage, not just a report.
      5 new mocked tests (`tests/test_vocab_probe.py`, same injectable-client
      pattern as `test_neighborhood.py`); full suite 28/28 passing. Verified
      live: `wikidata-kg vocab Q11344 --limit 40 --top 10` (Q11344 = chemical
      element, confirmed via live label fetch first) surfaced `P31`
      (instance_of, 39/40) and `P279` (subclass_of, 18/40) as expected, plus
      7 real unmapped PIDs (`P138`, `P1343`, `P61`, `P910`, `P5008`, `P1889`,
      `P1552`) — genuine candidates for `relation_map.py`, not synthetic.
      Also found and fixed along the way: the `.venv`'s editable install of
      this package was stale (`.pth`-based finder present but not actually
      registering at interpreter startup, so `wikidata-kg` as an installed
      console script failed with `ModuleNotFoundError` even though
      `python -m wikidata_connector.cli` worked fine) — fixed by
      `uv pip install --python .venv/bin/python -e ".[dev]" --reinstall-package wikidata-connector`.
      Unrelated to this phase's code; a pre-existing environment issue,
      noted here in case it recurs.

## Next (in order)

- [ ] Phase 4 — CLI unification (add the `fetch` subcommand — currently
      `fetch_neighborhood()`/`write_kg_json()` are only callable directly
      from Python, not via `wikidata-kg`), README/CLAUDE.md updates. `examples/
      ml_neighborhood_demo.md` recording the Phase 5 run is now written
      (see below) — fold into Phase 4 docs pass.

## Ideas / backlog (unscheduled, not part of the phase plan above)

- [ ] **Named-entity density check** — a lightweight, scoped-down feature
      extraction, added 2026-07-20 from a side discussion about a personal
      reading memory (Tolstoy vs. golden-age hard SF): count distinct named
      entities per 1000 words, plus frequency of kinship/title/clothing
      nouns, across a small text sample. Purpose: test whether a specific,
      falsifiable claim holds ("Tolstoy-style 19th-century social-realist
      prose is measurably denser in named people/relationships/social detail
      than Clarke/Asimov-era hard SF, which is comparatively idea-forward
      and description-thin") — not a general stylometry pipeline. Explicitly
      **not** the heavier stylometric approach (parse-tree depth, TTR,
      hapax legomena rate, readability scores) considered and correctly
      rejected in the same discussion as overkill for this project's scope
      and running into copyright limits on any real corpus. No dependency
      on the Wikidata connector; would live as a separate small script if
      pursued, not a `wikidata_connector` capability.

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
