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


def test_yaml_word_names_and_boolean_values(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("""
endpoints:
  off: {backend: openai, think_mode: off}
models:
  no: {endpoint: off, model: model, think: true}
  yes: {endpoint: off, model: model, think: false}
profiles:
  off:
    default: no
    stages: {on: yes, off: no, yes: no, no: yes, skipped: null}
  on: {default: no}
  yes: {default: yes}
""", encoding="utf-8")

    config = load_config(path)

    assert list(config.endpoints) == ["off"]
    assert config.endpoints["off"].name == "off"
    assert config.endpoints["off"].think_mode == "off"
    assert list(config.models) == ["no", "yes"]
    assert config.models["no"].name == "no"
    assert config.models["no"].endpoint == "off"
    assert config.models["no"].think is True
    assert config.models["yes"].think is False
    assert list(config.profiles) == ["off", "on", "yes"]
    for name, profile in config.profiles.items():
        assert profile.name == name
    assert config.profiles["off"].default == "no"
    assert config.profiles["on"].model_for("stage") == "no"
    assert config.profiles["yes"].model_for("stage") == "yes"
    assert config.profiles["off"].stages == {
        "on": "yes", "off": "no", "yes": "no", "no": "yes", "skipped": None,
    }
    config.validate()


def test_numeric_names_and_references(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("""
endpoints:
  1: {backend: openai}
models:
  2: {endpoint: 1, model: model}
profiles:
  3: {default: 2, stages: {4: 2, skipped: null}}
""", encoding="utf-8")

    config = load_config(path)

    assert list(config.endpoints) == ["1"]
    assert config.endpoints["1"].name == "1"
    assert list(config.models) == ["2"]
    assert config.models["2"].name == "2"
    assert config.models["2"].endpoint == "1"
    assert list(config.profiles) == ["3"]
    assert config.profiles["3"].name == "3"
    assert config.profiles["3"].default == "2"
    assert config.profiles["3"].stages == {"4": "2", "skipped": None}
    assert config.profiles["3"].model_for("4") == "2"
    assert config.profiles["3"].model_for("other") == "2"
    config.validate()


def test_existing_config_and_env_expansion(tmp_path, monkeypatch):
    monkeypatch.setenv("LLMBENCH_TEST_KEY", "secret")
    monkeypatch.delenv("LLMBENCH_TEST_URL", raising=False)
    path = tmp_path / "config.yaml"
    path.write_text("""
endpoints:
  local:
    backend: openai
    base_url: ${LLMBENCH_TEST_URL:-http://localhost:8000/v1}
    api_key: ${LLMBENCH_TEST_KEY}
models:
  small: {endpoint: local, model: model, think: false, options: {seed: 0}}
profiles:
  baseline: {default: small, stages: {'scenario.*': small, skipped: null}}
run:
  repeat: 2
  concurrency: 3
  stages: ['scenario.*']
  tags: [smoke]
  exclude_tags: [slow]
""", encoding="utf-8")

    config = load_config(path)

    assert config.endpoints["local"].base_url == "http://localhost:8000/v1"
    assert config.endpoints["local"].api_key == "secret"
    assert config.models["small"].options == {"seed": 0}
    assert config.models["small"].think is False
    assert config.profiles["baseline"].default == "small"
    assert config.profiles["baseline"].model_for("scenario.plan") == "small"
    assert config.profiles["baseline"].model_for("skipped") is None
    assert config.repeat == 2
    assert config.concurrency == 3
    assert config.stages == ["scenario.*"]
    assert config.tags == ["smoke"]
    assert config.exclude_tags == ["slow"]
