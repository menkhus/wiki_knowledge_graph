"""SPARQL query fragments shared between neighborhood.py (grounding-fetch)
and vocab_probe.py (DSL/vocabulary-probe), so the traversal pattern isn't
duplicated between the two capabilities.
"""

ENTITY_URI_PREFIX = "http://www.wikidata.org/entity/"


def strip_entity_uri(uri: str) -> str:
    """'http://www.wikidata.org/entity/Q42' -> 'Q42'."""
    if uri.startswith(ENTITY_URI_PREFIX):
        return uri[len(ENTITY_URI_PREFIX) :]
    return uri


def subtree_member_clause(root_qid: str) -> str:
    """The `wdt:P31/wdt:P279*` bounded-subtree membership clause, shared by
    both the neighbor-enumeration query and the vocabulary-probe's subtree
    queries. Anchored to a single starting QID, per WDQS's own guidance
    ("designed for when you know the characteristics of your desired
    data") — never an open/unbounded pattern.
    """
    return f"?item wdt:P31/wdt:P279* wd:{root_qid} ."
