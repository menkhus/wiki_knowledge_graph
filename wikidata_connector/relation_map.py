"""Wikidata property (PID) -> relationship-string policy.

Decision (see this project's CLAUDE.md / notes/reference.md for the full
reasoning): use freeform relationship strings carrying real Wikidata
semantics (instance_of, subclass_of, ...) rather than forcing Wikidata's
taxonomy relations into auto_knowledge_graph's 6-value epistemic
RelationType enum (SUPPORTS/INVALIDATES/GROUNDS/REFERS_TO/DISCLAIMS/
UNRELATED). kg_embeddings.py never validates against that enum — it reads
`relationship` as an opaque display string. Forcing e.g. `instance_of` into
`SUPPORTS` would discard real information for no consumer benefit.

REFERS_TO is used as the one escape-hatch fallback (its enum value,
"refers_to", already means "generic reference to another entity") for any
property not yet in this table. The table is intentionally small at first
and meant to grow from real usage — see relationship_for()'s stderr notice
on first encountering an unmapped PID.
"""

import sys

WIKIDATA_TO_RELATIONSHIP: dict[str, str] = {
    "P31": "instance_of",
    "P279": "subclass_of",
    "P361": "part_of",
    "P527": "has_part",
    "P131": "located_in",
    "P106": "occupation",
    "P21": "sex_or_gender",
    "P569": "date_of_birth",
    "P19": "place_of_birth",
    "P800": "notable_work",
    "P1412": "languages_spoken",
    "P463": "member_of",
    "P279*": "subclass_of",  # transitive-closure marker used in SPARQL paths
}

_UNMAPPED_FALLBACK = "refers_to"
_warned_pids: set[str] = set()


def relationship_for(pid: str, pid_label: str | None = None) -> str:
    """Map a Wikidata PID to a relationship string.

    Falls back to `refers_to` for anything not in the table, logging a
    one-time stderr notice per unmapped PID so the table can be grown from
    real usage.
    """
    mapped = WIKIDATA_TO_RELATIONSHIP.get(pid)
    if mapped:
        return mapped

    if pid not in _warned_pids:
        _warned_pids.add(pid)
        label_note = f" ({pid_label})" if pid_label else ""
        print(
            f"[relation_map] unmapped property {pid}{label_note} — "
            f"falling back to '{_UNMAPPED_FALLBACK}'",
            file=sys.stderr,
        )
    return _UNMAPPED_FALLBACK
