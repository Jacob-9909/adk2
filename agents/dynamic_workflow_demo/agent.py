# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ADK 2.0 **Dynamic workflows** 데모 (`ctx.run_node`, 병렬).

그래프 `edges`는 진입점 한 줄만 두고, 실제 순서·분기·병렬은 파이썬 코드로 작성합니다.
문서: https://adk.dev/workflows/dynamic/

실행: `adk web agents` → **dynamic_workflow_demo** 선택 후 아무 텍스트 입력.
"""

from __future__ import annotations

import asyncio
from typing import Any

from google.adk import Context
from google.adk import Workflow
from google.adk.workflow import node


@node(name="hello_leaf")
def hello_leaf(node_input: Any) -> str:
    """문서의 `my_node`와 같이 단순 리프 노드."""
    return f"Hello — got: {node_input!r}"


@node(name="double_text")
def double_text(node_input: str) -> str:
    return node_input * 2


@node(name="add_prefix")
def add_prefix(node_input: str) -> str:
    return f"[prefix]{node_input}"


@node(name="add_suffix")
def add_suffix(node_input: str) -> str:
    return f"{node_input}[suffix]"


@node(rerun_on_resume=True)
async def dynamic_orchestrator(ctx: Context, node_input: str):
    """순차 `run_node` 후 `asyncio.gather`로 병렬 실행."""
    seed = (node_input or "").strip() or "demo"

    step1 = await ctx.run_node(hello_leaf, seed)
    step2 = await ctx.run_node(double_text, step1)

    branch_a, branch_b = await asyncio.gather(
        ctx.run_node(add_prefix, step2),
        ctx.run_node(add_suffix, step2),
    )

    return (
        "Dynamic workflow finished.\n"
        f"- after leaf: {step1!r}\n"
        f"- after double: {step2!r}\n"
        f"- parallel prefix: {branch_a!r}\n"
        f"- parallel suffix: {branch_b!r}"
    )


root_agent = Workflow(
    name="dynamic_workflow_demo",
    edges=[("START", dynamic_orchestrator)],
)
