---
name: Replit backend dev domain
description: How to reach a backend workflow's public URL from the frontend in Replit.
---

For a backend workflow listening on port 8000, the public URL is the same `$REPLIT_DEV_DOMAIN` as the frontend workflow, but with `:8000` appended. The `.replit` file maps `localPort = 8000` to `externalPort = 8000`.

**Why:** Replit exposes each workflow port on a separate external port under the same dev domain. The frontend workflow typically owns the bare domain (externalPort 80), while the backend workflow owns port 8000. Calling the bare domain hits the frontend, not the backend.

**How to apply:** When configuring the frontend `API_BASE` to talk to a Replit backend, use `https://<REPLIT_DEV_DOMAIN>:8000` unless the backend is deployed to a separate domain or combined behind a reverse proxy. Update this value when the dev domain changes or when moving to a deployment.
