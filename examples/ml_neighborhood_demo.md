# Phase 5 demo: Wikidata neighborhood → embedding-searchable KG

Real run, 2026-07-20, `arm64` machine. This is the cross-repo proof that
`wikidata_connector`'s output actually feeds `auto_knowledge_graph`'s
embedding/query pipeline end to end, with no manual JSON editing.

## 1. Fetch the neighborhood

`wikidata-kg fetch` doesn't exist as a CLI subcommand yet — wiring it up is
Phase 4's job (see TODO.md). This step was run directly from Python instead:

```python
from pathlib import Path
from wikidata_connector.neighborhood import fetch_neighborhood
from wikidata_connector.kg_json_writer import write_kg_json

result = fetch_neighborhood("Q7259", hops=1, limit=30)
write_kg_json(result, Path("knowledge_graph/"))
```

Q7259 = Ada Lovelace. Produces `ada_lovelace_kg.json`: 31 nodes, 30 edges,
`{summary, nodes, edges}` schema, freeform relationship strings (e.g.
`place_of_birth`, not a forced enum value).

## 2. Feed it to `auto_knowledge_graph`

Copy/symlink the output into `auto_knowledge_graph/knowledge_graph/`, then:

```
cd auto_knowledge_graph
uv pip install --python .venv/bin/python sentence-transformers faiss-cpu
python3 kg_embeddings.py --build --kg-dir knowledge_graph
```

Node count went from a pre-existing baseline of **26** (an older index that
predates the Ada Lovelace file) to **57** after rebuild — the new file's 31
nodes picked up cleanly. Four unrelated 0-byte placeholder `*_kg.json`
files in the same directory are skipped with a warning; that's existing,
correct behavior, not a bug.

## 3. Query it — no LLM call, pure embedding similarity

```
python3 kg_embeddings.py "who is Ada Lovelace" --kg-dir knowledge_graph --with-edges
```

Note: `query` is a **positional** argument, not `--query` (an earlier draft
of this repo's TODO.md had that wrong).

Top result:

```
**Ada Lovelace** (entity) [score: 0.795]
  Ada Lovelace. English mathematician (1815–1852)...
  Source: ada_lovelace
```

Related edges, freeform (not enum-coerced):

```
Ada Lovelace --place_of_birth--> London
Ada Lovelace --sex_or_gender--> female
Ada Lovelace --instance_of--> human
Ada Lovelace --refers_to--> Lord Byron
...
```

## 4. Control: prove the new content is actually contributing

Move `ada_lovelace_kg.json` out, rebuild (back to 26 nodes), rerun the
identical query:

```
**hil_constraint** (concept) [score: 0.160]
  Human-in-the-Loop as a constraint where AI amplifies/filters knowledge...
  Source: ARCHITECTURE
```

Top score dropped from 0.795 to 0.160, and the result set has zero
overlap with the Ada Lovelace content — the step-3 result isn't a
coincidence. Restore the file and rebuild; final on-disk state is the
57-node index from step 2.

## Takeaway

The connector's freeform-relation, provenance-carrying JSON output is a
drop-in `*_kg.json` file for `auto_knowledge_graph` — no schema
translation, no manual editing, no enum coercion. This is the proof the
project's thesis needed: Wikidata can feed the same
extraction→embedding→query pipeline as any other source in that repo.
