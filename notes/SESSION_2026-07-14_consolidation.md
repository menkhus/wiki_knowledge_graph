# Session Consolidation — wiki_knowledge_graph origin session

**Date:** 2026-07-14
**Location:** `~/Documents/src/wiki_knowledge_graph/` (empty at session start)
**Purpose of this document:** You asked to stop before deciding anything and get
a complete record of (1) the prompts that drove this session, (2) everything
searched and found, (3) which directories inform this project and why, and
(4) technical and academic references — because this may become a project you
publish, and you want to think about it deliberately rather than react to a plan.

This is a record, not a plan. No recommendation is finalized here.

---

## 1. The prompts, verbatim

**Prompt 1:**
> can you look for work I have done realted to wikis in ../../writing ~/writing ~/src ../src

**Prompt 2 (the thesis statement — your own words, preserved exactly):**
> So, not only do I think wikipedia itself is a powerful ontology source in
> principle, and I feel that a KG can be a tool for long term structurally
> sound AI accessibility. Now, I don't have knowledge of how to extract, use
> and create the wiki. I know that APIs are important, semantic access like
> RAG and similarly aligned tools. I feel like knowledge structure needs to be
> easy for an AI to use into the middle of a knowledge graph.

**Prompt 3 (this request):**
> So much stuff scrolled by, I need to catch up with what you found, and
> concluded. I am picking this up because I feel that I want to have a
> comprehensive AI adjacent method that I build into every project I make.
> The `find ~/writing -name ....` and so on.
>
> Create a plan that includes these items. More importantly, document the
> prompts for this generative work session as well as all the knowledge you
> have searched for, which directories inform this project and all the
> knowledge that scrolled by on my screen. I want to stop, and think about
> this. Please put technical AND academic references too. This is a
> significant work I mean to publish if I cannot find an effective general
> method for this. git, gh, md, my own ghost tools, complicated wikis. The
> idea here is that Post AI knowledge work needs to have accessibility via AI
> so I can be informed and reuse that knowledge. This is my thinking about
> long term AI as programming and writing tool.

**Reading of the ask:** two things are entangled here and worth separating
before acting on either:

1. **The wiki/KG idea itself** — Wikipedia/Wikidata as an ontology source,
   with a knowledge structure an AI can enter mid-graph (not just root-to-leaf),
   accessed via API + semantic/RAG methods.
2. **A meta-method** — "a comprehensive AI-adjacent method that I build into
   every project I make." This is bigger than the wiki idea: it's about having
   a repeatable, general practice (search-first orientation across `git`, `gh`,
   markdown docs, your `ghost` tooling, and prior "complicated wikis") that you
   apply at the *start* of any project, of which this consolidation-search you
   just watched happen is itself the first instance.

Both are preserved below, separately, because they may end up as two different
publishable artifacts: a method paper (the meta-method) and a system paper/tool
(the wiki KG). Conflating them risks neither getting done well.

---

## 2. What was searched, and what turned up

### Search 1: literal "wiki" in the four requested directories

```
find ~/writing -iname "*wiki*"                    → nothing (dir is empty of wiki content)
find ~/src -maxdepth 3 -iname "*wiki*"             → nothing (true $HOME/src is nearly empty —
                                                       most work actually lives under ~/Documents/src)
find ~/Documents/writing -iname "*wiki*"           → scrivner_docs/wiki/ (12 files)
find ~/Documents/src -iname "*wiki*"               → wiki_knowledge_graph (this, empty),
                                                       systems_design_using_ai/docs/wiki/ (14 files),
                                                       two wikilinks.pyi files bundled inside a
                                                       third-party jedi/typeshed vendor tree
                                                       (writing-surface/dist/... — not your work,
                                                       ignore)
```

**Key correction of a home-directory assumption:** `~/writing` and `~/src`
(literal, under `/Users/mark/`) are nearly empty. The real project tree lives
under `~/Documents/src/` and `~/Documents/writing/` — this matches
`~/Documents/CLAUDE.md`'s description of `~/Documents/` as "the top of the
working tree." Any future `find` for this kind of survey should target
`~/Documents/src` and `~/Documents/writing`, not the bare home-directory paths.

**What the two literal "wiki" folders actually are:** both are GitHub-wiki-style
*documentation* folders (getting-started guides, architecture explainers) for
other tools — not wiki *processing* code, not Wikipedia/Wikidata integration.
- `scrivner_docs/wiki/` — docs for a Scrivener-adjacent writing tool. Notably
  contains `rag_and_graph_rag_explained.md`, `graph-thinking.md`,
  `hop_expansion_explained.md` — i.e., you've already written explainer docs
  about graph-RAG and multi-hop graph traversal in a *different* project. Worth
  reading before writing anything new on the same topic — you may have already
  worked out the explanation you'd otherwise redo.
- `systems_design_using_ai/docs/wiki/` — docs for AI-assisted systems design
  process (TDD, formal methods, orchestration). Not wiki-content-related, just
  uses "wiki" as the docs-folder name (standard GitHub convention).

### Search 2: broader grep for "wiki" content, real knowledge-graph hits

```
grep -rli "wiki" ~/Documents/src --include="*.md" --include="*.py"
```

Returned ~50+ files. Triaged for actual relevance (excluding CVE/CPE files
where "wiki" was a coincidental substring match, e.g. `cpe_uris.txt`):

- **`ai_plus_kg/`** — most relevant hit. Active project (has a GitHub remote,
  `github.com/menkhus/ai_plus_kg`). Contains a whole planning track titled
  "Knowledge Graph / Lenat" that explicitly proposes **Wikidata** and
  **KBpedia** as federation anchors for a security-domain KG. Not yet built —
  planning documents only.
- **`auto_knowledge_graph/`** — a *different*, more mature KG engine. No direct
  Wikidata/wiki mentions, but has working code for the generic KG substrate:
  schema, provenance, embeddings. Directly relevant as reusable infrastructure
  (see §3).
- **`aggregated_personal_knowledge_graph.dir/`** — a third KG-named project,
  but scoped to personal/device data (PIM, sensors, browser history) — matched
  the search only because of the "knowledge graph" name; not wiki-related.
  Noted for completeness, not pursued further.
- **`projects/ai_shell_and_agents_with_roles/.../knowledge_graph_crawler.py`**
  — has two literal `"wiki"` string references (lines 430, 633), likely a
  source-type tag in a crawler config, not inspected in depth this session.
  Worth a closer look if the crawler already has generic web/wiki fetch logic.

### Search 3: targeted grep for `mediawiki|wikipedia dump|wikidata|wiki dump|wiktionary`

Real hits (excluding CVE files, response logs, and other coincidental matches):

- `ai_plus_kg/plan/NEXT_STEPS.md` — the core planning document (full relevant
  section quoted in §4 below)
- `ai_plus_kg/research/rough_conversation_about_graphs.md` — a long exploratory
  dialogue (with Gemini, by the file's tone) about KBpedia/Wikidata/OpenCyc as
  federation candidates
- `ai_plus_kg/research/reperf_gemini_discussion.md` — philosophical material:
  Wikipedia as a "knowledge amplifier," wikiHow as a procedural-knowledge
  training corpus (cites Allen AI's research use of wikiHow)
- `aggregated_personal_knowledge_graph.dir/GARAGE-AI-TRANSCRIPT.md` and
  `book/ch04_the_morning_briefing.md`, `book/ch07_when_the_lights_came_on.md`
  — narrative/book-draft material, not technical; not reviewed in depth

**No code anywhere touches the actual Wikidata API, SPARQL endpoint, Wikipedia
API, or a Wikipedia/Wikidata dump.** This is a genuine, confirmed gap — the
thinking exists, the extraction mechanics do not.

### Search 4: `auto_knowledge_graph` internals (the reusable engine)

Read `kg_schema.py` and `kg_embeddings.py` directly (not just grepped):

- `kg_schema.py` defines a **domain-independent** node/edge schema:
  - `RelationType` enum: `SUPPORTS`, `INVALIDATES`, `GROUNDS`, `REFERS_TO`,
    `DISCLAIMS`, `UNRELATED` — epistemic relation types, not just generic
    "related-to" edges
  - `Provenance` dataclass: every edge carries `timestamp`, `summary`,
    `search_results`, `hil_choice`, `hil_rejected`, `validation_reasoning`,
    `command` — i.e., full audit trail of *why* an edge exists and what a
    human confirmed vs. rejected
- `kg_embeddings.py` builds a **FAISS vector index over KG nodes** so queries
  are answered by embedding similarity *without* an LLM call at query time.
  Explicit three-stage architecture stated in its docstring:
  ```
  EXTRACTION (one-time): Documents → LLM → Nodes/Edges
  EMBEDDING (one-time):  Nodes → Embedding model → FAISS index
  QUERY (instant):       Query → Embed → FAISS search → Results
  ```
  This is the direct, already-working answer to "knowledge structure needs to
  be easy for an AI to use into the middle of a knowledge graph" — semantic
  entry into the graph at any node, not root-to-leaf traversal. It has never
  been pointed at Wikidata/Wikipedia content.
- `docs/REFERENCES.md` in this project already contains a curated academic
  literature review (full contents reproduced in §5 below) — this predates
  this session and should not be redone from scratch.

### Search 5: your own tooling context (`ghost`, `~/bin`)

- `ghost` is a real, installed tool: `~/bin/ghost` symlinks to
  `~/data/venvs/ghost/bin/ghost`, a dedicated virtualenv — this is your
  archival/search tool referenced in `~/Documents/CLAUDE.md`
  ("`ghost search "query"` — search across all ghost-indexed projects").
  `auto_knowledge_graph` itself is ghost-indexed (`.ghost-index.joblib`,
  `.ghost.sqlite` present in its directory listing) — meaning it's already
  inside your searchable-knowledge substrate, separate from the KG-of-KGs
  question itself.
- `ghost_mcp.py` — symlinked from
  `~/Documents/src/mcp_local_service_registry/scripts/ghost_mcp.py` — ghost is
  exposed as an MCP server, i.e. already AI-accessible via tool-call, not just
  CLI. This matters directly for the "AI accessibility" thesis: you have a
  working example, in `ghost`, of a personal knowledge substrate made
  AI-native through MCP. Worth treating as the working prototype of the meta-
  method, not just prior art.
- `project_status` (mentioned in `~/Documents/CLAUDE.md` as "the right first
  move") was **not found** on PATH in this session — either aliased/functioned
  in `.zshrc` (not sourced in the tool sandbox) or the doc is stale. Flag this
  as something to verify next real session, since the CLAUDE.md instructs
  using it as the first move and it didn't resolve.
- Git remotes: only `ai_plus_kg` has a GitHub remote
  (`github.com/menkhus/ai_plus_kg`). `auto_knowledge_graph` and
  `aggregated_personal_knowledge_graph.dir` are local git repos with no
  `origin` configured — relevant if "git, gh" in your meta-method means every
  project should have a remote and issue tracker from the start, that's not
  currently uniform practice across these three.

---

## 3. Which directories inform this project, and how

| Directory | Role | Status |
|---|---|---|
| `~/Documents/src/ai_plus_kg/` | The **why** — states the thesis that Wikidata/KBpedia should anchor a KG's upper ontology; security-domain framing | Planning only, has GitHub remote, actively worked (TODO.md dated through 2026-07) |
| `~/Documents/src/auto_knowledge_graph/` | The **engine** — domain-independent schema, provenance model, FAISS mid-graph semantic entry, already working code | Built, ghost-indexed, local git only (no remote) |
| `~/Documents/writing/scrivner_docs/wiki/` | Prior **explainer writing** on graph-RAG and multi-hop traversal — same concepts, different project, may be directly reusable prose | Complete, for a different tool |
| `~/bin/ghost` + `mcp_local_service_registry` | A working **prototype of AI-native personal knowledge access** — CLI + MCP server over ghost-indexed projects | Installed, in daily use |
| `~/Documents/src/aggregated_personal_knowledge_graph.dir/` | A third KG effort, different domain (personal/device data) | Tangential — noted, not load-bearing |
| `~/Documents/src/systems_design_using_ai/docs/wiki/` | Docs-as-wiki convention example (not content) | Tangential — naming-convention precedent only |

**The gap `wiki_knowledge_graph` (this project) would fill, if pursued:** the
extraction/connector layer between actual Wikidata/Wikipedia sources and
`auto_knowledge_graph`'s existing schema+embedding engine. Nobody has written
this yet. It is a connector, not a new engine — the engine already exists and
already solves the "AI enters mid-graph" requirement via FAISS semantic search.

---

## 4. The `ai_plus_kg` planning material, in full (already written, not re-derived)

From `ai_plus_kg/plan/NEXT_STEPS.md`:

> **KBpedia** — Modern reconstruction incorporating portions of OpenCyc.
> Replaced OpenCyc's upper ontology with a cleaner structure. Bridges
> Wikidata, Schema.org, and other public knowledge sources. Actively
> maintained. More practical starting point than raw OpenCyc for new domain
> construction. kbpedia.org
>
> **Wikidata** — Crowdsourced, massive, actively maintained. Less rigorous
> than Cyc but orders of magnitude larger. Useful for: product → vendor → CPE
> relationships; entity disambiguation. The scale makes it the practical
> anchor for the federation layer.
>
> **KNOW Ontology (2024)** — "Knowledge Navigator Ontology for the World" —
> Haltia.AI. Open source; designed to augment LLMs rather than replace them.
> 12+ language libraries. arxiv.org/html/2405.19877. Modern take on Lenat's
> vision, built for the hybrid neuro-symbolic era.

Open problems this same document already identified (still open):

1. **The interrogative graph interface** — not a dashboard, a dialogue. What
   questions surface implicit edges a person hasn't named?
2. **Context as first-class citizen** — Lenat's Microtheories: the same node
   needs different meaning under different context/conditions of
   applicability, not just a flat edge.
3. **The ontological root** — a shared upper ontology for domain federation is
   still an open problem industry-wide; KBpedia + Wikidata + OpenCyc is the
   nearest existing approximation.
4. **Compression fidelity** — when AI session context compacts, structure
   survives but *significance* does not; a KG (or the interrogative graph) is
   proposed as the fix, because the human's weighting of what matters lives in
   the graph, not the transcript.

---

## 5. Academic and technical references

### Already curated in this workspace (`auto_knowledge_graph/docs/REFERENCES.md`, 2026-01-21)

**Foundational / historical:**
- Freebase (2007) → Google acquisition (2010) → Google Knowledge Graph (2012)
  → Freebase shutdown, migration to Wikidata (2016). [From Freebase to
  Wikidata: The Great Migration](https://research.google.com/pubs/archive/44818.pdf)
  — directly relevant: this is the historical precedent for exactly what
  you're proposing (a crowdsourced wiki-derived graph as the practical
  backbone of a knowledge system).
- [Knowledge Graph (Google) — Wikipedia](https://en.wikipedia.org/wiki/Knowledge_Graph_(Google))
- [Freebase (database) — Wikipedia](https://en.wikipedia.org/wiki/Freebase_(database))

**Surveys (most current first):**
- LLM-empowered Knowledge Graph Construction: A Survey (Oct 2025).
  [arXiv:2510.20345](https://arxiv.org/abs/2510.20345)
- On the Evolution of Knowledge Graphs: A Survey and Perspective (May 2025).
  [arXiv:2310.04835v3](https://arxiv.org/html/2310.04835v3)
- A Survey on Knowledge Graph Structure and Embeddings (2024).
  [arXiv:2412.10092](https://arxiv.org/abs/2412.10092)
- Knowledge Graphs as Tools for Explainable Machine Learning: A Survey (2021).
  [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0004370221001788)
- Knowledge-graph-based Explainable AI: A Systematic Review (2024).
  [PMC11316662](https://pmc.ncbi.nlm.nih.gov/articles/PMC11316662/)
- OK Google, What Is Your Ontology? (2018).
  [arXiv:1805.03885](https://arxiv.org/abs/1805.03885)

**Construction methodology:**
- Neo4j: Text to Knowledge Graph Information Extraction Pipeline.
  https://neo4j.com/blog/genai/text-to-knowledge-graph-information-extraction-pipeline/
- NLP4KGC: NLP for Knowledge Graph Creation — IBM Research.
  https://research.ibm.com/publications/nlp4kgc-natural-language-processing-for-knowledge-graph-creation
- Knowledge Graph Construction: Extraction, Learning, and Evaluation (2025).
  https://www.mdpi.com/2076-3417/15/7/3727
- Information Extraction Pipelines for Knowledge Graphs (2022).
  https://link.springer.com/article/10.1007/s10115-022-01826-x

**Explainability / trust / provenance (the "WHY layer"):**
- KG4XAI: Knowledge Graphs for Explainable AI — taxonomy and methodology.
  https://medium.com/@adnanmasood/kg4xai-knowledge-graphs-for-explainable-artificial-intelligence-taxonomies-methodologies-and-190f098c3a77
- The role of knowledge graphs in building agentic AI systems.
  https://zbrain.ai/knowledge-graphs-for-agentic-ai/
- From "Trust Me" to "Prove It": Why Enterprises Need Graph RAG.
  https://community.netapp.com/t5/Tech-ONTAP-Blogs/From-quot-Trust-Me-quot-to-quot-Prove-It-quot-Why-Enterprises-Need-Graph-RAG/ba-p/462813
- Unlocking Trustworthy AI with Ontologies and Knowledge Graphs.
  https://cyberhillpartners.com/enterprise-ai-ontologies-knowledge-graphs/

**Enterprise case studies / ROI:**
- Stardog Enterprise KG ROI study (320% ROI, $9.86M benefit over 3 years).
  https://www.stardog.com/blog/understand-the-roi-of-an-enterprise-knowledge-graph-platform/
- Gartner: graph technologies in 80% of data/analytics innovations by 2025
  (up from 10% in 2021), via Enterprise Knowledge.
  https://enterprise-knowledge.com/top-graph-use-cases-and-enterprise-applications-with-real-world-examples/
- Case studies: Roche (clinical trial integration), Walmart (product data
  model/GDM), BBC (Linked Data Platform), NASA (OntoMat). Via
  https://www.poolparty.biz/case-studies-for-enterprise-knowledge-graphs and
  https://www.ontotext.com/knowledgehub/case-studies/industry-use-cases-with-knowledge-graphs/

### Surfaced this session, not previously in the workspace

- **Lenat & Marcus (2023)** — "LLMs and Cyc," Lenat's last co-authored paper
  before his death in August 2023, with Gary Marcus (NYU). PDF already present
  locally at `ai_plus_kg/lenat_marcus_2023_llms_cyc.pdf`. States 16 desiderata
  for trustworthy AI; Section 3 covers how Cyc addresses each; Section 4
  proposes concrete LLM↔Cyc synergies (LLM generates candidate edges → Cyc
  formalizes/checks contradictions → asks follow-up questions). This is the
  clearest existing articulation of "knowledge structure an AI can use," worth
  reading in full before designing a new schema.
- **KBpedia** (kbpedia.org) — actively maintained, positions itself explicitly
  as the bridge between Wikidata, Schema.org, and OpenCyc's upper ontology.
  The most direct existing answer to "how do I use Wikipedia/Wikidata as an
  ontology source without building the upper ontology myself."
- **OpenCyc v4.0** (github.com/asanchez75/opencyc) — free, unmaintained since
  2017, ~239,000 concepts. Useful for learning ontological structure, not for
  production use per `ai_plus_kg`'s own assessment.
- **KNOW Ontology (2024)**, Haltia.AI — "Knowledge Navigator Ontology for the
  World," open source, explicitly designed to augment (not replace) LLMs,
  12+ language libraries. [arXiv:2405.19877](https://arxiv.org/html/2405.19877)
  — the most modern, LLM-era-native alternative to Cyc/KBpedia; worth
  comparing directly against KBpedia before choosing an anchor.
- **wikiHow as procedural-knowledge training data** — cited in
  `ai_plus_kg/research/reperf_gemini_discussion.md` as Allen AI research
  treating wikiHow as a "skill registry at human scale." Relevant if the
  eventual system cares about procedural/how-to knowledge, not just factual
  entity graphs — a different extraction target than Wikidata's structured
  triples.
- **Wikidata Query Service (SPARQL endpoint)** and the **Wikidata REST API**
  — not yet evaluated against each other in any local document. This is the
  actual technical decision point for extraction mechanics that nobody here
  has made yet: SPARQL (powerful, arbitrary graph queries, steeper syntax) vs.
  REST API (simpler per-entity fetch, no arbitrary query) vs. bulk dumps
  (complete, but requires your own index/database to make queryable). This
  needs its own evaluation pass, not a snap decision.

---

## 6. The two threads, kept separate for your thinking time

**Thread A — the wiki/KG system itself.** Wikidata as an ontology anchor
(per `ai_plus_kg`'s own prior analysis), fed through a connector you'd build,
into `auto_knowledge_graph`'s existing schema + FAISS mid-graph semantic
access. The novel contribution, if there is one for publication, is likely
in the connector design plus whatever answers "context as first-class
citizen" (open problem #2 above) for a *general-purpose*, not
security-domain-specific, KG.

**Thread B — the meta-method.** "A comprehensive AI-adjacent method I build
into every project I make." What this session's own search process
demonstrated in miniature: survey existing prior art (`find`/`grep` across
`git`-tracked project directories, `ghost search` as the indexed equivalent),
read the docs/`CLAUDE.md` chain, check for existing schema/engine code before
proposing new code, pull citations already curated in-repo before searching
externally. If you want this to be the reusable method, the candidate steps
are roughly: (1) orient via `~/Documents/CLAUDE.md`'s prescribed
`project_status`/`ghost search` (note: `project_status` didn't resolve this
session — worth fixing first), (2) grep/find for prior art across
`~/Documents/src` and `~/Documents/writing` before writing new code or docs,
(3) check `git`/`gh` remote status and issue tracker existence, (4) check for
an existing `docs/REFERENCES.md`-style academic grounding file before doing a
fresh literature search, (5) write a consolidation doc like this one before
committing to a plan on anything you intend to publish.

Nothing in this document commits you to either thread. It's the record you
asked for, to think from.
