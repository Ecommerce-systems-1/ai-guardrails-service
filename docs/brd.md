# Business Requirements Document: AI Guardrails Service

## Problem Statement

LLM-powered chatbots deployed without input/output safety layers expose companies to PII breaches, prompt injection attacks, hallucinated product data, and off-brand responses. Guardrails must run synchronously in the request path — asynchronous moderation is too slow and too late.

## High-Level Requirements (HLRs)

| ID | Requirement | Measure |
|----|-------------|---------|
| HLR-01 | All-guards execution | All 9 guards run on every request; no short-circuit on first violation |
| HLR-02 | Aggregate decision | BLOCK overrides WARN; WARN overrides ALLOW |
| HLR-03 | Input PII detection | Email, phone, credit card (Luhn-validated), SSN — all BLOCK severity |
| HLR-04 | Prompt injection detection | 10+ injection patterns matched case-insensitively — BLOCK severity |
| HLR-05 | Toxicity detection | High-tier terms BLOCK; low-tier (frustration) WARN |
| HLR-06 | Off-topic detection | Zero shopping-domain keywords → BLOCK |
| HLR-07 | Competitor mention detection | Known brand names → WARN (not BLOCK — business policy, not safety) |
| HLR-08 | Hallucination detection on output | Non-fashion product categories in response → BLOCK |
| HLR-09 | Response length enforcement | > 500 characters → WARN |
| HLR-10 | Brand voice enforcement | Apology phrases or hedging language in response → WARN |
| HLR-11 | Content moderation on output | Toxic content in LLM response → BLOCK |
| HLR-12 | Sub-50ms guardrail latency | POST /analyze p99 < 50ms (pure Python, no model inference) |
| HLR-13 | Rate limiting | 30 req/min per IP on POST /analyze |
| HLR-14 | Single-container deployment | FastAPI + Next.js static export in one Docker image, port 7860 |

## User Personas

**AI Engineer (Priya):** Evaluating guardrail approaches before production deployment. Wants to see real detection logic, not a mock. Reads the test suite to validate guard accuracy.

**Platform Engineer (Lee):** Needs a deployable Docker image with a /health endpoint and no external service dependencies. Wants non-root container for security compliance.

**Product Manager (Dana):** Needs to explain to leadership what gets blocked and why. Wants the demo frontend to clearly visualize per-guard decisions.

## Out of Scope (MVP)

- Live Anthropic API calls (pre-computed responses in fixtures eliminate API cost risk on HuggingFace)
- Persistent audit logging (no database — stateless, in-memory only)
- Multi-tenant policy configuration (single hardcoded policy for the demo)
- ML-based toxicity classifiers (pure regex/heuristics only — no model download)
- Streaming response moderation (request/response model only)
- Real product catalog integration (fictional StyleSeek catalog in scenario fixtures)
