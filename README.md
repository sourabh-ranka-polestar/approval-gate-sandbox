# approval-gate-sandbox

Throwaway test of: publish to a preview, then a GitHub Environment approval, then import to the Apidog
SANDBOX project's main. Never point it at the developer portal (project 1373099); the workflow refuses.

Setup: secret APIDOG_ACCESS_TOKEN; variables SANDBOX_PROJECT_ID (1343253) and optional SANDBOX_PREVIEW_BRANCH_ID;
Environment `sandbox-main-approval` with required reviewers.
