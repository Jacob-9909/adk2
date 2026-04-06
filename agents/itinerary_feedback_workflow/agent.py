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

"""문서 예시: 이전 노드가 만든 `ActivitiesList`를 `payload`로 넘기며 HITL 요청.

원문: https://adk.dev/workflows/human-input/#request-input-with-data-payload

- `build_itinerary`: (데모) LLM 대신 고정 일정을 만들어 `ActivitiesList`를 출력합니다.
- `get_user_feedback`: `message` + `payload=node_input` + `response_schema` 로 사용자 의견 요청.

참고: 문서의 `response_schema={"user":"response"}` 는 타입 표기 오류로 보이며,
같은 페이지의 다른 예시와 맞추어 `user_response: str` 필드를 기대합니다.
회신 예: `{"user_response": "City walk sounds great!"}`

에이전트 선택: **itinerary_feedback_workflow**
"""

from __future__ import annotations

from typing import Dict
from typing import List

from google.adk import Event
from google.adk import Workflow
from google.adk.events import RequestInput
from pydantic import BaseModel
from pydantic import Field


class ActivitiesList(BaseModel):
    """각 활동은 이름·설명 dict."""

    itinerary: List[Dict[str, str]] = Field(
        description="활동 목록: 각 항목에 name, description",
    )


class UserFeedback(BaseModel):
    """HITL 응답."""

    user_response: str = Field(description="일정에 대한 피드백 (자유 텍스트)")


def build_itinerary(node_input: str):
    """실제론 LLM 에이전트가 채울 단계. 여기서는 결정적 샘플 데이터."""
    hint = (node_input or "").strip() or "your trip"
    data = ActivitiesList(
        itinerary=[
            {
                "name": "Morning city walk",
                "description": f"Easy walk around central area (context: {hint})",
            },
            {
                "name": "Local museum",
                "description": "Regional history and art",
            },
            {
                "name": "Food market",
                "description": "Street food and groceries",
            },
        ],
    )
    return Event(output=data)


async def get_user_feedback(node_input: ActivitiesList):
    """추천 일정을 보여 주고, 사용자 의견을 `RequestInput`으로 요청."""
    message = (
        "Here is your recommended base itinerary:\n"
        f"{node_input.model_dump_json(indent=2)}\n\n"
        "Which of these items appeal to you (if any)? "
        "Reply with JSON matching the response schema, e.g. "
        '{"user_response": "I like the museum and the market."}'
    )

    yield RequestInput( # 여기서 잠깐 멈춤 HITL
        message=message,
        payload=node_input,
        response_schema=UserFeedback,
    )


def acknowledge_feedback(node_input: UserFeedback):
    """사용자 피드백을 받은 뒤 마무리."""
    return Event(
        message=(
            "Thanks for your feedback.\n"
            f"— You wrote: {node_input.user_response}\n"
            "WORKFLOW COMPLETED."
        )
    )


root_agent = Workflow(
    name="itinerary_feedback_workflow",
    edges=[("START", build_itinerary, get_user_feedback, acknowledge_feedback)],
)
