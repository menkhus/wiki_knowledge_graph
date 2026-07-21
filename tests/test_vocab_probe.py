import wikidata_connector.vocab_probe as vocab_probe
from wikidata_connector.sparql_client import SparqlClient
from wikidata_connector.vocab_probe import build_subtree_query, probe_vocabulary


class FakeSparqlClient(SparqlClient):
    """Same pattern as test_neighborhood.py's FakeSparqlClient: a real
    SparqlClient subclass (so `client: SparqlClient | None` type-checks)
    that answers `.query()` from a canned binding list instead of HTTP.
    """

    def __init__(self, bindings: list[dict]):
        self.bindings = bindings
        self.queries: list[str] = []

    def query(self, sparql: str) -> dict:
        self.queries.append(sparql)
        return {"results": {"bindings": self.bindings}}


def _member(qid: str) -> dict:
    return {"item": {"value": f"http://www.wikidata.org/entity/{qid}"}}


def _entity(claims: dict[str, list[str]]) -> dict:
    return {"id": "unused", "label": None, "description": None, "claims": claims}


def test_build_subtree_query_embeds_root_qid_and_limit():
    query = build_subtree_query("Q11344", limit=50)

    assert "wd:Q11344" in query
    assert "wdt:P31/wdt:P279*" in query
    assert "LIMIT 50" in query


def test_probe_vocabulary_tallies_property_frequency(monkeypatch):
    fake_client = FakeSparqlClient([_member("Q1"), _member("Q2"), _member("Q3")])

    monkeypatch.setattr(
        vocab_probe,
        "fetch_entities",
        lambda _qids: {
            "Q1": _entity({"P31": ["Q5"], "P21": ["Q6581097"]}),
            "Q2": _entity({"P31": ["Q5"]}),
            "Q3": _entity({"P31": ["Q5"], "P106": ["Q901"]}),
        },
    )

    result = probe_vocabulary("Q5", limit=200, top_n=15, client=fake_client)

    assert result.root_qid == "Q5"
    assert result.limit == 200
    assert result.sparql_query == fake_client.queries[-1]
    assert set(result.member_qids) == {"Q1", "Q2", "Q3"}
    assert result.property_counts == {"P31": 3, "P21": 1, "P106": 1}


def test_probe_vocabulary_top_properties_sorted_and_relationship_mapped(monkeypatch):
    fake_client = FakeSparqlClient([_member("Q1"), _member("Q2"), _member("Q3")])

    monkeypatch.setattr(
        vocab_probe,
        "fetch_entities",
        lambda _qids: {
            "Q1": _entity({"P31": ["Q5"], "P21": ["Q6581097"]}),
            "Q2": _entity({"P31": ["Q5"]}),
            "Q3": _entity({"P31": ["Q5"], "P106": ["Q901"]}),
        },
    )

    result = probe_vocabulary("Q5", limit=200, top_n=2, client=fake_client)

    # top_n=2 caps the report even though 3 distinct PIDs were observed.
    assert len(result.top_properties) == 2
    # Most frequent first; known PID maps to its real relationship string.
    assert result.top_properties[0] == ("P31", "instance_of", 3)


def test_probe_vocabulary_unmapped_pid_falls_back_via_relation_map(monkeypatch):
    fake_client = FakeSparqlClient([_member("Q1")])

    monkeypatch.setattr(
        vocab_probe,
        "fetch_entities",
        lambda _qids: {"Q1": _entity({"P9999999": ["Q1"]})},
    )

    result = probe_vocabulary("Q5", limit=200, top_n=15, client=fake_client)

    assert result.top_properties == [("P9999999", "refers_to", 1)]


def test_probe_vocabulary_handles_empty_subtree(monkeypatch):
    fake_client = FakeSparqlClient([])

    monkeypatch.setattr(vocab_probe, "fetch_entities", lambda _qids: {})

    result = probe_vocabulary("Q5", limit=200, top_n=15, client=fake_client)

    assert result.member_qids == []
    assert result.property_counts == {}
    assert result.top_properties == []
