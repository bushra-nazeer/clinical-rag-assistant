"""Typed configuration loaded from ``config/config.yaml``."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel

DEFAULT_CONFIG_PATH = "config/config.yaml"


class Paths(BaseModel):
    index_path: str
    reports_dir: str
    figures_dir: str


class RetrieverCfg(BaseModel):
    top_k: int = 4


class LLMCfg(BaseModel):
    provider: str = "extractive"  # extractive | anthropic | openai
    anthropic_model: str = "claude-sonnet-4-6"
    openai_model: str = "gpt-4o-mini"
    max_tokens: int = 400


class EvalCfg(BaseModel):
    k: int = 4


class Config(BaseModel):
    paths: Paths
    random_state: int = 42
    retriever: RetrieverCfg = RetrieverCfg()
    llm: LLMCfg = LLMCfg()
    eval: EvalCfg = EvalCfg()


def load_config(path: str | Path = DEFAULT_CONFIG_PATH) -> Config:
    with open(path) as fh:
        data = yaml.safe_load(fh)
    return Config(**data)
