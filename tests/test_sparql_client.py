import responses

from wikidata_connector import config
from wikidata_connector.sparql_client import SparqlClient, WikidataThrottleError


@responses.activate
def test_query_sends_user_agent_header():
    responses.add(
        responses.GET,
        config.WDQS_ENDPOINT,
        json={"boolean": True},
        status=200,
    )
    client = SparqlClient(sleep_fn=lambda _s: None)
    result = client.ask()

    assert result is True
    sent_headers = responses.calls[0].request.headers
    assert sent_headers["User-Agent"] == config.USER_AGENT


@responses.activate
def test_retries_on_429_then_succeeds():
    responses.add(responses.GET, config.WDQS_ENDPOINT, status=429)
    responses.add(responses.GET, config.WDQS_ENDPOINT, json={"boolean": True}, status=200)

    sleeps = []
    client = SparqlClient(sleep_fn=lambda s: sleeps.append(s))
    result = client.ask()

    assert result is True
    assert len(responses.calls) == 2
    assert len(sleeps) == 1  # one backoff sleep between the two attempts


@responses.activate
def test_raises_throttle_error_after_exhausting_retries():
    for _ in range(5):
        responses.add(responses.GET, config.WDQS_ENDPOINT, status=429)

    client = SparqlClient(sleep_fn=lambda _s: None, max_retries=3)

    try:
        client.ask()
        assert False, "expected WikidataThrottleError"
    except WikidataThrottleError:
        pass

    assert len(responses.calls) == 3  # stopped at max_retries, didn't keep going forever


@responses.activate
def test_throttle_sleeps_when_time_budget_exhausted():
    responses.add(responses.GET, config.WDQS_ENDPOINT, json={"boolean": True}, status=200)

    fake_now = [0.0]

    def fake_clock():
        return fake_now[0]

    sleeps = []

    def fake_sleep(seconds):
        sleeps.append(seconds)
        fake_now[0] += seconds

    client = SparqlClient(
        sleep_fn=fake_sleep,
        clock_fn=fake_clock,
        time_budget_s=10.0,
        window_s=60.0,
    )
    # Simulate a prior query that already used up the whole time budget,
    # ending "now" (fake_now[0] == 0.0).
    client._recent_queries.append((0.0, 10.0))

    client.ask()

    assert len(sleeps) == 1
    assert sleeps[0] > 0
