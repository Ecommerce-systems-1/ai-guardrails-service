# 5-Questions: AI Guardrails Service

## 1. Who is the customer?

**Primary:** AI/ML Engineers and Platform Engineers at e-commerce companies deploying LLM-powered shopping assistants who need safety layers before going to production.

**Secondary:** CTOs and Engineering Leads evaluating LLM safety tooling (Guardrails AI, LlamaGuard, custom approaches) and product teams building trust in customer-facing AI.

## 2. What is the customer problem statement?

Customer-facing LLMs expose companies to simultaneous failure modes: users accidentally sending PII into chat logs, bad actors injecting prompts to extract system instructions, chatbots hallucinating products that don't exist, and off-brand or toxic responses reaching customers.

**Problem size:** A single PII breach event costs an average of $4.88M in fines and remediation (IBM Cost of a Data Breach Report, 2024). Prompt injection is OWASP's #1 risk for LLM applications (OWASP Top 10 for LLMs, 2025). Companies deploying LLM assistants without input/output guardrails are taking on regulatory, reputational, and financial risk at every conversation.

## 3. What is the high-level solution?

A policy engine with 9 configurable guards (5 input + 4 output) that intercepts every message before it reaches the LLM and every response before it reaches the user. Guards run in parallel (all checks execute regardless of earlier results), aggregate to a BLOCK / WARN / ALLOW decision, and return per-guard violation detail. A demo frontend lets reviewers select from 10 pre-built scenarios and see side-by-side with/without guardrails comparisons — no live API calls required.

## 4. What does the customer experience look like?

- Engineer evaluating the service opens the demo and clicks "Prompt Injection Attempt"
- The input panel shows the malicious message; the guard pipeline view shows PromptInjectionGuard lit red with the matched pattern
- The comparison panel shows what Claude would have said without guards vs. the polite block message with guards
- Engineer clicks "Multiple Violations" to see PIIGuard and ToxicityGuard both trigger simultaneously — demonstrating that all guards run, not just the first match

## 5. What does success look like?

| Metric | Target | Measurement |
|--------|--------|-------------|
| Guard accuracy | 100% on 10 demo scenarios | All scenarios return `expected_decision` |
| API latency | < 50ms p99 | POST /analyze with in-memory guards |
| Guard coverage | 5 input + 4 output guards | 9 guard classes, all tested |
| Test coverage | 39 tests, all passing | pytest suite |
| Zero API cost at runtime | $0 | No Anthropic API calls in production path |
| Single-container deploy | 1 Docker image | docker build + run on port 7860 |
