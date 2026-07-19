from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone
from uuid import uuid4
import os
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "dan_moosa_db")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Fallback storage for traffic when MongoDB is unavailable
TRAFFIC_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traffic.jsonl")

# ============ Models ============
class Service(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    description: str
    price_from: int
    duration_min: int
    category: str

class Review(BaseModel):
    model_config = ConfigDict(extra="ignore")
    author: str
    text: str
    rating: int

class ReviewResponse(BaseModel):
    overall_rating: float
    total_reviews: int
    sources: list[str]
    reviews: list[Review]

class Booking(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    phone: str
    email: str | None = None
    service: str
    stylist_preference: str | None = None
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    notes: str | None = None

class BookingResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    name: str
    phone: str
    email: str | None
    service: str
    stylist_preference: str | None
    date: str
    time: str
    notes: str | None
    status: str
    created_at: str

class ContactMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    email: str
    phone: str
    message: str

class Visit(BaseModel):
    model_config = ConfigDict(extra="ignore")
    path: str = "/"
    referrer: str | None = None
    screen_width: int | None = None
    screen_height: int | None = None
    language: str | None = None

# ============ Storage Helpers ============
async def store_visit(visit_doc: dict) -> None:
    """Store a visit in MongoDB; fall back to local JSON lines if MongoDB is unavailable."""
    try:
        await db.visits.insert_one(visit_doc)
        return
    except Exception as e:
        print(f"MongoDB visit store failed: {e}")
    # Fallback: append to JSON lines file
    try:
        with open(TRAFFIC_FILE, "a") as f:
            f.write(json.dumps(visit_doc, default=str) + "\n")
    except Exception as e:
        print(f"Fallback visit store failed: {e}")

async def load_visits() -> list[dict]:
    """Load visits from MongoDB or the local fallback file."""
    visits = []
    try:
        visits = await db.visits.find().to_list(None)
        visits = [{**v, "_id": str(v.get("_id", ""))} for v in visits]
        return visits
    except Exception as e:
        print(f"MongoDB stats read failed: {e}")
    if os.path.exists(TRAFFIC_FILE):
        try:
            with open(TRAFFIC_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        visits.append(json.loads(line))
        except Exception as e:
            print(f"Fallback stats read failed: {e}")
    return visits

# ============ Services Endpoint ============
@app.get("/api/services")
async def get_services():
    services = [
        {"id": "1", "name": "Haircut", "description": "Professional haircut tailored to your style", "price_from": 300, "duration_min": 30, "category": "hair"},
        {"id": "2", "name": "Hair Color", "description": "Premium hair coloring with quality products", "price_from": 800, "duration_min": 120, "category": "color"},
        {"id": "3", "name": "Hair Spa", "description": "Relaxing spa treatment for healthy hair", "price_from": 600, "duration_min": 60, "category": "spa"},
        {"id": "4", "name": "Styling", "description": "Expert styling for any occasion", "price_from": 400, "duration_min": 45, "category": "styling"},
        {"id": "5", "name": "Beard Craft", "description": "Precision beard grooming and shaping", "price_from": 250, "duration_min": 25, "category": "beard"},
        {"id": "6", "name": "Keratin Treatment", "description": "Smoothing keratin treatment for silky hair", "price_from": 1200, "duration_min": 150, "category": "treatment"},
        {"id": "7", "name": "Facial", "description": "Rejuvenating facial treatments", "price_from": 800, "duration_min": 60, "category": "facial"},
        {"id": "8", "name": "Bridal", "description": "Complete bridal makeup and styling", "price_from": 2000, "duration_min": 180, "category": "bridal"},
    ]
    return services

# ============ Reviews Endpoint ============
@app.get("/api/reviews")
async def get_reviews():
    reviews = [
        {"author": "Nitin Nagappan", "text": "Excellent service, friendly staff, great ambience, quality products.", "rating": 5},
        {"author": "Archana Das", "text": "Truly satisfied with the experience and would highly recommend this place!", "rating": 5},
        {"author": "Abdus Salam", "text": "All the Staff will give friendly vibe and on the other hand best services.", "rating": 5},
    ]
    return ReviewResponse(
        overall_rating=4.7,
        total_reviews=85,
        sources=["Justdial", "Google"],
        reviews=reviews
    )

# ============ Bookings Endpoints ============
@app.post("/api/bookings")
async def create_booking(booking: Booking):
    booking_doc = {
        "id": str(uuid4()),
        **booking.model_dump(),
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.bookings.insert_one(booking_doc)
    return booking_doc

@app.get("/api/bookings")
async def get_bookings():
    bookings = await db.bookings.find().to_list(None)
    return [{**b, "_id": str(b.get("_id", ""))} for b in bookings]

# ============ Contact Endpoint ============
@app.post("/api/contact")
async def create_contact(message: ContactMessage):
    doc = {
        "id": str(uuid4()),
        **message.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.contact_messages.insert_one(doc)
    return {"status": "success", "message": "Message received"}

# ============ Traffic / Visit Tracking ============
@app.post("/api/visits")
async def record_visit(request: Request, visit: Visit):
    """Record a page visit. Captures page path, device info, and IP/User-Agent from the request headers."""
    # Try to get the real client IP even if behind a proxy
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    elif request.client:
        ip = request.client.host
    else:
        ip = None

    visit_doc = {
        "id": str(uuid4()),
        **visit.model_dump(),
        "ip": ip,
        "user_agent": request.headers.get("user-agent"),
        "referrer": visit.referrer or request.headers.get("referer"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    await store_visit(visit_doc)
    return {"status": "success"}

@app.get("/api/visits/stats")
async def get_visit_stats():
    """Return traffic statistics from MongoDB or the local fallback file."""
    visits = await load_visits()
    total = len(visits)
    unique_ips = len(set(v.get("ip") for v in visits if v.get("ip")))
    today = datetime.now(timezone.utc).date().isoformat()
    visits_today = len([v for v in visits if v.get("timestamp", "").startswith(today)])
    recent = sorted(visits, key=lambda v: v.get("timestamp", ""), reverse=True)[:50]

    return {
        "total_visits": total,
        "unique_visitors": unique_ips,
        "visits_today": visits_today,
        "recent_visits": recent,
    }

@app.get("/admin/traffic", response_class=HTMLResponse)
async def traffic_dashboard():
    """Simple HTML dashboard for viewing captured traffic."""
    stats = await get_visit_stats()
    rows = ""
    for v in stats["recent_visits"]:
        ua = v.get("user_agent") or ""
        rows += (
            f"<tr>"
            f"<td>{v.get('timestamp', '')}</td>"
            f"<td>{v.get('path', '')}</td>"
            f"<td>{v.get('ip', '')}</td>"
            f"<td>{ua[:70]}{'...' if len(ua) > 70 else ''}</td>"
            f"<td>{v.get('referrer', '')}</td>"
            f"</tr>"
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dan·Moosa Traffic Dashboard</title>
<style>
body {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 2rem; background: #FAF9F6; color: #1C1B1A; }}
.cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
.card {{ background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
.card h2 {{ margin: 0; font-size: 2rem; color: #9C5B42; }}
.card p {{ margin: 0.25rem 0 0; color: #5C5A56; font-size: 0.875rem; }}
table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 0.5rem; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
th, td {{ text-align: left; padding: 0.75rem 1rem; border-bottom: 1px solid #E5DFD5; font-size: 0.875rem; }}
th {{ background: #1C1B1A; color: #FAF9F6; font-weight: 500; }}
tr:hover {{ background: #F3EFEA; }}
</style>
</head>
<body>
<h1>Dan·Moosa Hair Studio — Traffic Dashboard</h1>
<div class="cards">
  <div class="card"><h2>{stats['total_visits']}</h2><p>Total Visits</p></div>
  <div class="card"><h2>{stats['unique_visitors']}</h2><p>Unique Visitors</p></div>
  <div class="card"><h2>{stats['visits_today']}</h2><p>Visits Today</p></div>
</div>
<table>
  <thead>
    <tr><th>Time</th><th>Page</th><th>IP</th><th>User Agent</th><th>Referrer</th></tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
</body>
</html>"""
    return html

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
