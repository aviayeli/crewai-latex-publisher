"""Tests for the LatexPublisherSDK — the sole entry point into the pipeline."""

from unittest.mock import MagicMock, patch

from src.sdk.latex_publisher_sdk import LatexPublisherSDK

# ── version ───────────────────────────────────────────────────────────────────


def test_sdk_version_is_a_non_empty_string():
    sdk = LatexPublisherSDK()
    assert isinstance(sdk.version, str) and sdk.version


def test_sdk_version_matches_src_package_version():
    from src import __version__

    sdk = LatexPublisherSDK()
    assert sdk.version == __version__


# ── run ───────────────────────────────────────────────────────────────────────


def test_sdk_run_delegates_to_crew_kickoff():
    with patch("src.sdk.latex_publisher_sdk.PublisherCrew") as MockCrew:
        MockCrew.return_value.kickoff.return_value = "pipeline complete"
        sdk = LatexPublisherSDK()
        result = sdk.run()
    assert result == "pipeline complete"


def test_sdk_run_creates_publisher_crew_on_first_call():
    with patch("src.sdk.latex_publisher_sdk.PublisherCrew") as MockCrew:
        MockCrew.return_value.kickoff.return_value = "done"
        sdk = LatexPublisherSDK()
        sdk.run()
    MockCrew.assert_called_once()


def test_sdk_run_reuses_crew_across_multiple_calls():
    with patch("src.sdk.latex_publisher_sdk.PublisherCrew") as MockCrew:
        MockCrew.return_value.kickoff.return_value = "done"
        sdk = LatexPublisherSDK()
        sdk.run()
        sdk.run()
    assert MockCrew.call_count == 1


def test_sdk_run_calls_kickoff_each_time():
    with patch("src.sdk.latex_publisher_sdk.PublisherCrew") as MockCrew:
        mock_crew = MagicMock()
        mock_crew.kickoff.return_value = "done"
        MockCrew.return_value = mock_crew
        sdk = LatexPublisherSDK()
        sdk.run()
        sdk.run()
    assert mock_crew.kickoff.call_count == 2


def test_sdk_crew_is_none_before_first_run():
    sdk = LatexPublisherSDK()
    assert sdk._crew is None


def test_sdk_crew_is_set_after_run():
    with patch("src.sdk.latex_publisher_sdk.PublisherCrew") as MockCrew:
        MockCrew.return_value.kickoff.return_value = "done"
        sdk = LatexPublisherSDK()
        sdk.run()
    assert sdk._crew is not None


# ── topic passthrough ─────────────────────────────────────────────────────────


def test_sdk_run_passes_topic_as_inputs_to_kickoff():
    with patch("src.sdk.latex_publisher_sdk.PublisherCrew") as MockCrew:
        MockCrew.return_value.kickoff.return_value = "done"
        sdk = LatexPublisherSDK()
        sdk.run(topic="Quantum Computing")
    MockCrew.return_value.kickoff.assert_called_once_with(
        inputs={"topic": "Quantum Computing"}
    )


def test_sdk_run_with_no_topic_passes_empty_string():
    with patch("src.sdk.latex_publisher_sdk.PublisherCrew") as MockCrew:
        MockCrew.return_value.kickoff.return_value = "done"
        sdk = LatexPublisherSDK()
        sdk.run()
    MockCrew.return_value.kickoff.assert_called_once_with(inputs={"topic": ""})
