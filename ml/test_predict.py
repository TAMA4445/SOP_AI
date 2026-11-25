import pytest

from ml.predict import predict_risk

EXPECTED_KEYS = {
    "predicted_level",
    "confidence",
    "probabilities",
    "classes",
    "risk_explanation",
}


def test_predict_risk_normal_input():
    result = predict_risk(
        "Operator hand was caught in the press machine while cleaning the die"
    )
    assert set(result.keys()) == EXPECTED_KEYS
    assert result["predicted_level"] in result["classes"]
    assert 0.0 <= result["confidence"] <= 1.0
    assert set(result["probabilities"].keys()) == set(result["classes"])
    assert sum(result["probabilities"].values()) == pytest.approx(1.0, abs=0.01)


@pytest.mark.parametrize("bad", ["", "   ", None])
def test_predict_risk_empty_input(bad):
    with pytest.raises(ValueError):
        predict_risk(bad)


def test_predict_risk_very_long_input():
    text = "The worker slipped near the machine and injured his arm. " * 100
    result = predict_risk(text)
    assert set(result.keys()) == EXPECTED_KEYS
    assert result["predicted_level"] in result["classes"]
