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

"""Human input (HITL) graph: `RequestInput`로 멈췄다가 사용자 응답 후 다음 노드 실행.

문서: https://adk.dev/workflows/human-input/

실행 후 개발 UI에서 **human_input_workflow** 선택. 인터럽트 시 스키마에 맞는
응답을 보내야 다음 단계로 진행됩니다 (`response_schema`는 자동 변환을 보장하지 않음).

예: `{"value": 7}` 형태(JSON)로 `value` 정수를 넣어 회신.
"""

from __future__ import annotations

from google.adk import Event
from google.adk import Workflow
from google.adk.events import RequestInput
from pydantic import BaseModel
from pydantic import Field


class NumberAnswer(BaseModel):
    """사용자 응답 스키마."""

    value: int = Field(description="곱하기 할 정수")


def ask_for_number():
    """HITL: 사용자 입력이 올 때까지 워크플로를 일시 중단."""
    yield RequestInput(
        message=(
            "정수 하나를 알려 주세요. 응답은 아래 스키마와 동일한 형식이어야 합니다.\n"
            '예: {"value": 21}'
        ),
        payload={
            "note": "참고용 페이로드(선택). UI에서 함께 표시될 수 있습니다.",
            "example_answer": {"value": 10},
        },
        response_schema=NumberAnswer,
    )


def double_user_number(node_input: NumberAnswer):
    """인간 응답이 이어지면 실행됩니다."""
    n = node_input.value
    return Event(message=f"입력값: {n} → 2배: {n * 2}")


root_agent = Workflow(
    name="human_input_workflow",
    edges=[("START", ask_for_number, double_user_number)],
)
