# TODO

Status as of 2026-07-15. Paused for the summer — resume on an ARM Mac or GPU
workstation per the hardware note below.

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

## Next (in order)

- [ ] Write the deferred Phase 2 mocked tests: `tests/test_neighborhood.py`,
      `tests/test_kg_json_writer.py`. No hardware dependency — do this
      first, on any machine, before anything else below.
- [ ] On an ARM Mac (preferred) or a GPU workstation, set up
      `auto_knowledge_graph`'s embedding environment:
      ```
      cd auto_knowledge_graph
      uv venv .venv && source .venv/bin/activate
      uv pip install sentence-transformers faiss-cpu
      ```
      Expected to succeed there — confirmed blocked on Intel Mac /
      Python 3.13 only because no `torch` wheel exists for that
      platform/version combination (see Known Issues below).
- [ ] Re-run Phase 5, the cross-repo end-to-end proof:
      1. `wikidata-kg fetch Q7259 --hops 1 --limit 30 --out knowledge_graph/`
         (Q7259 = Ada Lovelace; regenerate if `ada_lovelace_kg.json` isn't
         still around from the last session).
      2. Copy/symlink the output into `auto_knowledge_graph/knowledge_graph/`.
      3. `cd auto_knowledge_graph && python3 kg_embeddings.py --build --kg-dir knowledge_graph`
         — confirm it globs the new file without error, reports an
         increased node count.
      4. `python3 kg_embeddings.py --query "who is Ada Lovelace" --kg-dir knowledge_graph --with-edges`
         — confirm the new nodes surface with plausible scores, and
         freeform (non-enum) relationship strings render correctly.
      5. Control: temporarily move the new file aside, rebuild, rerun the
         same query, confirm results differ (proves the new content is
         actually contributing, not coincidentally irrelevant).
      Acceptance: no manual JSON editing needed between step 1 and step 3.
- [ ] Phase 3 — DSL/vocabulary-probe capability (`vocab_probe.py`,
      `wikidata-kg vocab` subcommand). No hardware dependency of its own;
      do this after Phase 5 passes, per the original phase ordering.
- [ ] Phase 4 — CLI unification, README/CLAUDE.md updates, `examples/
      ml_neighborhood_demo.md` recording the real Phase 5 run.

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
- **No `torch` wheel for macOS x86_64 (Intel) on Python 3.13** — confirmed
  via `uv`'s dependency resolver, which lists `macosx_14_0_arm64` (Apple
  Silicon) and Linux as the platforms with available wheels. This blocks
  `sentence-transformers` (and therefore `auto_knowledge_graph`'s embedding
  step) entirely on the current Intel development machine, independent of
  virtual environment or Python version choice, for as long as this
  platform gap persists upstream.
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
