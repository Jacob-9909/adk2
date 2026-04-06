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

"""Mixed sequential + parallel graph: prep → 3-way fan-out → JoinNode → finalize.

Flow:
  START → sequential_prepare (strip/normalize user text)
       → (parallel_branch_a | parallel_branch_b | parallel_branch_c) 동시 실행
       → join_parallel (모든 분기 출력을 dict로 합침)
       → sequential_finalize (사용자에게 요약 메시지)

`adk web agents` → **mixed_fanout_workflow** 선택.
"""

from __future__ import annotations

from google.adk import Event
from google.adk import Workflow
from google.adk.workflow import JoinNode # 그냥 joinnode? 

join_parallel = JoinNode(name="join_parallel")


def sequential_prepare(node_input: str):
    """Single sequential step before parallel work."""
    text = (node_input or "").strip()
    if not text:
        text = "(empty)"
    return Event(output=f"[prep] {text}")


def parallel_branch_a(node_input: str):
    """Parallel worker: pseudo 'lexical' feature."""
    return Event(output=f"lex:{node_input.upper()}")


def parallel_branch_b(node_input: str):
    """Parallel worker: length / stats."""
    return Event(output=f"len:{len(node_input)}")


def parallel_branch_c(node_input: str):
    """Parallel worker: simple tag."""
    return Event(output="tag:parallel_shard_c")


def sequential_finalize(node_input: dict):
    """Runs after JoinNode; input is predecessor_name -> output."""
    lines = [f"- {name}: {value!r}" for name, value in sorted(node_input.items())]
    body = "\n".join(lines)
    return Event(
        message=(
            "Merged parallel results:\n"
            f"{body}\n"
            "---\n"
            "WORKFLOW COMPLETED."
        )
    )


root_agent = Workflow(
    name="mixed_fanout_workflow",
    edges=[
        (
            "START",
            sequential_prepare,
            (parallel_branch_a, parallel_branch_b, parallel_branch_c),
        ),
        (
            (parallel_branch_a, parallel_branch_b, parallel_branch_c),
            join_parallel,
        ),
        (join_parallel, sequential_finalize),
    ],
)


# root_agent = Workflow(
#     name="mixed_fanout_workflow",
#     edges=[
#         (
#             "START",
#             sequential_prepare,
#             (parallel_branch_a, parallel_branch_b, parallel_branch_c),
#             join_parallel,
#             sequential_finalize),
#     ],
# )