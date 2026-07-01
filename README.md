# AI Guardrails Service

A policy engine that protects customer-facing shopping chatbots with 9 configurable safety guards. Live detection logic runs on every request; responses are pre-computed so no Anthropic API costs are incurred in the demo.

## Why I built it

Customer-facing LLMs expose companies to PII breaches, prompt injection attacks, hallucinated product data, and off-brand responses simultaneously. Rule-based keyword filters catch surface patterns; a policy engine with typed guards, severity levels, and full-pipeline execution catches compound violations and gives engineers per-guard audit trails. This project demonstrates the architecture pattern used by production LLM safety platforms.

**Problem size:** The average PII breach costs $4.88M in fines and remediation (IBM, 2024). Prompt injection is OWASP's #1 LLM risk (OWASP Top 10 for LLMs, 2025).

## Who it's for

- **AI Engineers** evaluating guardrail approaches before deploying a shopping assistant to production
- **Platform Engineers** who need a deployable, self-contained safety layer with a /health endpoint
- **Product Managers** who need to explain to leadership what gets blocked and why

## Core Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Guard coverage | 9 guards (5 input + 4 output) | ✅ |
| Test suite | 39 tests passing | ✅ |
| API latency (p99) | < 50ms | ✅ ~15ms local |
| Runtime API cost | $0 | ✅ No live LLM calls |
| Container footprint | Single Docker image | ✅ |

## Architecture

```
POST /analyze
  → Input Guards (all 5 run, no short-circuit)
      PIIGuard · PromptInjectionGuard · ToxicityGuard · OffTopicGuard · CompetitorMentionGuard
  → If any BLOCK: return block response from fixture
  → Else: Output Guards (all 4 run)
      HallucinationGuard · ResponseLengthGuard · BrandVoiceGuard · ContentModerationGuard
  → Aggregate (BLOCK > WARN > ALLOW) → AnalyzeResponse
```

FastAPI serves the API and Next.js static export from a single Docker container on port 7860.

## Tradeoffs

- **Pure regex/heuristics over ML classifiers:** No model download, no inference latency, fully deterministic and testable. Tradeoff: lower recall on novel phrasing (a production system would layer in a toxicity classifier).
- **Pre-computed fixture responses over live API:** Eliminates API cost risk on a public demo URL. Tradeoff: responses don't adapt to user edits of the input text (the scenario fixture is always used).
- **In-memory stateless over persistent audit log:** Zero infrastructure dependencies, instant restart. Tradeoff: no audit history across requests (a production deployment would write to a structured log store).

## Edge Cases Solved

- **Luhn validation on credit cards:** `4111-1111-1111-1111` triggers PIIGuard; `4111-1111-1111-1112` (invalid Luhn) does not — prevents false positives on reference numbers and order IDs that happen to be 16 digits.
- **All guards run on BLOCK:** A message with both PII and toxic content shows both violations — the pipeline never short-circuits on the first match.
- **Output guards on WARN inputs:** Competitor mention (WARN) still triggers output guard pipeline — a response that also violates brand voice bumps to WARN.

## What I'd Do Differently

1. **Layer in a lightweight ML toxicity scorer** (e.g., `detoxify`) alongside regex for recall on novel phrasing — run async to avoid latency impact.
2. **Structured audit logging to PostgreSQL** — immutable record of every violation for compliance reporting and model fine-tuning signals.
3. **Policy-as-config:** Guard thresholds (severity tiers, keyword lists, competitor names) loaded from a YAML/JSON config file instead of hardcoded — enables per-tenant policy overrides without code changes.

## Running Locally

```bash
pip install -r requirements.txt
uvicorn src.api.main:app --port 7860 --reload
# frontend dev server:
cd frontend && npm install && npm run dev
```

## Running Tests

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t ai-guardrails .
docker run -p 7860:7860 ai-guardrails
```

## HuggingFace Space

Live demo: https://huggingface.co/spaces/placeholder/ai-guardrails-service
