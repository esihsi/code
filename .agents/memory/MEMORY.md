---
name: project-structure
---

# Project Structure Note

- The imported project is currently served as a static single-page site from `index.html` in the workspace root, not from the `frontend/` React/Vite scaffold described in the README.
- `backend/server.py` (FastAPI) and the `frontend/` directory exist but are not wired into the running site.
- Any future work that assumes the README's React/FastAPI structure should first verify whether the static root site has been migrated or if the backend has been connected.

- [Replit backend URL](replit-backend-url.md) — A backend workflow on port 8000 shares the same dev domain as the frontend but must be accessed with `:8000`.
