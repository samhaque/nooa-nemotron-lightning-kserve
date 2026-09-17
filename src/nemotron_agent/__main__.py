# SPDX-License-Identifier: Apache-2.0
"""Runnable demo: uv run python -m nemotron_agent"""

import asyncio

from nemotron_agent.agent import ClusterOpsAgent


async def main() -> None:
    agent = ClusterOpsAgent()
    report = "nemotron-lightning-predictor is returning 503s for all requests since 09:14 UTC."

    triage = await agent.triage(report)
    print(f"severity={triage.severity} service={triage.affected_service}")
    print(f"summary: {triage.summary}\n")

    action = await agent.recommend_action(report)
    print(f"recommended action:\n{action}")


if __name__ == "__main__":
    asyncio.run(main())
