from unittest.mock import MagicMock, patch

import pytest
import requests
from src.tools.perplexity_search import PerplexitySearchInput, perplexity_search_tool

_SUCCESS_JSON = {"choices": [{"message": {"content": "some result"}}]}


def _mock_resp(status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = _SUCCESS_JSON
    if status_code >= 400:
        resp.raise_for_status.side_effect = requests.HTTPError(
            response=resp
        )
    return resp


def test_tool_name_attribute():
    assert perplexity_search_tool.name == "perplexity_search"


def test_args_schema_has_query_field():
    assert "query" in PerplexitySearchInput.model_fields


def test_empty_query_raises():
    with pytest.raises(ValueError):
        perplexity_search_tool._run(query="", max_results=3)


def test_request_sent_to_perplexity_endpoint():
    with patch("src.tools.perplexity_search.requests.post") as mock_post:
        mock_post.return_value = _mock_resp()
        perplexity_search_tool._run(query="transformers")
    url = mock_post.call_args.args[0]
    assert "perplexity.ai" in url


def test_bearer_token_in_headers():
    with patch("src.tools.perplexity_search.requests.post") as mock_post:
        mock_post.return_value = _mock_resp()
        perplexity_search_tool._run(query="attention mechanism")
    headers = mock_post.call_args.kwargs["headers"]
    assert headers["Authorization"].startswith("Bearer ")


def test_returns_string_on_success():
    with patch("src.tools.perplexity_search.requests.post") as mock_post:
        mock_post.return_value = _mock_resp()
        result = perplexity_search_tool._run(query="transformers")
    assert isinstance(result, str)


def test_http_error_raises():
    with patch("src.tools.perplexity_search.requests.post") as mock_post:
        mock_post.return_value = _mock_resp(status_code=401)
        with pytest.raises((ValueError, requests.HTTPError)):
            perplexity_search_tool._run(query="transformers")


def test_rate_limit_429_raises():
    with patch("src.tools.perplexity_search.requests.post") as mock_post:
        mock_post.return_value = _mock_resp(status_code=429)
        with pytest.raises((ValueError, requests.HTTPError)):
            perplexity_search_tool._run(query="transformers")
