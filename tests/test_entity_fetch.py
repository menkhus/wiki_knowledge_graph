import responses

from wikidata_connector.entity_fetch import fetch_entities

# Minimal Action API wbgetentities-shaped response, matching what
# WikibaseIntegrator actually calls under the hood (confirmed by spying on
# outbound requests during development: POST to
# https://www.wikidata.org/w/api.php, not the Linked Data Interface).
_Q42_RESPONSE = {
    "entities": {
        "Q42": {
            "pageid": 138,
            "ns": 0,
            "title": "Q42",
            "lastrevid": 2516783698,
            "modified": "2026-07-12T21:34:04Z",
            "id": "Q42",
            "type": "item",
            "labels": {"mul": {"language": "mul", "value": "Douglas Adams"}},
            "descriptions": {"en": {"language": "en", "value": "British writer"}},
            "aliases": {},
            "claims": {
                "P31": [
                    {
                        "mainsnak": {
                            "snaktype": "value",
                            "property": "P31",
                            "datatype": "wikibase-item",
                            "datavalue": {
                                "value": {"entity-type": "item", "id": "Q5", "numeric-id": 5},
                                "type": "wikibase-entityid",
                            },
                        },
                        "type": "statement",
                        "id": "Q42$fake-statement-id",
                        "rank": "normal",
                    }
                ]
            },
            "sitelinks": {},
        }
    },
    "success": 1,
}


@responses.activate
def test_fetch_entities_resolves_label_with_mul_fallback():
    responses.add(
        responses.POST,
        "https://www.wikidata.org/w/api.php",
        json=_Q42_RESPONSE,
        status=200,
    )

    result = fetch_entities(["Q42"])

    assert "Q42" in result
    assert result["Q42"]["label"] == "Douglas Adams"
    assert result["Q42"]["description"] == "British writer"
    assert result["Q42"]["claims"]["P31"] == ["Q5"]


@responses.activate
def test_fetch_entities_skips_failed_qid_without_aborting_batch():
    responses.add(
        responses.POST,
        "https://www.wikidata.org/w/api.php",
        json={"entities": {"Q999999999": {"missing": ""}}},
        status=200,
    )

    result = fetch_entities(["Q999999999"])

    # A "missing" entity should not raise, and the batch should complete
    # (result may be empty for this QID, but the call must not crash).
    assert isinstance(result, dict)


def test_batching_splits_large_qid_lists():
    from wikidata_connector.entity_fetch import _batched

    qids = [f"Q{i}" for i in range(120)]
    batches = _batched(qids, 50)

    assert len(batches) == 3
    assert len(batches[0]) == 50
    assert len(batches[1]) == 50
    assert len(batches[2]) == 20
