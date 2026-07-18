from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, ConfigDict
from datetime import datetime
import os
from dotenv import load_dotenv
from uuid import uuid4

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
        "created_at": datetime.utcnow().isoformat()
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
        "created_at": datetime.utcnow().isoformat()
    }
    await db.contact_messages.insert_one(doc)
    return {"status": "success", "message": "Message received"}

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
