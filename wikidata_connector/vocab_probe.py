"""Capability 2: DSL/vocabulary-probe -> a domain's real property vocabulary.

Given a root QID for a *class* (e.g. Q11344, "chemical element"), enumerates
a bounded set of members of its wdt:P31/wdt:P279* subtree (the same
subtree_member_clause shared with the neighbor-enumeration query, see
query_fragments.py), fetches their entity data, and tallies which
properties actually occur across their claims.

This is a discovery tool, not just a reporting one: relation_map.py's PID
table is deliberately small and "meant to grow from real usage" (see its own
docstring); probe_vocabulary() is how that real usage gets observed, by
running relationship_for() over each domain's most common properties and
seeing which ones still fall back to the unmapped default.
"""

from collections import Counter
from dataclasses import dataclass, field

from wikidata_connector.entity_fetch import fetch_entities
from wikidata_connector.query_fragments import strip_entity_uri, subtree_member_clause
from wikidata_connector.relation_map import relationship_for
from wikidata_connector.sparql_client import SparqlClient


@dataclass
class VocabProbeResult:
    root_qid: str
    limit: int
    sparql_query: str
    member_qids: list[str]
    property_counts: dict[str, int]  # PID -> occurrence count across members' claims
    top_properties: list[tuple[str, str, int]] = field(default_factory=list)  # (pid, relationship, count)


def build_subtree_query(root_qid: str, limit: int = 200) -> str:
    """A scoped SELECT enumerating up to `limit` members of the bounded
    instance_of/subclass_of subtree rooted at `root_qid`. Kept narrow and
    QID-anchored, per WDQS's documented strength, same as
    neighborhood.build_neighbor_query.
    """
    return f"""
SELECT ?item WHERE {{
  {subtree_member_clause(root_qid)}
}}
LIMIT {limit}
""".strip()


def probe_vocabulary(
    root_qid: str, limit: int = 200, top_n: int = 15, client: SparqlClient | None = None
) -> VocabProbeResult:
    """Enumerate up to `limit` members of the subtree rooted at `root_qid`,
    fetch their entity data, and tally which properties actually occur
    across their claims - the domain's real property vocabulary, discovered
    from live data rather than assumed in advance.
    """
    if client is None:
        client = SparqlClient()

    query = build_subtree_query(root_qid, limit=limit)
    result = client.query(query)
    member_qids = [
        strip_entity_uri(binding["item"]["value"])
        for binding in result.get("results", {}).get("bindings", [])
    ]

    entities = fetch_entities(member_qids)

    property_counts: Counter[str] = Counter()
    for entity in entities.values():
        property_counts.update(entity.get("claims", {}).keys())

    top_properties = [
        (pid, relationship_for(pid), count) for pid, count in property_counts.most_common(top_n)
    ]

    return VocabProbeResult(
        root_qid=root_qid,
        limit=limit,
        sparql_query=query,
        member_qids=member_qids,
        property_counts=dict(property_counts),
        top_properties=top_properties,
    )
