## 1. Configuration and safe service boundary

- [x] 1.1 [Backend] Add an explicit `APP_CORS_ALLOWED_ORIGINS` configuration and
  narrow CORS middleware; default to no cross-origin access, no wildcard, and no
  credentials. Verification: focused backend CORS tests cover allowed and
  unconfigured origins. Evidence: `tests/contract/test_backend_cors.py` verifies
  default denial, an explicitly allowed local origin, no credentials header, and
  rejection of wildcard or non-local configuration.
- [x] 1.2 [Frontend] Add an explicit `VITE_PREDICTION_API_BASE_URL` configuration
  boundary and a typed HTTP transport for the existing prediction contract.
  Verification: unit tests cover URL construction, JSON request shape, timeout,
  safe status mapping, and malformed response rejection. Evidence:
  `prediction-api-config.test.ts` covers explicit local configuration and
  `http-prediction-transport.test.ts` covers the contract transport boundary.
- [ ] 1.3 [Frontend] Preserve mock as the default when the API URL is absent and
  keep the browser away from CSV files, model artifacts, and local storage.
  Verification: component/client tests distinguish mock and configured modes.

## 2. ClaimVox user flow

- [ ] 2.1 [Frontend] Inject the selected prediction client into the
  classification flow and render real responses through the existing contract
  and human-review result component. Verification: tests confirm narrative-only
  requests, canonical output, review state, and no automatic routing.
- [ ] 2.2 [Frontend] Add accessible loading and recovery states for unavailable,
  rejected, timed-out, and incompatible service responses. Verification:
  keyboard and screen-reader-friendly error assertions plus responsive checks.
- [ ] 2.3 [Frontend / Backend] Ensure the local API origin can be configured for
  the Vite dev and preview workflows without becoming a public deployment
  policy. Verification: documented local commands and preflight behaviour.

## 3. Verification and evidence

- [ ] 3.1 [QA] Run frontend typecheck, lint, format, unit tests, build, focused
  backend tests, contract tests, repository quality, whitespace check, and
  strict OpenSpec validation. Record actual commands and results only.
- [ ] 3.2 [QA] Execute a local end-to-end smoke test with a synthetic narrative
  and an ignored local baseline artifact. Record only aggregate statuses,
  selected mode, review requirement, and privacy assertions in a versioned
  report; do not store request text, artifact, logs, or screenshots containing
  it.
- [ ] 3.3 [Documentation] Update only documents whose meaning changes: frontend
  and API guides, README, delivery levels, daily, changelog, NotebookLM sources,
  and evidence. Preserve the distinction between local integration and deployed
  product.

## 4. Review and closure

- [ ] 4.1 [Coordination] Reconcile `PG-6`, this change, tests, evidence, and
  Pull Request before human review. Do not mark `ESS-04` verified unless the
  full end-to-end evidence is merged and meets the delivery criterion.
- [ ] 4.2 [Coordination] Prepare the Pull Request toward `dev` with explicit
  limits, security review, verification output, and rollback note; do not merge
  or archive without human approval.
