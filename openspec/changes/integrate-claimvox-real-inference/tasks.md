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
- [x] 1.3 [Frontend] Preserve mock as the default when the API URL is absent and
  keep the browser away from CSV files, model artifacts, and local storage.
  Verification: component/client tests distinguish mock and configured modes.
  Evidence: `configured-prediction-client.test.ts` confirms absent configuration
  keeps the contract-valid mock client and does not issue a network request.

## 2. ClaimVox user flow

- [x] 2.1 [Frontend] Inject the selected prediction client into the
  classification flow and render real responses through the existing contract
  and human-review result component. Verification: tests confirm narrative-only
  requests, canonical output, review state, and no automatic routing. Evidence:
  `ClassificationPage.test.tsx` verifies a configured-service response is
  rendered as advisory human-review support and not as a simulated result.
- [x] 2.2 [Frontend] Add accessible loading and recovery states for unavailable,
  rejected, timed-out, and incompatible service responses. Verification:
  keyboard and screen-reader-friendly error assertions plus responsive checks.
  Evidence: `ClassificationPage.test.tsx` asserts generic live progress, safe
  error categories, focus transfer to the alert, and no narrative or internals
  in service-unavailable and incompatible-response recovery states.
- [x] 2.3 [Frontend / Backend] Ensure the local API origin can be configured for
  the Vite dev and preview workflows without becoming a public deployment
  policy. Verification: documented local commands and preflight behaviour.
  Evidence: `app/api/.env.example`, `app/interface/.env.example`, both component
  guides, and `tests/contract/test_backend_cors.py` define and verify the local
  opt-in path for ports `5173` and `4173`.

## 3. Verification and evidence

- [x] 3.1 [QA] Run frontend typecheck, lint, format, unit tests, build, focused
  backend tests, contract tests, repository quality, whitespace check, and
  strict OpenSpec validation. Record actual commands and results only. Evidence:
  frontend typecheck, lint, Prettier check, 47 Vitest tests and PWA build passed;
  26 focused backend contract/CORS tests, repository quality, whitespace check,
  and strict validation passed on 2026-07-28.
- [x] 3.2 [QA] Execute a local end-to-end smoke test with a synthetic narrative
  and an ignored local baseline artifact. Record only aggregate statuses,
  selected mode, review requirement, and privacy assertions in a versioned
  report; do not store request text, artifact, logs, or screenshots containing
  it. Evidence: `reports/validation/claimvox_local_inference_smoke.md` records
  successful live local service, CORS, configured frontend-module checks, and
  human visual confirmation of the advisory result and review state.
- [x] 3.3 [Documentation] Update only documents whose meaning changes: frontend
  and API guides, README, delivery levels, daily, changelog, NotebookLM sources,
  and evidence. Preserve the distinction between local integration and deployed
  product. Evidence: `README.md`, both component guides,
  `docs/project_management/delivery_levels.md`, daily, changelog and NotebookLM
  sources identify the local `ESS-04` evidence as pending review and merge, and
  explicitly exclude deployment, authentication, persistence and automatic
  routing.

## 4. Review and closure

- [x] 4.1 [Coordination] Reconcile `PG-6`, this change, tests, evidence, and
  Pull Request before human review. Do not mark `ESS-04` verified unless the
  full end-to-end evidence is merged and meets the delivery criterion. Evidence:
  the branch is clean, based on current `origin/dev` (`0` commits behind and
  `10` ahead), has no existing Pull Request, and contains the OpenSpec change,
  focused tests and `claimvox_local_inference_smoke.md`. Jira remains in its
  current operational state until the human-reviewed Pull Request is merged.
- [ ] 4.2 [Coordination] Prepare the Pull Request toward `dev` with explicit
  limits, security review, verification output, and rollback note; do not merge
  or archive without human approval.
