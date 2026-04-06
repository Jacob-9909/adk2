# ADK 2.0 시작 템플릿

Google ADK **2.0 알파**의 **그래프 워크플로**(`Workflow`) 예제입니다.

## 요구 사항

- Python 3.11+
- **Vertex AI:** GCP 프로젝트 + 서비스 계정(또는 사용자) IAM  
- **또는** `GEMINI_API_KEY`(AI Studio, Vertex 미사용)

### Vertex + 서비스 계정 JSON

1. [IAM](https://console.cloud.google.com/iam-admin/iam)에서 서비스 계정에 **`Vertex AI 사용자`** (`roles/aiplatform.user`) 부여.  
2. 해당 서비스 계정에 **키 만들기(JSON)** 후, 이 저장소 밖 또는 `credentials/`(git 제외)에 보관.  
3. `.env`에 다음을 설정:
   - `GOOGLE_APPLICATION_CREDENTIALS` — 키 파일의 **절대 경로**
   - `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`
   - `GOOGLE_GENAI_USE_VERTEXAI=1`

애플리케이션은 **ADC**로 이 키를 자동 사용합니다. 이때 `gcloud auth application-default login` 은 필요 없습니다(키 파일만으로 충분).

## 설치

```bash
cd <이 저장소 루트>
uv sync
# 또는: uv venv --python 3.13 && uv pip install -e .
```

## 실행

```bash
cp .env.example .env
# .env 에 API 키 또는 GCP 설정 입력

uv run adk web agents
```

브라우저에서 개발 UI가 뜨면 에이전트 **`city_workflow`**, **`routing_workflow`**, **`mixed_fanout_workflow`**, **`human_input_workflow`**, **`itinerary_feedback_workflow`**, **`dynamic_workflow_demo`** 중 하나를 선택합니다.

## 구조

| 경로 | 설명 |
|------|------|
| `agents/city_workflow/agent.py` | 순차 Workflow: 도시 생성 → 시각 조회(함수) → 보고 LLM → 완료 메시지 |
| `agents/routing_workflow/agent.py` | 분기 Workflow: 분류 LLM → `router` → BUG / CUSTOMER_SUPPORT / LOGISTICS |
| `agents/mixed_fanout_workflow/agent.py` | 순차 → **병렬 fan-out**(튜플) → `JoinNode` → 순차 요약 (LLM 없음, 로직 데모) |
| `agents/human_input_workflow/agent.py` | HITL: `yield RequestInput(...)` → 사용자 응답 → 후속 함수 (`response_schema`는 `NumberAnswer`) |
| `agents/itinerary_feedback_workflow/agent.py` | HITL + **payload**: `ActivitiesList` 출력 → `RequestInput(payload=...)` → `UserFeedback` |
| `agents/dynamic_workflow_demo/agent.py` | **Dynamic workflow**: `edges=[(START, orchestrator)]` 만 두고 `@node` + `ctx.run_node` + `asyncio.gather` (LLM 불필요) |

ADK 2.0은 알파이므로 프로덕션에서는 1.x 사용을 권장합니다. 자세한 내용은 [ADK 문서 — Graph-based workflows](https://google.github.io/adk-docs/workflows/)를 참고하세요.
