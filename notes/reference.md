# Reference: Wiki-as-Ontology-Source and AI-Native Document Structure

**Status:** living reference document, revised twice in one session as
earlier framings turned out to be wrong on inspection (see the two
"Correction" notes in §3 and §4 — kept in place, not silently edited out,
since the corrections are themselves informative). Supersedes the narrative
form of `SESSION_2026-07-14_consolidation.md` (kept as raw session log; this
file is the processed version — summary first, links, dated context).

---

## 0. The thesis — "post-AI document publishing" (your synthesis, this session)

Stated in your own words, then unpacked: *"Wikipedia is a great knowledge
graph in itself. When that wiki points to docs that have this human
accessible method as if it's a book, this increases referentially useful
annotation in a person's work. It's reference supporting, it's AI reference
grounding too."*

This resolves the tension running through §§1–4 (Wikipedia-as-graph vs.
Wikipedia-as-wiki vs. book-structure-as-retrieval vs. RAG) into one thesis,
rather than leaving them as competing approaches:

1. **Wikipedia already is the target pattern, not just a source to mine.**
   It is simultaneously a knowledge graph (entities, cross-links, category
   structure) *and* a human-readable, book-structured document (headers,
   sections, a references/back-matter list, citations). It is not one or the
   other — the dual nature is the point, and it is existence proof that the
   pattern holds at a scale (6M+ articles, human-maintained, decades running)
   that nothing else in this document reaches.
2. **The unit that needs upgrading is the citation/reference edge itself,
   not the article in isolation.** A Wikipedia citation today points to a
   source that is frequently static, possibly stale, possibly unstructured,
   sometimes paywalled or link-rotted. "Post-AI document publishing" means
   the *cited* document — a paper, a manual, a spec, another wiki — should
   itself carry the same apparatus discussed in §4 (frontmatter, ToC/
   structure, back-matter index, document-level provenance/currency per the
   SDM discussion above), so that *following* a reference is a structured,
   groundable act, for a human and for an AI, instead of a gamble on whether
   the link still resolves to anything usable.
3. **This serves two consumers with one document design, not two designs
   for two audiences.** The same structure that lets a human reader follow a
   citation to verify or go deeper is what lets an AI cite a specific,
   current, structured passage as grounding for a claim — "reference
   supporting" and "reference grounding" are the same mechanism seen from
   the human side and the AI side. This is why the answer to §4's original
   question ("does book structure help an AI") turned out to be yes, and why
   it's not a coincidence that the same apparatus (index, provenance,
   structure) kept reappearing across the RAG-vs-wiki-vs-KG discussion, the
   page/ToC research, and the SDM currency problem — they are facets of one
   underlying design, not separate solutions competing for the same slot.

**What this makes the actual north star of `wiki_knowledge_graph`, if
pursued:** not "build a Wikidata connector" as an isolated extraction task,
but **a standard for publishing a document — any document: a manual, a
paper, a spec, a wiki article — such that its outbound and inbound
references stay live, structured, current, and equally legible to a human
reader and to an AI grounding a claim.** In that frame:
- **Wikipedia is the existence proof** that the dual graph/book structure
  works, at scale, maintained by humans.
- **The Intel SDM is the acute, lived pain case** — a document that badly
  needs this treatment and currently has none of it (stale local copies, no
  API, no currency signal).
- **Wikidata/KBpedia/OpenCyc/KNOW Ontology (§2–§3) are candidate anchors**
  for the entity layer underneath the publishing standard — a way to
  identify "this citation is about the same real-world thing as that
  citation," across documents, without each document re-inventing entity
  identity from scratch.

### Is this naive? — checked against evidence, not assumed either way

You raised, this session, that AI engineers would likely call this naive:
that engineers train on "the shreds of the data" and don't care about
post-training grounding or references, and that no one trusts AI knowledge
recall as a result. This deserved a check against actual research rather
than a reflexive defense or a reflexive concession — the claim turns out to
be **half right, in a specific and useful way**, not simply naive or simply
correct.

**Where you're right, with a citable mechanism, not just a vibe:**
"Fewer truncations improve language modeling" (ICML 2024) found that the
standard concat-and-chunk pretraining pipeline — fixed-length windows that
ignore document boundaries — **actively causes** hallucination and breaks
factual consistency, because the model ends up attending across unrelated
documents stitched together arbitrarily inside one training window. This is
not a metaphor for carelessness; it is a measured training-time defect with
a specific cause, presented at a top ML venue, with proposed fixes (keep
chunks single-document; pack by relatedness). See
[arXiv summary via Pinecone chunking overview](https://www.pinecone.io/learn/chunking-strategies/)
and the Amazon Science writeup,
["Improving LLM pretraining with better data organization."](https://www.amazon.science/blog/improving-llm-pretraining-with-better-data-organization)
So: "engineers are just using the shreds of the data" is, for a real and
still-common share of current pretraining practice, literally true — not
cynicism.

**Where "no one trusts AI knowledge recall" is right, with numbers:** a 2026
Futurum Group Decision Maker Survey (n=820) found 55.4% of organizations
name "AI agent reliability and hallucination management in production" as
their top adoption barrier. A Financial Times survey of 1,200 C-suite
executives found 71% unwilling to scale AI without "hallucination-proofing."
Current studies still measure GPT-4o/Claude-class models hallucinating on
15–20% of factual citation tasks — with invented DOIs well-formed enough,
and invented author names plausible enough, that detection requires an
actual lookup against Crossref/Semantic Scholar, not inspection by eye. See
[Futurum Group, "AI Code Review Hits a Wall"](https://futurumgroup.com/insights/ai-code-review-hits-a-wall-why-speed-without-trust-risks-engineering-chaos/)
and
["Hallucinations in generative AI: A threat to scholarly integrity"](https://www.sciencedirect.com/science/article/abs/pii/S221462962600191X).
The failure mode's danger is precisely that it's *plausible*, not obviously
wrong — which is a stronger argument for grounding than "AI is sometimes
wrong" alone would be.

**Where the field is already moving toward your thesis, not away from
it — this is the part worth knowing before assuming engineers would dismiss
this as naive:** the same body of evidence finds retrieval grounding cuts
hallucination by an estimated 75–90%, tool grounding by 65–80%, and —
directly bearing on your "reference supporting is AI reference grounding
too" — **users who can see the citation trail report measurably higher
confidence** in the answer. See
["AI Hallucination and Grounding: How Citation Actually Works in Enterprise Knowledge Systems"](https://www.clarityarc.com/insights/ai-hallucination-grounding-citation)
and
["RAG & AI Trust Statistics 2026: Beating Hallucinations."](https://www.cmarix.com/blog/rag-ai-statistics/)
Visible, checkable grounding is not a fringe position in 2026 — it is the
field's best-evidenced current mitigation, and the direction of travel
matches your instinct.

**So the precise version of "would an AI engineer call this naive":** not
the grounding thesis itself — that's now mainstream, well-evidenced
consensus, not a fringe idea, and dismissing it as naive would itself be out
of step with the 2026 literature. The genuinely open, still-contested part
is the specific *mechanism* you're proposing: that a document's own
human-authored front matter and structure (title, date, ToC, index) should
serve as the grounding substrate, rather than an embedding index computed
after the fact. An AI engineer could reasonably call *that specific choice*
unproven at scale — not because §4 shows it's wrong (PageIndex's reported
results suggest it can outperform embeddings on densely structured
documents), but because most production grounding systems in 2026 still
default to embedding-based RAG, and a structure-native alternative remains
an emerging, minority practice rather than the field's default tool. That
is a fair, narrow objection to anticipate and answer — not a reason to
abandon the thesis.

This reframing doesn't discard anything decided earlier in this document —
it explains *why* the RAG/wiki/KG distinction (§3) and the page/ToC-structure
findings (§4) both mattered: they are properties a well-published document
needs, not competing systems to choose between.

### Follow-up, same session: training-data recall, copyright, and why grounding-by-fetch sidesteps the whole fault line

You sharpened the "naive" question further: a trained model has *already*
seen some version of whatever document a person wants to reference, but
"AI recall is controversial" specifically because of **legal and
engineering-driven guardrails** designed to suppress or deny verbatim
recall-and-reuse — not because the capability doesn't exist. Your proposal:
stop relying on or invoking trained-in recall at all. Ground every answer
instead in **publicly available, currently-fetched** documents via their own
front/back matter, the same move a diligent human researcher makes — which
never enters memorization/reproduction territory to begin with, rather than
trying to argue that territory is safe.

Checked against 2026 evidence, not assumed: **this is not a generalization —
it is a specific, documented, currently-litigated fault line, and your
read of it is accurate.**

- **Verbatim memorization is real and measured, not hypothetical.**
  "Extracting books from production language models" (January 2026,
  [arXiv:2601.02671](https://arxiv.org/pdf/2601.02671)) documents ~95.8%
  verbatim recall of *Harry Potter and the Sorcerer's Stone* from
  Claude 3.7 Sonnet, and two full in-copyright books (including *1984*)
  extracted near-verbatim from a production, guardrailed, consumer-facing
  model. This is a "production, consumer-facing LLM (with guardrails)" being
  *induced* to emit this — meaning the guardrail's job is specifically to
  make that induction hard, not to make the underlying recall absent. See
  [summary discussion](https://p4sc4l.substack.com/p/can-production-consumer-facing-llms).
- **Companies deploy output filters to block this, and cite the filters'
  effectiveness in legal defense.** RLHF, system prompts, and output filters
  aimed at blocking verbatim regurgitation are documented industry practice,
  and their efficacy has been cited by AI companies directly in litigation.
  This matches your claim precisely: the guardrail is a legal-exposure
  mitigation layered on top of a real capability, not evidence the capability
  doesn't exist.
- **The legal fault line is specific and currently moving, not vague
  "controversy."** *Bartz et al. v. Anthropic* settled for **$1.5B**
  (~$3,000/work) over **storing pirated copies** — a distinct issue from
  whether training itself is fair use. Courts are trending toward treating
  training as fair use (called "highly transformative"), while 2026
  litigation is explicitly **shifting from training-data acquisition toward
  output-level reproduction claims** (Disney v. Midjourney is the marquee
  2026 case on this shift). See
  [Norton Rose Fulbright, "AI in litigation series: An update on AI copyright cases in 2026"](https://www.nortonrosefulbright.com/en/knowledge/publications/ce8eaa5f/ai-in-litigation-series-an-update-on-ai-copyright-cases-in-2026)
  and
  [Morrison Foerster, "Copyright Litigation Shifts from Training Data to AI Outputs."](https://www.mofo.com/resources/insights/260210-ai-trends-for-2026-copyright-litigation)
  So: training-time ingestion is trending toward legally settled (fair use);
  verbatim output reproduction is exactly where legal exposure is
  concentrating in 2026 — which is precisely the boundary your "no we don't
  have the ability to recall that" guardrail behavior is drawn to protect.

**Why grounding-by-fetch is the clean way out, not a workaround:** if the
system's design principle is "never answer from what might be memorized —
always look up the current, publicly available document and cite the
specific section," the memorization/reproduction question becomes
structurally irrelevant to how the system operates, rather than a risk to
manage or a controversy to litigate around. The AI is never being asked to
"recall and reuse" training-data content as its answer; it is being asked to
fetch, read, and cite a public document *at query time*, the same operation
a human researcher performs, using human knowledge-extraction conventions
(front matter, back matter, citation) that are not controversial because
they were never about model memorization in the first place. This is a
second, independent argument for the front-matter/back-matter-native design
in §4 and the thesis in this section — not just that it may retrieve better
(the PageIndex evidence), but that it avoids the copyright/memorization
fault line entirely by construction, rather than by guardrail suppression
after the fact.

**The plain-language version, your own words, and the center this whole
section has been circling:** *this is in some ways how to talk to a
human, without over-reaching into AI recall and hallucination.* Strip away
the legal argument, the hallucination statistics, and the retrieval-quality
evidence, and one behavioral rule is left, and it is the actual design
principle: **an AI operating this way talks the way a well-prepared human
does** — it says "here's what this specific, current source says, here's
where," rather than asserting from memory and hoping the memory is right.
Everything else in this document — front matter as provenance, back-matter
index as the navigation aid, fetch-at-query-time instead of trained recall,
avoiding the copyright fault line — is a mechanism *in service of* that one
rule, not a separate set of features. If this becomes something you
publish, this sentence is plausibly the thesis statement the rest of the
document exists to support.

---

## 1. Summary

Three distinct things are in play, and conflating any two of them has already
produced a wrong conclusion once in this document (corrected in §3):

1. **RAG (chunk + embed)** — does not reorganize the source; slices it and
   matches queries against the unmodified fragments.
2. **Wiki** — reorganizes the source into a new, synthesized, cross-linked
   document (what Wikipedia's editors do; what Karpathy's April 2026 pattern
   automates for a bounded working set; what your own `CLAUDE.md` files
   already do independently).
3. **Structure-guided retrieval (ToC/page/index)** — does not reorganize the
   source either, like RAG, but unlike embedding-based RAG it reuses the
   *structure a human editor already built* (front matter, table of contents,
   page boundaries, back-matter index) as the retrieval mechanism, instead of
   computing a new one via embeddings. §4 documents that this is not a
   human-only legacy method — it is a currently competitive, benchmarked
   alternative to embeddings, sometimes outperforming them.

None of these three requires the largest scale — Wikipedia already runs (2)
at massive scale, continuously, by hand. The variable that matters is
*which operation each performs on the source* (rewrite vs. leave-as-chunks
vs. navigate-via-existing-structure), not how much material is involved.
Your own `CLAUDE.md` files are a real instance of (2) — a rewritten, curated
document — independent of scale and predating Karpathy's public post.

Your question about book anatomy (frontmatter, ToC, index, glossary, back
matter) is a *third*, related question: not "which retrieval strategy" but
"what document structure, historically proven for human navigation of long
material, has an AI-native analog." Addressed directly in §4 — the honest
answer is that most print conventions map cleanly, a few don't, and the
places they don't map are informative.

---

## 2. Directory index (linked, no narrative)

| Path | What it is | Relevance |
|---|---|---|
| [`~/Documents/src/ai_plus_kg/`](/Users/mark/Documents/src/ai_plus_kg/) | Active project, has GitHub remote (`menkhus/ai_plus_kg`) | States the Wikidata/KBpedia-as-ontology-anchor thesis. Planning only. |
| [`ai_plus_kg/plan/NEXT_STEPS.md`](/Users/mark/Documents/src/ai_plus_kg/plan/NEXT_STEPS.md) | Planning doc | KBpedia, Wikidata, KNOW Ontology comparison; 4 open problems (§ below) |
| [`ai_plus_kg/research/rough_conversation_about_graphs.md`](/Users/mark/Documents/src/ai_plus_kg/research/rough_conversation_about_graphs.md) | Exploratory dialogue transcript | Wikidata/KBpedia/OpenCyc federation discussion |
| [`ai_plus_kg/research/reperf_gemini_discussion.md`](/Users/mark/Documents/src/ai_plus_kg/research/reperf_gemini_discussion.md) | Philosophical/discussion transcript | Wikipedia-as-knowledge-amplifier framing; wikiHow as procedural corpus |
| [`~/Documents/src/auto_knowledge_graph/`](/Users/mark/Documents/src/auto_knowledge_graph/) | Built, working code, ghost-indexed, local git (no remote) | The reusable **engine**: domain-independent schema + provenance + FAISS embeddings |
| [`auto_knowledge_graph/kg_schema.py`](/Users/mark/Documents/src/auto_knowledge_graph/kg_schema.py) | Code | `RelationType` enum (SUPPORTS/INVALIDATES/GROUNDS/REFERS_TO/DISCLAIMS/UNRELATED) + `Provenance` dataclass |
| [`auto_knowledge_graph/kg_embeddings.py`](/Users/mark/Documents/src/auto_knowledge_graph/kg_embeddings.py) | Code | FAISS index over KG nodes — semantic entry to *any* node, not root-to-leaf. Answers your "enter the middle of a graph" requirement, already built. |
| [`auto_knowledge_graph/docs/REFERENCES.md`](/Users/mark/Documents/src/auto_knowledge_graph/docs/REFERENCES.md) | Curated lit review, dated 2026-01-21 | Pre-existing academic grounding — see §5, not redone here |
| [`~/Documents/writing/scrivner_docs/wiki/rag_and_graph_rag_explained.md`](/Users/mark/Documents/writing/scrivner_docs/wiki/rag_and_graph_rag_explained.md) | Explainer prose, different project | You've already written the RAG/graph-RAG explanation once — read before rewriting |
| [`~/Documents/writing/scrivner_docs/wiki/hop_expansion_explained.md`](/Users/mark/Documents/writing/scrivner_docs/wiki/hop_expansion_explained.md) | Explainer prose | Multi-hop graph traversal, already explained in your own words |
| [`~/bin/ghost`](/Users/mark/bin/ghost) → `~/data/venvs/ghost/bin/ghost` | Installed CLI tool | Your working prior art for AI-native personal knowledge search |
| [`~/Documents/src/mcp_local_service_registry/scripts/ghost_mcp.py`](/Users/mark/Documents/src/mcp_local_service_registry/scripts/ghost_mcp.py) | MCP server wrapping ghost | Proof you've already made a personal knowledge substrate AI-callable, not just human-searchable |
| [`~/Documents/src/aggregated_personal_knowledge_graph.dir/`](/Users/mark/Documents/src/aggregated_personal_knowledge_graph.dir/) | Different KG, personal/device data domain | Tangential, name-collision only |
| [`~/Documents/src/systems_design_using_ai/docs/wiki/`](/Users/mark/Documents/src/systems_design_using_ai/docs/wiki/) | Docs-as-wiki naming convention | Tangential, naming precedent only |
| [`~/CLAUDE.md`](/Users/mark/CLAUDE.md), [`~/Documents/CLAUDE.md`](/Users/mark/Documents/CLAUDE.md) | Your own project instruction files | **Already a live Karpathy-pattern instance** — see §3 |

**Confirmed gap, unchanged from prior search:** no code anywhere in
`~/Documents/src` touches the Wikidata REST API, the Wikidata Query Service
(SPARQL), or a Wikipedia/Wikidata dump. The ontology-anchor thinking exists;
the extraction mechanics do not.

---

## 3. Where this idea-space sits in 2026: Karpathy's "LLM Wiki"

**Dated, sourced, not from training-data memory** — this is a live April 2026
development, checked via web search this session.

- **What happened:** On **2026-04-04**, Andrej Karpathy (former Tesla AI
  director, OpenAI co-founder) published a GitHub gist,
  [`llm-wiki.md`](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
  Not code, not a product — an "idea file" in plain prose, meant to be pasted
  into an agent (Claude Code, Codex, etc.) so the agent builds the specifics
  in collaboration with the user.
- **The core move:** stop re-reading raw sources on every query (what RAG
  does). Instead, read the sources **once**, extract and organize into a
  structured, interlinked markdown wiki (by topic/entity/relationship), then
  query *the wiki*, not the raw corpus. Karpathy's framing: "treat knowledge
  the way compilers treat source code — pre-process once, run fast forever."
- **The stated flaw in RAG this responds to:** RAG is stateless/"amnesiac" —
  every query re-searches, re-retrieves chunks, re-assembles an answer, then
  discards all of that synthesis work. Nothing compounds across queries.
- **Where this already lives in your own practice, independently:**
  Claude Code's own `CLAUDE.md` convention — a structured, human-and-agent-
  editable knowledge file consulted at the start of every session — is cited
  directly in coverage of this idea as a working instantiation of exactly this
  pattern. You already run this at three levels
  (`~/CLAUDE.md`, `~/Documents/CLAUDE.md`, and per-project `CLAUDE.md` files)
  before Karpathy's post existed. This is worth stating plainly: you built a
  version of the thing being called novel in April 2026, months earlier,
  for a different reason (session-start orientation), and didn't name it as
  a general pattern.
- **Scale claim, precisely:** proponents note this applies where the curated
  knowledge base fits under roughly a **million tokens** — modern frontier
  context windows (100K–1M+ tokens, e.g. long-context Gemini) make "the whole
  focused domain, in context, no retrieval" strictly better on recall than
  chunk-based RAG *at that size*. It is not a claim that this replaces
  retrieval for internet-scale corpora. Wikidata alone is many orders of
  magnitude past that ceiling — this pattern does not obviate a KG for
  Wikidata-scale material; it obviates RAG for a *curated working set*.
- **Nuance from early empirical work:** at least one comparative study
  (agentic curation vs. full-context retrieval on long documents) found
  overall accuracy statistically indistinguishable between the two paradigms
  in some conditions, with agentic curation showing an edge specifically on
  *direct retrieval* tasks. Treat "RAG is dead" headlines as the marketing
  layer on top of a narrower, real empirical result — the claim is scale-
  bounded and task-dependent, not universal.

**Correction — these are not the same move at different scales.** An earlier
draft of this section framed Karpathy's wiki and a KG's embedding index as
"Tier 1 (in-context) / Tier 2 (behind semantic search)" — i.e., scale as the
only distinguishing variable. That's wrong. The variable that actually
distinguishes these approaches is **whether the source gets reorganized**,
not how big it is:

| | Touches/reorganizes source structure? | Produces a new artifact? |
|---|---|---|
| **RAG (chunk + embed)** | No — chunks preserve the original as-is | No — retrieval returns unmodified fragments of the source |
| **Wiki (Karpathy pattern)** | Yes — read once, discarded, rewritten | Yes — a new, synthesized, cross-linked *document* |
| **Knowledge graph** | Yes, one step further — decomposed into typed entities/edges | Yes — a structured *graph*, no longer document-shaped at all |

Wikipedia itself is already the "wiki" layer: it is prose, continuously
reorganized by editors from raw sources into topic-structured, cross-linked
articles — this is not a metaphor, it is literally what a wiki is. Wikidata is
already the next layer down: Wikipedia's prose decomposed one step further
into entities and typed relations. RAG-with-embeddings is an orthogonal
**access method** — it can be pointed at raw sources, at Wikipedia's prose, or
at Wikidata's graph, without performing any further reorganization of any of
them.

**Implication for `wiki_knowledge_graph`:** the project is not choosing
between "build a KG" and "build a Karpathy-style wiki" as competing designs
at different scales. It is choosing **which existing reorganized layer to
consume** (raw sources / Wikipedia prose / Wikidata graph, or some
combination), and separately, **whether it needs to perform its own
additional reorganization pass** on top — e.g., resynthesizing a
security-domain or writing-craft sub-wiki from Wikidata entities, the way
`ai_plus_kg` originally proposed for the security domain. RAG/embeddings is
then the access method layered onto whichever of those artifacts you decide
to build or consume — not a competing tier, and not synonymous with either
"wiki" or "graph."

Your own `CLAUDE.md` files are a small, real instance of the *reorganization*
move (source sessions/decisions → a rewritten, curated document), which is
why they're relevant here — not because they're "small enough to fit in
context," but because they demonstrate you already do the rewrite-not-just-
retrieve move, at the scale of a project, without embeddings or a vector
index anywhere in the loop.

---

## 4. Your document-anatomy question: does book structure map to AI use?

**Correction, 2026-07-14, later same session:** the original version of this
section concluded that page numbers and linear ToC-navigation "don't
transfer" to AI use, on the theory that they exist only to compensate for a
human's inability to search. That conclusion was wrong, and asserted without
checking whether it had actually been tested. It has — recently, at scale,
in both industry benchmarks and academic KG-extraction work — and the result
contradicts the original table. The corrected findings are below; the
original table is kept further down, annotated, because the specific place
it was wrong is informative.

### What's actually documented (industry, 2024–2026)

- **Page-level chunking is empirically strong, not a fallback.** NVIDIA's
  2024 chunking-strategy benchmark found page-level chunking (one chunk per
  printed page) reached 0.648 accuracy with the *lowest variance* of any
  method tested, outperforming fixed-token-window chunking. The documented
  reason: real documents place related material on the same page by editorial
  intent (a balance sheet on one page, a figure with its caption on another) —
  page boundaries already encode a human decision about what belongs together.
  Token-window chunking cuts across that decision; page-respecting chunking
  preserves it for free. See
  [Firecrawl, "Best Chunking Strategies for RAG (and LLMs) in 2026"](https://www.firecrawl.dev/blog/best-chunking-strategies-rag)
  and [Best RAG Chunking Strategies: 4 Methods](https://inteligenai.com/best-rag-chunking-strategies/).
- **ToC-as-navigation is now a named, working retrieval architecture, not a
  legacy human-only artifact.** [PageIndex](https://github.com/VectifyAI/PageIndex)
  (Vectify AI, 2026) discards embeddings and vector search entirely and
  replaces them with reasoning over the document's own table-of-contents /
  heading hierarchy: the LLM is asked "given this document structure and this
  question, where should I look?", follows cross-references the way a human
  expert flips to the right chapter, and returns a full reasoning trace of
  which sections it visited. Reported 98.7% accuracy on professional document
  analysis (financial reports, legal filings, technical manuals, academic
  textbooks) — domains where page/section structure is dense with intent.
  See also
  [PageIndex: Vectorless RAG with Reasoning-Based Document Retrieval](https://yuv.ai/blog/pageindex),
  [RAG Without Vectors: How PageIndex Retrieves by Reasoning](https://www.marktechpost.com/2026/04/25/rag-without-vectors-how-pageindex-retrieves-by-reasoning/).
  A 3-level heading structure (title / major section / subtopic) is reported
  as the practical sweet spot between granularity and retrieval efficiency.
- **Front matter and back matter are being mined directly as KG source
  material, not bypassed by AI.** Kokash, Romanello, Suyver & Colavizza,
  ["From Books to Knowledge Graphs"](https://arxiv.org/abs/2204.10766)
  (arXiv:2204.10766, 2022, v3 2023) built a pipeline that extracts structured
  data specifically from the **bibliographies and back-matter indexes** of
  humanities/social-science books, disambiguates and normalizes it, and
  exports it as linked data — tested on Brill's Classics collection. Their
  explicit framing: back matter is unusually good raw material for automated
  KG construction precisely *because* a human editor already did half the
  structuring work — mining it is cheaper and more reliable than extracting
  the same relationships from unstructured prose.

**Corrected one-sentence version:** front matter, back matter, page
boundaries, and ToC hierarchy are not a human-only crutch obsoleted by AI
search — they are a **documented, currently competitive retrieval and
KG-construction strategy**, validated in 2024–2026 benchmarks and academic
extraction pipelines, in some regimes outperforming embeddings-based
retrieval outright, precisely because they encode a human editorial
structuring decision that would otherwise have to be re-derived
computationally at greater cost and lower reliability.

### Worked example, raised this session: the Intel SDM (~12,000 pages)

You noted having done research/applications on turning the Intel processor
Software Developer's Manual (SDM) — on the order of 12,000 pages across
volumes — into an AI-and-human-usable document *without* typical
embedding-based RAG. No dedicated project or notes for this surfaced in
`~/Documents/src` or via `ghost search` this session (`ghost search "intel
processor documentation"` returned 0 results) — recorded here as a claim from
conversation, not verified against existing files. If notes exist elsewhere
(a different machine, an unindexed directory, a conversation with another AI
tool), they're worth locating and linking here rather than re-deriving.

The SDM is close to the ideal case for the structure-guided approach
documented above, for reasons specific to this document class:

- **Its hierarchy is rigid and semantically load-bearing, not decorative.**
  Volume → chapter → section → instruction mnemonic → encoding table → bit-
  field description. Register bit layouts and instruction encodings sit
  exactly where cross-references expect them — this is closer to source code
  organization than to prose.
- **It already contains a native, human-authored graph, expressed as
  citations.** Cross-references by section number ("see Vol. 3A §4.5") are
  functionally hyperlinks that were never made clickable. A ToC/structure-
  walking approach (PageIndex's method) can traverse this directly, the same
  way an engineer flips between volumes by citation.
- **Embedding similarity plausibly underperforms here, not just ties.**
  Two instructions with near-identical prose (`MOV` vs `MOVZX`) can sit close
  in embedding space while being functionally distinct — the manual's own
  structure (separate entries, separate encoding tables, separate opcode
  rows) disambiguates them for free; an embedding index has to learn that
  disambiguation from scratch and can get it wrong.
- **The back matter (opcode maps, mnemonic index) is close to a ground-truth
  entity list already**, the same category of artifact Kokash et al. (§4
  above) found valuable to mine directly from AHSS back matter — except a
  technical spec's index is typically more rigorously maintained than a
  humanities book's, since an incorrect opcode-index entry has an immediate,
  checkable failure mode (the chip doesn't do what the manual says).
- **This is precisely the document class PageIndex reports its strongest
  results on** (financial reports, legal filings, technical manuals,
  regulatory filings, academic textbooks) — dense, cross-referenced,
  professionally structured reference material, as opposed to loosely
  organized prose where structure carries less disambiguating signal.

If you want to pursue this as a concrete pilot before deciding anything about
Wikidata/Wikipedia at large scale, the SDM is a better first test case than
Wikipedia: it's bounded (~12,000 pages, not 6M+ articles), its structure is
denser and more rigorous than typical prose, and PageIndex-style vectorless
retrieval is directly applicable with an existing open-source
implementation (`github.com/VectifyAI/PageIndex`) rather than something to
build from scratch.

**Follow-up, same session — the actual problem you lived with was different
from a retrieval-strategy question.** From working at Intel directly: the
lived complaint wasn't "chunks vs. structure vs. embeddings" — it was that
the copy of the SDM on disk was **always stale**, and what you wanted was
**current access via a simple API**, in human-readable form, not a frozen
local PDF. This reframes the SDM case: the primary unsolved problem is
**currency and distribution**, not retrieval strategy. A perfectly-indexed
PageIndex-style tree over a six-month-old local copy still gives an engineer
a wrong answer if a new stepping or errata sheet shipped since. This is
closer to a "live document API" problem (does Intel publish the SDM, or
errata/spec-update documents, in a way that's fetchable and diffable against
a local cache?) than a chunking/graph problem — and it's a different
engineering task from anything else in this document: it needs a freshness/
versioning layer (fetch-and-diff against a canonical source, flag what
changed since last sync), independent of whatever retrieval method sits on
top.

**The second point — general knowledge vs. grounding, stated precisely.**
Your framing: an LLM already carries broad general competence about x86
architecture (from training on public docs, forums, other manuals, code) —
the SDM's value isn't filling a knowledge gap the model doesn't have, it's
**grounding that general competence in the current, authoritative, specific
source** an engineer needs to trust for their exact chip. This is a
meaningfully different framing from the usual RAG pitch ("retrieval gives
the model facts it lacks") — it's closer to a **provenance/currency**
problem than a **knowledge-gap** problem: the question isn't "does the model
know what `MOVZX` does," it's "is what it just told me consistent with the
specific, current, citable section of the specific manual revision that
governs this chip." This is the same shape as the `Provenance` dataclass
already in `auto_knowledge_graph/kg_schema.py`
(`timestamp`, `validation_reasoning`, `hil_choice`) — except applied to
whole documents/revisions rather than individual KG edges: what's needed is
a **document-level provenance record** (which SDM revision, which date,
which errata applied) attached to any answer, not a bigger or better-chunked
copy of last year's PDF.

### Where the original table was right and wrong

The frontmatter/glossary/provenance mappings in the original table below
still hold. The error was narrower and specific: claiming page numbers and
linear ToC don't transfer because "an AI can already search." What the
research shows instead is that search *without* structure and structure
*without* search are both weaker than structure-guided search — PageIndex's
entire result is that reasoning over the ToC **outperforms** vector search
on certain document classes, not merely that it's an unnecessary alternative
to it. The corrected reading: page/ToC structure is a *cheaper, more
faithful index* than an embedding index has to reconstruct from scratch,
because it was already built, by a human, for exactly the purpose of
locating meaning inside a large document — which is the same purpose an
embedding index serves, arrived at by a different (and here, sometimes
better) route.

### Original table (kept for reference, page-number/ToC rows superseded above)

Your framing, restated: printed documents (books, PDFs) evolved a standard
apparatus for humans navigating large material without linear reading —
frontmatter (title, copyright, authors, year, ToC), a linear page-delimited
structure, and back matter (index, glossary/dictionary of terms, endnotes) —
with a keyword/topic index that maps *terms back to specific page locations*.
The question: does this apparatus help an AI the way it helps a human, and at
what scale?

**Answer, piece by piece — most of it transfers, with one structural
mismatch:**

| Print convention | Human function | AI-native analog | Transfers? |
|---|---|---|---|
| Title, authors, copyright, year | Provenance, citability, currency check | Frontmatter/metadata block (YAML, `Provenance` dataclass in `kg_schema.py`) | **Yes, directly.** An AI needs to know *when* and *by whom* a claim was made to weigh trust — this is exactly what `auto_knowledge_graph`'s `Provenance` fields (`timestamp`, `hil_choice`, `validation_reasoning`) already do. |
| Table of contents (linear, top-down) | Lets a human jump to a section without reading sequentially | Header hierarchy + anchors in markdown; a KG's node hierarchy | **Yes, but demoted.** A ToC is a *navigation aid for humans who read linearly by default*. An AI doesn't default to linear reading — it can search directly. The ToC's real value to an AI is as a **structure signal** (what's a subsection of what), not as a jump-table. |
| Page numbers | Physical, fixed location reference | None — pages are an artifact of print, not of information structure | **No.** This is the one convention that doesn't transfer at all. A page number encodes *where ink sits on paper*, not *what the content means or relates to*. The AI-native replacement is a **stable anchor/ID** (a heading slug, a node ID, a URI) — a reference to *content*, not *position*. This is worth naming explicitly: pagination was never really an index into meaning, it was an index into physical location that happened to correlate with meaning because books are read in order. |
| Back-of-book index (keyword → page list) | Lets a human find every place a topic is discussed without rereading | This is the closest print analog to **exactly what a KG or embedding index does** — a topic maps to every location it appears, except an AI-native index maps *semantically* (concept similarity, so a query for "poverty" also surfaces "economic hardship") rather than by *exact keyword string match*. This is the single biggest upgrade over print: print indexes are limited to whatever terms the indexer manually chose; a semantic index has no such ceiling. | **Yes, and improved.** This is the strongest match in the whole table — your instinct that the index is the load-bearing piece is correct. |
| Glossary / dictionary of special terms | Defines domain vocabulary once, referenced throughout | This maps directly to an **ontology's controlled vocabulary / entity-type definitions** — in KG terms, this *is* the schema (what a `RelationType` means, what counts as an entity type). Wikidata's own item/property definitions serve exactly this role at Wikidata scale. | **Yes, directly** — and this is precisely why Wikidata/KBpedia matter as an anchor: they're a pre-built, maintained glossary-of-everything. |
| Endnotes | Citations, tangential elaboration without breaking main flow | Edge provenance / footnote-as-edge-metadata; in a KG, this is an edge's `search_results`/`validation_reasoning` fields rather than a separate section | **Yes**, though in graph form it's attached to the specific edge rather than collected at the end. |
| Linear front-to-back reading order | Default consumption mode for a human without a search tool | **Does not exist for an AI as a default need** — an AI's "consumption mode" is query-driven, not sequential. This is the deep reason page numbers don't transfer: the entire print apparatus is scaffolding *for the absence of search*. A human without an index has to guess-and-flip; an AI never has to. | **No**, and this is the important negative result: **most of the print apparatus (ToC, page numbers, linear order) exists to compensate for the human's lack of a search function.** An AI already has that function natively. So the apparatus that *does* transfer (index, glossary, provenance) is precisely the subset that isn't just "compensating for no search" — it's the part that encodes *meaning relationships*, which is what an AI still needs help with even though it doesn't need help *locating* text. |

**The one-sentence version of this section:** book structure splits into two
kinds of scaffolding — *location-finding* aids (ToC, page numbers, linear
order), which exist only because humans can't grep, and *meaning-structuring*
aids (index, glossary, citations/provenance), which encode relationships a
search function alone doesn't give you. The first kind is irrelevant to an
AI. The second kind is exactly what a knowledge graph is — which is why your
instinct to look at book anatomy led you back to the same place as the
Wikidata/KG thread in §3: an index-of-meaning, not an index-of-location, is
the actual object worth building, and Wikidata/Wikipedia/KBpedia are existing,
maintained instances of that object at a scale no single book or project ever
achieves alone.

---

## 5. Academic and technical references

*(Consolidated from prior session + this one; deduplicated; grouped by
question they answer rather than by discovery order.)*

### On Wikidata/Wikipedia/KBpedia as ontology sources
- KBpedia — kbpedia.org — bridges Wikidata, Schema.org, OpenCyc upper
  ontology; actively maintained; the practical starting point per
  `ai_plus_kg`'s own prior assessment.
- OpenCyc v4.0 — github.com/asanchez75/opencyc — free, unmaintained since
  2017, ~239,000 concepts; structural reference only, not production-ready.
- KNOW Ontology (2024), Haltia.AI — [arXiv:2405.19877](https://arxiv.org/html/2405.19877)
  — "Knowledge Navigator Ontology for the World," explicitly LLM-era-native,
  open source, 12+ languages. The modern alternative to compare against
  KBpedia before choosing an anchor.
- Lenat & Marcus (2023), "LLMs and Cyc" — local copy:
  `ai_plus_kg/lenat_marcus_2023_llms_cyc.pdf`. Lenat's last co-authored paper.
  16 desiderata for trustworthy AI; Section 4 proposes concrete LLM↔Cyc
  synergy loops (LLM proposes edges → Cyc formalizes/checks contradictions).
- From Freebase to Wikidata: The Great Migration —
  https://research.google.com/pubs/archive/44818.pdf — historical precedent:
  Freebase (2007) → Google KG (2012) → shutdown, migrated to Wikidata (2016).
  Direct precedent for "crowdsourced wiki data as production KG backbone."

### On Karpathy's LLM Wiki / RAG-vs-long-context (2026, this session)
- Karpathy, "llm-wiki" gist (2026-04-04) —
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  — primary source, read this directly rather than secondary coverage.
- "Long Context vs. RAG for LLMs: An Evaluation and Revisits" —
  [arXiv:2501.01880](https://arxiv.org/pdf/2501.01880) — the empirical paper
  behind the debate; predates Karpathy's post, gives the actual data.
- "Grounding Long-Context Reasoning with Contextual Normalization for RAG" —
  [arXiv:2510.13191](https://arxiv.org/pdf/2510.13191)
- "Agentic Knowledge Curation Versus Full-Context Retrieval: An Empirical
  Study of Retrieval Failure Topology in Long-Context LLM Systems" —
  https://doi.org/10.3390/app16136793 — the study cited above finding
  statistically indistinguishable overall accuracy, with an edge for agentic
  curation on direct-retrieval tasks specifically.
- "SagaScale: A Realistic, Scalable, and High-Quality Long-Context Benchmark
  Built from Full-Length Novels" — [arXiv:2601.09723](https://arxiv.org/pdf/2601.09723)

### On knowledge graph construction, explainability, provenance
*(Full list already curated at
[`auto_knowledge_graph/docs/REFERENCES.md`](/Users/mark/Documents/src/auto_knowledge_graph/docs/REFERENCES.md),
dated 2026-01-21 — not reproduced here to avoid duplication. Read that file
directly; highlights:)*
- "LLM-empowered Knowledge Graph Construction: A Survey" (Oct 2025) —
  [arXiv:2510.20345](https://arxiv.org/abs/2510.20345)
- "On the Evolution of Knowledge Graphs: A Survey and Perspective" —
  [arXiv:2310.04835v3](https://arxiv.org/html/2310.04835v3)
- "A Survey on Knowledge Graph Structure and Embeddings" —
  [arXiv:2412.10092](https://arxiv.org/abs/2412.10092)
- "Knowledge-graph-based Explainable AI: A Systematic Review" —
  [PMC11316662](https://pmc.ncbi.nlm.nih.gov/articles/PMC11316662/)

---

## 6. Open decisions (unchanged from prior search — not yet made)

1. **Extraction mechanics for Wikidata**, still unevaluated against each
   other: Wikidata Query Service (SPARQL, arbitrary graph queries) vs.
   Wikidata REST API (simple per-entity fetch) vs. bulk dumps (complete, but
   needs your own index to query). This needs a short hands-on evaluation,
   not a desk decision.
2. **Two-tier architecture, per §3** — worth deciding deliberately rather
   than defaulting to "build a KG" or "build a Karpathy wiki" alone.
3. **Meta-method (Thread B from the prior document)** — still open, still
   separate from the wiki/KG system itself. Not addressed further here since
   this document is scoped to Thread A (the wiki/KG idea) plus your document-
   anatomy question, both of which sit inside Thread A.
