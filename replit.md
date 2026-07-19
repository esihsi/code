# Dan·Moosa Hair Studio

A luxury unisex salon website for Dan·Moosa Hair Studio in Krishnarajapuram, Bengaluru.

## Project Overview

This is a static, single-page website built with plain HTML and CSS. It showcases the salon's services, story, gallery, testimonials, and booking flow, and routes booking requests through WhatsApp.

- **Frontend**: `index.html` (root-level static site)
- **Assets**: salon images (`Studio.png`, `Interior.png`, `HairWash.png`, `Facial.png`, `Reception.png`, `Customer Photo 1-7.png`, `Logo.png`, `Logo 2.png`)
- **Backend**: `backend/server.py` (FastAPI) and `frontend/` (React/Vite scaffold) exist but are not currently wired into the running site
- **Traffic capture**: `index.html` sends a small page-view beacon to `POST /api/visits` on the FastAPI backend; data is stored in MongoDB when available, otherwise in `backend/traffic.jsonl` as a fallback. View stats at `/admin/traffic` on the backend.

## How to Run

The website is served as a static site from the project root on port 5000. Start the Replit workflow **"Start application"** or run:

```bash
python -m http.server 5000
```

Then open the preview panel or visit the dev domain.

## User Preferences

- Keep the website's existing luxury salon aesthetic (cream, terracotta, olive palette; Cormorant Garamond + Outfit fonts).
- Use local image assets rather than external GitHub URLs when possible.
- Preserve the current single-page static structure unless the user explicitly asks to migrate to the React/Vite scaffold or connect the FastAPI backend.
