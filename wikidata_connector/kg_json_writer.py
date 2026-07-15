"""Nodes/edges -> validated *_kg.json, consumable by
auto_knowledge_graph/kg_embeddings.py.

The consumer (`KGEmbeddingIndex._load_kg_nodes()`) globs `*_kg.json` and
reads plain dicts via `.get()` with silent empty-string/list defaults on
missing keys. This writer deliberately does NOT rely on that forgiving
behavior — every node always gets explicit handle/type/content, every edge
always gets explicit from/to/relationship, so a malformed write fails
loudly here rather than silently producing an empty search string or a
dangling edge reference downstream.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from wikidata_connector.neighborhood import NeighborhoodResult
from wikidata_connector.relation_map import relationship_for


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug or "unknown"


def _build_handle_map(entities: dict[str, dict]) -> dict[str, str]:
    """QID -> handle, using the entity's label where available and unique,
    falling back to the QID itself on a missing or colliding label.
    kg_embeddings.py's node_to_idx dict assumes handles are usable as dict
    keys — a collision would silently overwrite an entry, so uniqueness is
    guaranteed here rather than left to chance.
    """
    seen_labels: dict[str, str] = {}  # label -> first QID that claimed it
    handle_map: dict[str, str] = {}

    for qid, entity in entities.items():
        label = entity.get("label")
        if label and label not in seen_labels:
            seen_labels[label] = qid
            handle_map[qid] = label
        else:
            handle_map[qid] = qid  # missing label, or collision -> fall back to QID
            if label:
                print(
                    f"[kg_json_writer] label collision on '{label}' "
                    f"({qid} vs {seen_labels[label]}) — using QID as handle for {qid}",
                    file=sys.stderr,
                )

    return handle_map


def entity_to_node(qid: str, entity: dict, handle: str) -> dict:
    label = entity.get("label") or qid
    description = entity.get("description") or ""
    content = f"{label}. {description}".strip()
    return {"handle": handle, "type": "entity", "content": content}


def edge_to_dict(from_qid: str, to_qid: str, pid: str, handle_map: dict[str, str]) -> dict:
    from_handle = handle_map.get(from_qid, from_qid)
    to_handle = handle_map.get(to_qid, to_qid)
    relationship = relationship_for(pid)
    return {
        "from": from_handle,
        "to": to_handle,
        "relationship": relationship,
        "reasoning": f"Wikidata property {pid}",
    }


def write_kg_json(result: NeighborhoodResult, out_dir: Path) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    handle_map = _build_handle_map(result.entities)

    nodes = [
        entity_to_node(qid, entity, handle_map[qid])
        for qid, entity in result.entities.items()
    ]

    # Only emit edges where both endpoints were actually fetched (an edge
    # to a QID outside the fetched entity set would dangle — no node for
    # kg_embeddings.py's get_related_edges() to resolve it against).
    edges = [
        edge_to_dict(from_qid, to_qid, pid, handle_map)
        for from_qid, to_qid, pid in result.edges
        if from_qid in result.entities and to_qid in result.entities
    ]

    root_label = result.entities.get(result.root_qid, {}).get("label", result.root_qid)
    timestamp = datetime.now(timezone.utc).isoformat()
    summary = (
        f"Wikidata neighborhood fetch: root={result.root_qid} ({root_label}), "
        f"hops={result.hops}, limit={result.limit}, fetched_at={timestamp}. "
        f"SPARQL: {result.sparql_query}"
    )

    payload = {"summary": summary, "nodes": nodes, "edges": edges}

    filename = f"{_slugify(root_label)}_kg.json"
    out_path = out_dir / filename
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return out_path
