# wiki_knowledge_graph

## Thesis

Wikipedia is already the target pattern, not just a source to mine: it is
simultaneously a knowledge graph (entities, cross-links, categories) and a
human-readable, book-structured document (headers, sections, a references
list, citations). The dual nature is the point — proof the pattern holds at
a scale nothing else reaches, maintained by humans, for decades.

The piece that's actually broken is the citation itself, not the article. A
reference today points to something that's frequently static, stale,
unstructured, or link-rotted. **Post-AI document publishing** means the
*cited* document — a paper, a manual, a spec, another wiki page — should
carry the same apparatus a book already gives a human reader: frontmatter
(title, author, date), a table of contents, a back-matter index, and
citations. That structure is reference-supporting for a human and
reference-grounding for an AI, at the same time, through the same mechanism.

An AI built this way avoids relying on trained-in recall of a document's
content — recall that is real, measurable, and legally contested (see
`notes/reference.md` §0) — and instead fetches and cites the current,
public, specific source at query time, the same way a well-prepared human
researcher would.

**The one-sentence version:** the AI should talk the way a well-prepared
human does — citing a specific, current source it just looked up, not
asserting from memory.

## What this project is, concretely

A gap in an otherwise well-developed idea space (see `notes/reference.md`
§2 for the full directory index): nothing in this workspace yet connects to
Wikidata/Wikipedia's actual APIs, or builds the document-publishing standard
described above. `auto_knowledge_graph` already has the reusable schema,
provenance model, and embedding-based semantic index this project would
build on rather than duplicate.

## Notes

- [`notes/reference.md`](notes/reference.md) — the processed reference
  document: directory index, dated placement in the 2026 idea-space
  (Karpathy's LLM Wiki vs. RAG vs. knowledge graphs), research on
  structure-guided retrieval vs. embeddings, the Intel SDM worked example,
  and the copyright/recall analysis behind the thesis above.
- [`notes/SESSION_2026-07-14_consolidation.md`](notes/SESSION_2026-07-14_consolidation.md)
  — the raw session log this was distilled from.
