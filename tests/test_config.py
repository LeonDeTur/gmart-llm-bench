import pytest

from llmbench.config import load_config


@pytest.mark.parametrize("overrides", ["", """
    think: true
    think_effort: high
    options: {top_k: 20, min_p: 0.0, repetition_penalty: 1.05,
              presence_penalty: 0.2, frequency_penalty: 0.3, seed: 0}
"""])
def test_model_config_keys(tmp_path, overrides):
    path = tmp_path / "config.yaml"
    path.write_text("""
endpoints:
  e: {backend: openai}
models:
  m:
    endpoint: e
    model: model
""" + overrides + """
profiles:
  p: {default: m}
""", encoding="utf-8")
    config = load_config(path)
    model = config.models["m"]
    assert config.profiles["p"].model_for("stage") == "m"
    if overrides:
        assert model.think is True and model.think_effort == "high"
        assert model.options == {
            "top_k": 20, "min_p": 0.0, "repetition_penalty": 1.05,
            "presence_penalty": 0.2, "frequency_penalty": 0.3, "seed": 0,
        }
    else:
        assert model.think is None and model.think_effort is None
        assert model.options == {}
