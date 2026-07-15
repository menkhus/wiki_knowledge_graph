"""wikidata-kg — CLI entry point.

Subcommands: ping, fetch, vocab (fetch/vocab added in later phases).
"""

import argparse
import sys
import time

from wikidata_connector import config
from wikidata_connector.entity_fetch import fetch_entities
from wikidata_connector.sparql_client import SparqlClient, WikidataThrottleError


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wikidata-kg", description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    ping_parser = subparsers.add_parser("ping", help="check connectivity to WDQS and the entity-fetch endpoint")
    ping_parser.set_defaults(func=cmd_ping)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
