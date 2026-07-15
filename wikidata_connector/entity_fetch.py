"""Batch entity fetch via the Wikidata Linked Data Interface / Action API.

Retrieves full entity data (labels, descriptions, claims) for a list of
QIDs, batching into groups of ENTITY_BATCH_SIZE (matches wbgetentities'
own limit). Kept separate from query construction (see neighborhood.py /
vocab_probe.py) so it's independently testable: "can we reliably get
entity data back" vs. "what entities do we want."
"""

import sys

from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.wbi_config import config as wbi_config

from wikidata_connector import config

wbi_config["USER_AGENT"] = config.USER_AGENT


def _batched(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


# Language fallback order for labels/descriptions/aliases. Not every entity
# has an "en" label — e.g. Q42 (Douglas Adams) has no "en" label at all,
# only language-specific ones plus "mul" ("multilingual", Wikidata's
# language-agnostic value used when a label doesn't vary by language).
# Confirmed against a live fetch during development. Full multi-language
# support beyond this fallback chain is out of scope for v1 (see README).
_LABEL_LANGUAGE_FALLBACK = ("en", "mul")


def _first_available(values, languages: tuple[str, ...] = _LABEL_LANGUAGE_FALLBACK):
    for lang in languages:
        value = values.get(lang)
        if value:
            return value
    return None


def fetch_entities(qids: list[str], batch_size: int = config.ENTITY_BATCH_SIZE) -> dict[str, dict]:
    """Fetch full entity data for a list of QIDs.

    Returns a dict keyed by QID -> entity data (labels, descriptions, claims).
    Malformed/missing QIDs are skipped with a stderr notice rather than
    aborting the whole batch.
    """
    wbi = WikibaseIntegrator()
    results: dict[str, dict] = {}

    for batch in _batched(qids, batch_size):
        for qid in batch:
            try:
                # maxlag=0 disables WikibaseIntegrator's replica-lag backoff
                # (its default, maxlag=5, is tuned for edit-bots being
                # polite before a *write*; it can retry up to 1000 times
                # with growing sleeps if Wikidata's replicas are lagged,
                # which was observed live during development to compound
                # into multi-minute stalls on a batch of ~30 QIDs). This is
                # a read-only fetch — there's no edit to protect a lagged
                # replica from, so the check is unnecessary here.
                entity = wbi.item.get(entity_id=qid, maxlag=0)
            except Exception as exc:  # noqa: BLE001 - report and continue, don't abort the batch
                print(f"[entity_fetch] skipping {qid}: {exc}", file=sys.stderr)
                continue

            label = _first_available(entity.labels)
            description = _first_available(entity.descriptions)
            aliases = entity.aliases.get("en") or entity.aliases.get("mul") or []

            claims: dict[str, list[str]] = {}
            for pid, claim_group in entity.claims.get_json().items():
                targets = []
                for claim in claim_group:
                    value = (
                        claim.get("mainsnak", {})
                        .get("datavalue", {})
                        .get("value")
                    )
                    if isinstance(value, dict) and "id" in value:
                        targets.append(value["id"])  # entity-valued claim -> QID
                if targets:
                    claims[pid] = targets

            results[qid] = {
                "id": qid,
                "label": str(label) if label else None,
                "description": str(description) if description else None,
                "aliases": [str(a) for a in aliases],
                "claims": claims,
            }

    return results
