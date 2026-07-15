"""Throttled, retrying HTTP client for the Wikidata Query Service (WDQS).

Keeps cumulative query time under WDQS's documented per-minute budget via an
in-process rolling window, and fails loudly (WikidataThrottleError) after a
capped number of retries rather than retrying forever — WDQS's own 2026
documentation notes it is measurably slower/flakier than in prior years, so
a persistent failure is plausibly not transient.
"""

import sys
import time
from collections import deque

import requests

from wikidata_connector import config


class WikidataThrottleError(RuntimeError):
    """Raised when WDQS keeps failing (429/5xx) after all retries are exhausted."""


class SparqlClient:
    def __init__(
        self,
        endpoint: str = config.WDQS_ENDPOINT,
        user_agent: str = config.USER_AGENT,
        time_budget_s: float = config.SPARQL_QUERY_TIME_BUDGET_S,
        window_s: float = config.SPARQL_THROTTLE_WINDOW_S,
        max_retries: int = config.MAX_RETRIES,
        timeout_s: float = config.REQUEST_TIMEOUT_S,
        sleep_fn=time.sleep,
        clock_fn=time.monotonic,
    ):
        self.endpoint = endpoint
        self.user_agent = user_agent
        self.time_budget_s = time_budget_s
        self.window_s = window_s
        self.max_retries = max_retries
        self.timeout_s = timeout_s
        self._sleep = sleep_fn
        self._clock = clock_fn
        # Rolling window of (end_timestamp, duration_s) for recent queries.
        self._recent_queries: deque[tuple[float, float]] = deque()

    def _throttle_if_needed(self) -> None:
        now = self._clock()
        while self._recent_queries and now - self._recent_queries[0][0] > self.window_s:
            self._recent_queries.popleft()
        cumulative = sum(d for _, d in self._recent_queries)
        if cumulative >= self.time_budget_s:
            oldest_end, _ = self._recent_queries[0]
            wait = self.window_s - (now - oldest_end)
            if wait > 0:
                print(
                    f"[sparql_client] throttling: {cumulative:.1f}s used in "
                    f"trailing {self.window_s:.0f}s window, sleeping {wait:.1f}s",
                    file=sys.stderr,
                )
                self._sleep(wait)

    def query(self, sparql: str) -> dict:
        """Run a SPARQL query against WDQS, returning the parsed JSON response.

        Raises WikidataThrottleError if retries are exhausted on 429/5xx.
        """
        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            self._throttle_if_needed()
            start = self._clock()
            try:
                resp = requests.get(
                    self.endpoint,
                    params={"query": sparql, "format": "json"},
                    headers={
                        "User-Agent": self.user_agent,
                        "Accept": "application/sparql-results+json",
                    },
                    timeout=self.timeout_s,
                )
            except requests.RequestException as exc:
                last_exc = exc
                duration = self._clock() - start
                self._recent_queries.append((self._clock(), duration))
                self._backoff(attempt)
                continue

            duration = self._clock() - start
            self._recent_queries.append((self._clock(), duration))
            print(f"[sparql_client] query took {duration:.2f}s (attempt {attempt + 1})", file=sys.stderr)

            if resp.status_code == 200:
                return resp.json()

            if resp.status_code == 429 or resp.status_code >= 500:
                last_exc = requests.HTTPError(f"HTTP {resp.status_code} from WDQS")
                self._backoff(attempt)
                continue

            resp.raise_for_status()

        raise WikidataThrottleError(
            f"WDQS query failed after {self.max_retries} attempts: {last_exc}"
        )

    def _backoff(self, attempt: int) -> None:
        if attempt < self.max_retries - 1:
            delay = config.RETRY_BACKOFF_BASE_S * (2**attempt)
            print(f"[sparql_client] retrying in {delay:.0f}s (attempt {attempt + 1} failed)", file=sys.stderr)
            self._sleep(delay)

    def ask(self, sparql: str = "ASK { ?s ?p ?o }") -> bool:
        """Trivial connectivity check — used by `wikidata-kg ping`."""
        result = self.query(sparql)
        return bool(result.get("boolean"))
