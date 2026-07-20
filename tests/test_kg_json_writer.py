import json

from wikidata_connector.kg_json_writer import (
    _build_handle_map,
    _slugify,
    edge_to_dict,
    entity_to_node,
    write_kg_json,
)
from wikidata_connector.neighborhood import NeighborhoodResult


def _entity(label=None, description=None):
    return {"id": "unused", "label": label, "description": description, "claims": {}}


def test_slugify_handles_spaces_and_punctuation():
    assert _slugify("Ada Lovelace") == "ada_lovelace"
    assert _slugify("Douglas Adams (writer)") == "douglas_adams_writer"


def test_slugify_falls_back_to_unknown_for_empty_input():
    assert _slugify("") == "unknown"
    assert _slugify("###") == "unknown"


def test_build_handle_map_uses_label_when_unique():
    entities = {"Q1": _entity("Ada Lovelace"), "Q2": _entity("London")}

    handle_map = _build_handle_map(entities)

    assert handle_map == {"Q1": "Ada Lovelace", "Q2": "London"}


def test_build_handle_map_falls_back_to_qid_on_missing_label():
    entities = {"Q1": _entity(label=None)}

    handle_map = _build_handle_map(entities)

    assert handle_map == {"Q1": "Q1"}


def test_build_handle_map_falls_back_to_qid_on_label_collision(capsys):
    # Two distinct QIDs sharing a label (e.g. two different "Lovelace"
    # entities) must not silently collide into one handle - kg_embeddings.py's
    # node_to_idx dict assumes handles are unique dict keys.
    entities = {"Q1": _entity("Lovelace"), "Q2": _entity("Lovelace")}

    handle_map = _build_handle_map(entities)

    assert handle_map["Q1"] == "Lovelace"
    assert handle_map["Q2"] == "Q2"
    assert "label collision" in capsys.readouterr().err


def test_entity_to_node_combines_label_and_description():
    node = entity_to_node("Q1", _entity("Ada Lovelace", "English mathematician"), "Ada Lovelace")

    assert node == {
        "handle": "Ada Lovelace",
        "type": "entity",
        "content": "Ada Lovelace. English mathematician",
    }


def test_entity_to_node_handles_missing_description():
    node = entity_to_node("Q1", _entity("Ada Lovelace", None), "Ada Lovelace")

    assert node["content"] == "Ada Lovelace."


def test_edge_to_dict_maps_pid_to_relationship_and_resolves_handles():
    handle_map = {"Q1": "Ada Lovelace", "Q2": "London"}

    edge = edge_to_dict("Q1", "Q2", "P19", handle_map)

    assert edge == {
        "from": "Ada Lovelace",
        "to": "London",
        "relationship": "place_of_birth",
        "reasoning": "Wikidata property P19",
    }


def test_write_kg_json_produces_valid_schema(tmp_path):
    result = NeighborhoodResult(
        root_qid="Q7259",
        hops=1,
        limit=30,
        sparql_query="SELECT ?neighbor ?prop WHERE { wd:Q7259 ?p ?neighbor . } LIMIT 30",
        entities={
            "Q7259": _entity("Ada Lovelace", "English mathematician"),
            "Q84": _entity("London", "capital of England"),
        },
        edges=[("Q7259", "Q84", "P19")],
    )

    out_path = write_kg_json(result, tmp_path)

    assert out_path == tmp_path / "ada_lovelace_kg.json"
    payload = json.loads(out_path.read_text())

    assert set(payload.keys()) == {"summary", "nodes", "edges"}
    assert "Q7259" in payload["summary"]
    assert "Ada Lovelace" in payload["summary"]

    handles = {node["handle"] for node in payload["nodes"]}
    assert handles == {"Ada Lovelace", "London"}
    for node in payload["nodes"]:
        assert set(node.keys()) == {"handle", "type", "content"}
        assert node["type"] == "entity"

    assert payload["edges"] == [
        {
            "from": "Ada Lovelace",
            "to": "London",
            "relationship": "place_of_birth",
            "reasoning": "Wikidata property P19",
        }
    ]


def test_write_kg_json_drops_edges_with_unfetched_endpoint(tmp_path):
    # An edge pointing at a QID outside the fetched entity set (e.g. beyond
    # the hop/limit boundary) must not dangle in the output - kg_embeddings's
    # get_related_edges() has no node to resolve it against.
    result = NeighborhoodResult(
        root_qid="Q7259",
        hops=1,
        limit=30,
        sparql_query="",
        entities={"Q7259": _entity("Ada Lovelace")},
        edges=[("Q7259", "Q999", "P19")],  # Q999 was never fetched
    )

    out_path = write_kg_json(result, tmp_path)
    payload = json.loads(out_path.read_text())

    assert payload["edges"] == []
    assert len(payload["nodes"]) == 1


def test_write_kg_json_creates_out_dir(tmp_path):
    nested = tmp_path / "nested" / "knowledge_graph"
    result = NeighborhoodResult(
        root_qid="Q1",
        hops=1,
        limit=30,
        sparql_query="",
        entities={"Q1": _entity("Test Entity")},
        edges=[],
    )

    out_path = write_kg_json(result, nested)

    assert out_path.exists()
    assert out_path.parent == nested
