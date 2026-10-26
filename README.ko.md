# adk2

[English](README.md) | **한국어**

Google ADK **2.0 알파**의 **그래프 워크플로**(`Workflow`) 예제 템플릿입니다. 6개의 작은 에이전트로 순차, 분기, 병렬 fan-out, Human-in-the-loop, 동적 워크플로를 보여 주며, ADK 개발 UI에서 하나씩 실행해 볼 수 있습니다.

> ADK 2.0은 알파 버전이므로 프로덕션에는 1.x를 권장합니다. 자세한 내용은 [ADK 문서 — Graph-based workflows](https://google.github.io/adk-docs/workflows/)를 참고하세요.

## 예제

| 에이전트 | 패턴 | 내용 |
|---|---|---|
| [`city_workflow`](agents/city_workflow/agent.py) | 순차 | 도시 생성 → 시각 조회(함수) → 보고 LLM → 완료 메시지 |
| [`routing_workflow`](agents/routing_workflow/agent.py) | 분기 | 분류 LLM → `router` → BUG / CUSTOMER_SUPPORT / LOGISTICS |
| [`mixed_fanout_workflow`](agents/mixed_fanout_workflow/agent.py) | 병렬 fan-out | 순차 → 병렬 fan-out(튜플) → `JoinNode` → 요약 (LLM 없음) |
| [`human_input_workflow`](agents/human_input_workflow/agent.py) | Human-in-the-loop | `yield RequestInput(...)` → 사용자 응답 → 후속 함수 (`response_schema`는 `NumberAnswer`) |
| [`itinerary_feedback_workflow`](agents/itinerary_feedback_workflow/agent.py) | payload HITL | `ActivitiesList` 출력 → `RequestInput(payload=...)` → `UserFeedback` |
| [`dynamic_workflow_demo`](agents/dynamic_workflow_demo/agent.py) | 동적 | `edges=[(START, orchestrator)]`만 두고 `@node` + `ctx.run_node` + `asyncio.gather` (LLM 없음) |

## 빠른 시작

Python 3.11 이상과 [uv](https://docs.astral.sh/uv/)가 필요합니다.

```bash
uv sync
cp .env.example .env     # GEMINI_API_KEY 또는 Vertex AI 설정 입력
uv run adk web agents
```

브라우저에 뜬 개발 UI에서 위 에이전트 중 하나를 선택합니다.

## 인증 설정

두 방법 중 하나를 쓰면 됩니다.

**방법 A: Gemini API 키 (AI Studio)** — `.env`에 `GEMINI_API_KEY`를 설정합니다.

**방법 B: Vertex AI + 서비스 계정**

1. [IAM](https://console.cloud.google.com/iam-admin/iam)에서 서비스 계정에 **Vertex AI 사용자**(`roles/aiplatform.user`) 역할을 부여합니다.
2. JSON 키를 만들어 저장소 밖이나 `credentials/`(git 제외)에 보관합니다.
3. `.env`에 다음을 설정합니다.
   - `GOOGLE_APPLICATION_CREDENTIALS`: 키 파일의 절대 경로
   - `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`
   - `GOOGLE_GENAI_USE_VERTEXAI=1`

애플리케이션은 ADC로 이 키를 자동 사용하므로 `gcloud auth application-default login`은 필요 없습니다.
