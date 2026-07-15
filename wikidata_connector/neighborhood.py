"""Capability 1: bounded entity neighborhood -> structured result.

Implements the two-step pattern recommended by Wikidata's own
documentation: (1) a narrow, QID-anchored SPARQL query enumerating a
bounded set of related QIDs (never a broad CONSTRUCT or unbounded pull),
then (2) a separate batch entity-data fetch for the QIDs found. Kept as two
steps because WDQS is optimized for narrow, well-characterized queries, not
for extracting full statement data at scale — that's what the entity-fetch
endpoints are for.
"""

from dataclasses import dataclass, field

from wikidata_connector.entity_fetch import fetch_entities
from wikidata_connector.query_fragments import strip_entity_uri
from wikidata_connector.sparql_client import SparqlClient


@dataclass
class NeighborhoodResult:
    root_qid: str
    hops: int
    limit: int
    sparql_query: str
    entities: dict[str, dict]  # qid -> entity data (from entity_fetch)
    edges: list[tuple[str, str, str]] = field(default_factory=list)  # (from_qid, to_qid, pid)


def build_neighbor_query(qid: str, limit: int = 200) -> str:
    """A scoped SELECT enumerating QIDs directly connected to `qid` via any
    property, plus which property connects them. Hop depth beyond 1 is
    handled by calling this repeatedly over the discovered neighbor set
    (see fetch_neighborhood), not by a deeper SPARQL property-path pattern —
    keeps each individual query narrow and bounded, per WDQS's documented
    strength.
    """
    return f"""
SELECT ?neighbor ?prop WHERE {{
  wd:{qid} ?p ?neighbor .
  ?prop wikibase:directClaim ?p .
  FILTER(isIRI(?neighbor))
  FILTER(STRSTARTS(STR(?neighbor), "http://www.wikidata.org/entity/Q"))
}}
LIMIT {limit}
""".strip()


def fetch_neighborhood(
    qid: str, hops: int = 1, limit: int = 200, client: SparqlClient | None = None
) -> NeighborhoodResult:
    """Orchestrate: run the neighbor query (repeated per hop), then batch-fetch
    full entity data for the root plus all discovered neighbors.
    """
    if client is None:
        client = SparqlClient()

    frontier = {qid}
    visited = {qid}
    edges: list[tuple[str, str, str]] = []
    last_query = ""

    for _ in range(hops):
        next_frontier: set[str] = set()
        for current_qid in frontier:
            query = build_neighbor_query(current_qid, limit=limit)
            last_query = query
            result = client.query(query)
            for binding in result.get("results", {}).get("bindings", []):
                neighbor_qid = strip_entity_uri(binding["neighbor"]["value"])
                pid = strip_entity_uri(binding["prop"]["value"])
                edges.append((current_qid, neighbor_qid, pid))
                if neighbor_qid not in visited:
                    next_frontier.add(neighbor_qid)
        visited |= next_frontier
        frontier = next_frontier
        if not frontier:
            break

    entities = fetch_entities(sorted(visited))

    return NeighborhoodResult(
        root_qid=qid,
        hops=hops,
        limit=limit,
        sparql_query=last_query,
        entities=entities,
        edges=edges,
    )
