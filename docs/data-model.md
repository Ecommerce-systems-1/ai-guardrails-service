# Data Model: AI Guardrails Service

## Guard Result

Every guard returns a `GuardResult` dataclass:

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `guard_name` | string | e.g. `PIIGuard` | Name of the guard that produced this result |
| `triggered` | bool | true / false | Whether the guard detected a violation |
| `severity` | enum | `BLOCK` \| `WARN` \| `PASS` | Action severity: BLOCK stops the request, WARN flags it, PASS is clean |
| `violations` | list[string] | e.g. `["email: j***@gmail.com"]` | Human-readable description of each match (PII values masked) |
| `details` | string | e.g. `"1 PII entity detected"` | Summary explanation of the result |

## Scenario Fixture Schema

Each entry in `data/scenarios.json`:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | URL-safe unique identifier (e.g. `pii_email`) |
| `title` | string | Human-readable scenario name for the UI |
| `category_tag` | enum | `ALLOW` \| `WARN` \| `BLOCK` — expected decision, used for card color coding |
| `user_input` | string | The message sent by the (simulated) user |
| `raw_response` | string | Pre-computed LLM response (no guardrails applied) |
| `guarded_response` | string | Pre-computed response after guardrails (block message, sanitized response, or truncated version) |
| `expected_decision` | enum | `ALLOW` \| `WARN` \| `BLOCK` — used for test assertions |

## API Schemas

### POST /analyze Request

```json
{
  "scenario_id": "pii_email",
  "user_input": "My email is john@gmail.com, where is my order?"
}
```

Validation: `scenario_id` required; `user_input` required, max 500 characters (422 if violated).

### POST /analyze Response

```json
{
  "scenario_id": "pii_email",
  "user_input": "My email is john@gmail.com, where is my order?",
  "final_decision": "BLOCK",
  "input_analysis": [
    {
      "guard_name": "PIIGuard",
      "triggered": true,
      "severity": "BLOCK",
      "violations": ["email: j***@gmail.com"],
      "details": "1 PII entity(ies) detected"
    },
    {
      "guard_name": "PromptInjectionGuard",
      "triggered": false,
      "severity": "PASS",
      "violations": [],
      "details": "No injection patterns detected"
    }
  ],
  "output_analysis": [],
  "without_guardrails": "I found your account for john@gmail.com! Your order #ORD-29471...",
  "with_guardrails": "Your request was blocked. Please don't share personal information..."
}
```

`output_analysis` is empty (`[]`) when `final_decision` is BLOCK from input guards — output guards are not run.

### GET /scenarios Response

```json
{
  "scenarios": [
    {
      "id": "clean_query",
      "title": "Clean shopping query",
      "category_tag": "ALLOW",
      "user_input": "What are your best winter coats?"
    }
  ]
}
```

Note: `raw_response` and `guarded_response` are not included in the list response — they are returned only by POST /analyze.

### GET /health Response

```json
{
  "status": "ok",
  "scenarios_loaded": 10,
  "guards_loaded": 9
}
```

## Guard Severity Decision Table

| Input Decision | Output Decision | Final Decision | with_guardrails |
|---------------|-----------------|----------------|-----------------|
| BLOCK | (not run) | BLOCK | `guarded_response` |
| ALLOW | BLOCK | BLOCK | `guarded_response` |
| ALLOW | WARN | WARN | `guarded_response` |
| WARN | ALLOW | WARN | `guarded_response` |
| ALLOW | ALLOW | ALLOW | `raw_response` (same as without) |

## Retention & Compliance

- No user data stored — the service is fully stateless; no database, no logs persisted
- PII values in violations are masked before being returned (email: `j***@domain.com`, card: `****-****-****-1234`)
- All scenario data is fictional (no real customer data in fixtures)
- No Anthropic API key in the container — no LLM calls at runtime
