from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import json
# OpenAI removed - using rule-based system instead

app = FastAPI(title="Discover Jordan API", version="1.0.0")

# Enable CORS for frontend integration
# Get frontend URL from environment variable, fallback to localhost for development
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [
    frontend_url,
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:5500",  # Live Server
]

# In production, use specific origins. For development, you can use ["*"]
if os.getenv("ENVIRONMENT") != "production":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Predefined Jordan spots
JORDAN_SPOTS = [
    {
        "id": 1,
        "name": "Petra",
        "description": "The ancient Nabatean city carved into rose-red cliffs. One of the New Seven Wonders of the World, featuring the iconic Treasury and numerous archaeological sites.",
        "lat": 30.3285,
        "lng": 35.4444,
        "category": "history",
        "tips": "Arrive early (before 8 AM) to avoid crowds and see the Treasury in morning light. Wear comfortable walking shoes - you'll walk 4-5 km. Allow at least 4-5 hours. Bring water and sun protection."
    },
    {
        "id": 2,
        "name": "Wadi Rum",
        "description": "A stunning red desert landscape known as the Valley of the Moon. Experience jeep tours, camel rides, and overnight stays in Bedouin camps under the stars.",
        "lat": 29.5833,
        "lng": 35.4167,
        "category": "nature",
        "tips": "Book a 4x4 jeep tour for the best experience. Stay overnight in a Bedouin camp for stargazing. Bring warm clothes - desert nights are cold. Best visited in spring or autumn."
    },
    {
        "id": 3,
        "name": "Dead Sea",
        "description": "The lowest point on Earth at 430 meters below sea level. Float in the mineral-rich waters and enjoy therapeutic mud treatments at world-class spa resorts.",
        "lat": 31.5,
        "lng": 35.5,
        "category": "wellness",
        "tips": "Don't shave before visiting - the salt will sting! Apply mud 20 minutes before floating. Avoid getting water in your eyes. Best time: early morning or late afternoon. Bring waterproof camera."
    },
    {
        "id": 4,
        "name": "Jerash",
        "description": "One of the best-preserved Roman cities outside of Italy. Explore colonnaded streets, ancient temples, the Oval Plaza, and Hadrian's Arch.",
        "lat": 32.2808,
        "lng": 35.8961,
        "category": "history",
        "tips": "Visit in the morning to avoid heat. Allow 2-3 hours. The Oval Plaza and Cardo Maximus are must-sees. Wear comfortable shoes for walking on ancient stones."
    },
    {
        "id": 5,
        "name": "Amman Citadel",
        "description": "An ancient hilltop site in the heart of Amman featuring ruins from the Roman, Byzantine, and Umayyad periods. Offers panoramic views of the capital city.",
        "lat": 31.9539,
        "lng": 35.9342,
        "category": "history",
        "tips": "Best visited in the morning or late afternoon for cooler weather and better photos. Allow 1-2 hours. The Jordan Archaeological Museum is included. Great views of downtown Amman."
    },
    {
        "id": 6,
        "name": "Ajloun",
        "description": "Home to the impressive Ajloun Castle, a 12th-century Islamic fortress built to protect against Crusader attacks. Surrounded by beautiful pine forests.",
        "lat": 32.3333,
        "lng": 35.75,
        "category": "history",
        "tips": "Combine with Jerash for a full day trip. The castle offers great views. Allow 1-2 hours. Best visited in spring when the surrounding area is green."
    },
    {
        "id": 7,
        "name": "Salt",
        "description": "A historic town with beautiful Ottoman-era architecture. Known for its traditional stone buildings, markets, and rich cultural heritage.",
        "lat": 32.0389,
        "lng": 35.7272,
        "category": "cultural",
        "tips": "Explore the old souk and traditional houses. Try local sweets and traditional Jordanian food. Best visited as a half-day trip from Amman. Great for photography."
    },
    {
        "id": 8,
        "name": "Dana Biosphere Reserve",
        "description": "Jordan's largest nature reserve with diverse ecosystems, hiking trails, and stunning mountain landscapes. Perfect for nature enthusiasts.",
        "lat": 30.6833,
        "lng": 35.6167,
        "category": "nature",
        "tips": "Bring hiking boots and water. Best for nature lovers and hikers. Allow a full day. Spring and autumn are the best seasons. Stay overnight for the full experience."
    },
    {
        "id": 9,
        "name": "Mount Nebo",
        "description": "The biblical site where Moses viewed the Promised Land. Features ancient mosaics and breathtaking views of the Jordan Valley and Dead Sea.",
        "lat": 31.7667,
        "lng": 35.7167,
        "category": "history",
        "tips": "Visit early morning for best views and fewer crowds. The mosaics in the church are beautiful. Allow 1 hour. Can be combined with Dead Sea visit."
    },
    {
        "id": 10,
        "name": "Karak Castle",
        "description": "A massive Crusader castle built in the 12th century. Explore the underground passages and enjoy panoramic views of the surrounding area.",
        "lat": 31.1833,
        "lng": 35.7,
        "category": "history",
        "tips": "Wear comfortable shoes for exploring the castle ruins. Allow 1-2 hours. Great views from the top. Can be visited on the way to Petra from Amman."
    }
]

# Pydantic models for request/response
class Spot(BaseModel):
    id: int
    name: str
    description: str
    lat: float
    lng: float
    category: str

class Preferences(BaseModel):
    days: int
    interests: List[str] = []
    budget: Optional[str] = None
    include_hidden_spots: bool = False
    include_famous_places: bool = True
    include_cultural_experiences: bool = True

class Stop(BaseModel):
    name: str
    description: str
    tips: str

class DayActivity(BaseModel):
    day: int
    stops: List[Stop]

class Itinerary(BaseModel):
    days: int
    itinerary: List[DayActivity]
    generated_at: str

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "Discover Jordan API",
        "version": "1.0.0",
        "endpoints": {
            "spots": "/spots",
            "generate": "/generate"
        }
    }

@app.get("/spots", response_model=List[Spot])
async def get_spots():
    """Returns a list of all Jordan tourist spots"""
    return JORDAN_SPOTS

@app.post("/generate", response_model=Itinerary)
async def generate_itinerary(preferences: Preferences):
    """
    Generates a personalized itinerary based on user preferences using rule-based system (no OpenAI)
    """
    if preferences.days < 1 or preferences.days > 14:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 14")
    
    # Filter spots based on preferences
    selected_spots = []
    
    # Map user interests to spot categories
    interest_category_map = {
        "history": "history",
        "nature": "nature",
        "adventure": "nature",  # Adventure spots are often nature-based
        "wellness": "wellness",
        "food": "cultural"  # Food experiences are often cultural
    }
    
    # Filter by interests
    if preferences.interests:
        for spot in JORDAN_SPOTS:
            spot_category = spot.get("category", "")
            for interest in preferences.interests:
                mapped_category = interest_category_map.get(interest, interest)
                if spot_category == mapped_category:
                    selected_spots.append(spot)
                    break
    else:
        # If no interests specified, include all spots
        selected_spots = JORDAN_SPOTS.copy()
    
    # Filter by famous places preference
    famous_places = ["Petra", "Wadi Rum", "Dead Sea", "Jerash", "Amman Citadel"]
    if not preferences.include_famous_places:
        selected_spots = [s for s in selected_spots if s["name"] not in famous_places]
    
    # Filter by hidden spots preference
    hidden_spots = ["Dana Biosphere Reserve", "Mount Nebo", "Karak Castle", "Salt", "Ajloun"]
    if not preferences.include_hidden_spots:
        selected_spots = [s for s in selected_spots if s["name"] not in hidden_spots]
    
    # Filter by cultural experiences
    if not preferences.include_cultural_experiences:
        selected_spots = [s for s in selected_spots if s.get("category") != "cultural"]
    
    # Remove duplicates
    seen = set()
    unique_spots = []
    for spot in selected_spots:
        if spot["id"] not in seen:
            seen.add(spot["id"])
            unique_spots.append(spot)
    
    selected_spots = unique_spots
    
    # Validate we have spots
    if not selected_spots:
        raise HTTPException(
            status_code=400,
            detail="No spots match your preferences. Try adjusting your filters (interests, famous places, hidden spots, or cultural experiences)."
        )
    
    # Limit spots based on number of days (roughly 1-2 spots per day)
    max_spots = preferences.days * 2
    if len(selected_spots) > max_spots:
        # Prioritize: famous places first, then by category match
        priority_spots = []
        other_spots = []
        
        for spot in selected_spots:
            if spot["name"] in famous_places:
                priority_spots.append(spot)
            else:
                other_spots.append(spot)
        
        selected_spots = priority_spots + other_spots[:max_spots - len(priority_spots)]
    
    # Generate itinerary by distributing spots across days
    itinerary_days = []
    spots_per_day = max(1, len(selected_spots) // preferences.days)
    remaining_spots = len(selected_spots) % preferences.days
    
    spot_index = 0
    for day in range(1, preferences.days + 1):
        day_stops = []
        spots_for_day = spots_per_day + (1 if day <= remaining_spots else 0)
        
        for i in range(spots_for_day):
            if spot_index < len(selected_spots):
                spot = selected_spots[spot_index]
                # Get tips from spot data, or provide default tips
                tips = spot.get("tips", f"Plan to spend 2-4 hours exploring {spot['name']}. Bring comfortable walking shoes and water.")
                
                day_stops.append(Stop(
                    name=spot["name"],
                    description=spot["description"],
                    tips=tips
                ))
                spot_index += 1
        
        if day_stops:
            itinerary_days.append(DayActivity(
                day=day,
                stops=day_stops
            ))
    
    if not itinerary_days:
        raise HTTPException(
            status_code=400,
            detail="Unable to generate itinerary. Please try adjusting your preferences."
        )
    
    return Itinerary(
        days=preferences.days,
        itinerary=itinerary_days,
        generated_at=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

