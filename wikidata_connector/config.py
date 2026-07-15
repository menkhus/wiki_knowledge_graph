"""Endpoints, rate-limit budgets, and other shared constants.

Rate-limit numbers are per Wikidata's own documentation as of 2026:
- WDQS throttle: 60s cumulative query-time/min (burst 120s), 30 errors/min
  (burst 60). See https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/query_limits
- Platform-wide Wikimedia API rate limit: unidentified clients (no/bare
  User-Agent) get 10 req/min; clients with a compliant User-Agent get
  200 req/min. See https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits
  A compliant User-Agent is therefore a correctness requirement, not
  politeness — it is the difference between the 10 and 200 req/min tiers.
"""

WDQS_ENDPOINT = "https://query.wikidata.org/sparql"
LDI_ENDPOINT_TEMPLATE = "https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"

# Replace the contact URL/email before any sustained real-world use — a
# generic UA still gets the 200 req/min tier, but a project-specific one is
# better Wikimedia-community etiquette and is required if this project is
# ever run at higher volume.
USER_AGENT = (
    "wiki_knowledge_graph/0.1 "
    "(https://github.com/menkhus/wiki_knowledge_graph; mark.menkhus@gmail.com) "
    "python-requests"
)

# Safety margins under WDQS's documented 60s/min and 30 errors/min budgets.
SPARQL_QUERY_TIME_BUDGET_S = 55.0
SPARQL_THROTTLE_WINDOW_S = 60.0
MAX_ERRORS_PER_MIN = 25

ENTITY_BATCH_SIZE = 50  # matches wbgetentities' own batching limit

REQUEST_TIMEOUT_S = 30
MAX_RETRIES = 3
RETRY_BACKOFF_BASE_S = 2.0  # 2s, 4s, 8s

MAX_HOPS = 2  # CLI-enforced ceiling; deeper hops risk exponential QID growth
              # against a shared, rate-limited public service.

# QLever (https://qlever.dev/wikidata) is a fast, community-run public
# SPARQL mirror of Wikidata — a documented fallback if WDQS throttling or
# its 2026 degraded performance becomes a real blocker. Not wired up in v1;
# noted here so a future session doesn't have to re-research it.
QLEVER_ENDPOINT = "https://qlever.cs.uni-freiburg.de/api/wikidata"
