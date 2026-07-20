import wikidata_connector.neighborhood as neighborhood
from wikidata_connector.neighborhood import build_neighbor_query, fetch_neighborhood
from wikidata_connector.sparql_client import SparqlClient


class FakeSparqlClient(SparqlClient):
    """Subclasses SparqlClient purely so the type checker accepts it where
    `client: SparqlClient | None` is expected — fetch_neighborhood only ever
    calls `.query(sparql)` on it, none of the real HTTP/throttle machinery
    from `__init__` is used. No HTTP mocking needed here (unlike
    entity_fetch, which talks to WikibaseIntegrator directly and has no
    equivalent injectable seam).
    """

    def __init__(self, bindings_by_qid: dict[str, list[dict]]):
        self.bindings_by_qid = bindings_by_qid
        self.queries: list[str] = []

    def query(self, sparql: str) -> dict:
        self.queries.append(sparql)
        # Every query built by build_neighbor_query embeds "wd:{qid}" —
        # recover which QID this call was for so the fake can answer per-QID.
        for qid, bindings in self.bindings_by_qid.items():
            if f"wd:{qid} " in sparql:
                return {"results": {"bindings": bindings}}
        return {"results": {"bindings": []}}


def _binding(neighbor_qid: str, pid: str) -> dict:
    return {
        "neighbor": {"value": f"http://www.wikidata.org/entity/{neighbor_qid}"},
        "prop": {"value": f"http://www.wikidata.org/entity/{pid}"},
    }


def test_build_neighbor_query_embeds_qid_and_limit():
    query = build_neighbor_query("Q7259", limit=30)

    assert "wd:Q7259" in query
    assert "LIMIT 30" in query


def test_fetch_neighborhood_single_hop(monkeypatch):
    fake_client = FakeSparqlClient(
        {"Q7259": [_binding("Q123", "P19"), _binding("Q456", "P106")]}
    )
    fetched_qids = []

    def fake_fetch_entities(qids, _batch_size=50):
        fetched_qids.append(sorted(qids))
        return {qid: {"id": qid, "label": qid, "description": None, "claims": {}} for qid in qids}

    monkeypatch.setattr(neighborhood, "fetch_entities", fake_fetch_entities)

    result = fetch_neighborhood("Q7259", hops=1, limit=30, client=fake_client)

    assert result.root_qid == "Q7259"
    assert result.hops == 1
    assert result.limit == 30
    assert result.sparql_query == fake_client.queries[-1]
    assert set(result.entities) == {"Q7259", "Q123", "Q456"}
    assert ("Q7259", "Q123", "P19") in result.edges
    assert ("Q7259", "Q456", "P106") in result.edges
    # Root plus both discovered neighbors are fetched in one batch call.
    assert fetched_qids == [["Q123", "Q456", "Q7259"]]
    # Only one SPARQL query issued for a single hop starting from one QID.
    assert len(fake_client.queries) == 1


def test_fetch_neighborhood_two_hops_expands_frontier(monkeypatch):
    fake_client = FakeSparqlClient(
        {
            "Q1": [_binding("Q2", "P31")],
            "Q2": [_binding("Q3", "P279")],
        }
    )

    monkeypatch.setattr(
        neighborhood,
        "fetch_entities",
        lambda qids, _batch_size=50: {
            qid: {"id": qid, "label": qid, "description": None, "claims": {}} for qid in qids
        },
    )

    result = fetch_neighborhood("Q1", hops=2, limit=30, client=fake_client)

    # Hop 1 queries Q1 (discovers Q2), hop 2 queries Q2 (discovers Q3).
    assert len(fake_client.queries) == 2
    assert set(result.entities) == {"Q1", "Q2", "Q3"}
    assert ("Q1", "Q2", "P31") in result.edges
    assert ("Q2", "Q3", "P279") in result.edges


def test_fetch_neighborhood_does_not_requery_already_visited_qid(monkeypatch):
    # Q1 -> Q2 via P31, and Q2 -> Q1 via P31 (a real-world reciprocal-ish
    # edge shape). Q1 must not be re-queried as part of hop 2's frontier
    # since it was already visited in hop 1.
    fake_client = FakeSparqlClient(
        {
            "Q1": [_binding("Q2", "P31")],
            "Q2": [_binding("Q1", "P31")],
        }
    )

    monkeypatch.setattr(
        neighborhood,
        "fetch_entities",
        lambda qids, _batch_size=50: {
            qid: {"id": qid, "label": qid, "description": None, "claims": {}} for qid in qids
        },
    )

    result = fetch_neighborhood("Q1", hops=2, limit=30, client=fake_client)

    # Frontier after hop 1 is {Q2} (Q1 already visited), so hop 2 only
    # queries Q2 - never re-queries Q1.
    assert len(fake_client.queries) == 2
    assert set(result.entities) == {"Q1", "Q2"}


def test_fetch_neighborhood_stops_early_when_frontier_empties(monkeypatch):
    # No outgoing bindings at all for Q1 -> frontier empties after hop 1,
    # so a requested hops=3 should still only issue one query.
    fake_client = FakeSparqlClient({"Q1": []})

    monkeypatch.setattr(
        neighborhood,
        "fetch_entities",
        lambda qids, _batch_size=50: {
            qid: {"id": qid, "label": qid, "description": None, "claims": {}} for qid in qids
        },
    )

    result = fetch_neighborhood("Q1", hops=3, limit=30, client=fake_client)

    assert len(fake_client.queries) == 1
    assert result.edges == []
    assert set(result.entities) == {"Q1"}
