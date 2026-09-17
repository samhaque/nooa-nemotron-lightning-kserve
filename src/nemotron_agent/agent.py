# SPDX-License-Identifier: Apache-2.0
"""Minimal NOOA agent exercising the on-prem Nemotron Lightning client.

Mirrors the NOOA quickstart pattern (see NVIDIA-NeMo/labs-OO-Agents
examples/quickstart/04_strategies.py): one deterministic tool method, one
PredictStrategy method for a typed single-shot call, one CodeActStrategy
method for a multi-step tool-using loop.
"""

from __future__ import annotations

from typing import Literal

from nooa import Agent, strategy
from nooa.strategies import CodeActStrategy, PredictStrategy
from pydantic import BaseModel, Field

from nemotron_agent.llm import build_llm

Severity = Literal["low", "medium", "high", "critical"]


class IncidentTriage(BaseModel):
    severity: Severity = Field(description="Impact severity of the incident.")
    affected_service: str = Field(description="Service name from the known inventory, if any.")
    summary: str = Field(description="One-sentence summary of the incident.")


class ClusterOpsAgent(Agent, llm=build_llm()):
    """You are an on-call assistant for an OpenShift cluster's platform services."""

    # SW1: deterministic tool, callable by the model, never hits the network.
    def known_services(self) -> dict[str, str]:
        """Return known service names mapped to their owning team."""
        return {
            "nemotron-lightning-predictor": "ml-platform",
            "kourier-internal": "networking",
            "kserve-controller-manager": "ml-platform",
        }

    # SW3, PredictStrategy: single-shot typed classification.
    @strategy(PredictStrategy())
    async def triage(self, report: str) -> IncidentTriage:
        """Classify an incoming incident report."""
        ...

    # SW3, CodeActStrategy (default): can call known_services() itself,
    # iterate, and decide when it has enough to answer.
    @strategy(CodeActStrategy())
    async def recommend_action(self, report: str) -> str:
        """Investigate an incident report and recommend a next action."""
        ...
