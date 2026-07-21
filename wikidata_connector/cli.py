"""wikidata-kg — CLI entry point.

Subcommands: ping, vocab. `fetch` (grounding-fetch -> KG JSON) is deferred
to Phase 4's CLI-unification pass — fetch_neighborhood()/write_kg_json()
are only callable directly from Python for now.
"""

import argparse
import sys
import time

from wikidata_connector import config
from wikidata_connector.entity_fetch import fetch_entities
from wikidata_connector.sparql_client import SparqlClient, WikidataThrottleError
from wikidata_connector.vocab_probe import probe_vocabulary


def cmd_ping(_args: argparse.Namespace) -> int:
    """Connectivity check: one trivial SPARQL query + one entity fetch."""
    client = SparqlClient()

    print("Checking WDQS (SPARQL endpoint)...")
    start = time.monotonic()
    try:
        ok = client.ask()
    except WikidataThrottleError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1
    elapsed = time.monotonic() - start
    print(f"  ASK query succeeded={ok} in {elapsed:.2f}s")

    print("Checking entity fetch (Q42, Douglas Adams)...")
    start = time.monotonic()
    entities = fetch_entities(["Q42"])
    elapsed = time.monotonic() - start
    entity = entities.get("Q42")
    if not entity or not entity.get("label"):
        print("FAILED: could not fetch Q42 or it has no label", file=sys.stderr)
        return 1
    print(f"  Fetched '{entity['label']}' in {elapsed:.2f}s")

    print("OK: both endpoints reachable, User-Agent accepted.")
    return 0


def cmd_vocab(args: argparse.Namespace) -> int:
    """Probe a domain's real property vocabulary: which properties actually
    appear on members of the wdt:P31/wdt:P279* subtree rooted at a QID.
    """
    result = probe_vocabulary(args.qid, limit=args.limit, top_n=args.top)

    print(f"Subtree root: {result.root_qid}")
    print(f"Members found: {len(result.member_qids)} (limit={result.limit})")
    print(f"\nTop {len(result.top_properties)} properties by frequency:")
    for pid, relationship, count in result.top_properties:
        print(f"  {pid:8} {relationship:20} {count}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wikidata-kg", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    ping_parser = subparsers.add_parser("ping", help="check connectivity to WDQS and the entity-fetch endpoint")
    ping_parser.set_defaults(func=cmd_ping)

    vocab_parser = subparsers.add_parser(
        "vocab", help="probe a domain's real property vocabulary from its Wikidata subtree"
    )
    vocab_parser.add_argument("qid", help="root QID of the class/subtree to probe (e.g. Q11344, chemical element)")
    vocab_parser.add_argument("--limit", type=int, default=200, help="max subtree members to fetch (default: 200)")
    vocab_parser.add_argument("--top", type=int, default=15, help="how many top properties to report (default: 15)")
    vocab_parser.set_defaults(func=cmd_vocab)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
