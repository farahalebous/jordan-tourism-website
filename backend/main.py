from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        "category": "history"
    },
    {
        "id": 2,
        "name": "Wadi Rum",
        "description": "A stunning red desert landscape known as the Valley of the Moon. Experience jeep tours, camel rides, and overnight stays in Bedouin camps under the stars.",
        "lat": 29.5833,
        "lng": 35.4167,
        "category": "nature"
    },
    {
        "id": 3,
        "name": "Dead Sea",
        "description": "The lowest point on Earth at 430 meters below sea level. Float in the mineral-rich waters and enjoy therapeutic mud treatments at world-class spa resorts.",
        "lat": 31.5,
        "lng": 35.5,
        "category": "wellness"
    },
    {
        "id": 4,
        "name": "Jerash",
        "description": "One of the best-preserved Roman cities outside of Italy. Explore colonnaded streets, ancient temples, the Oval Plaza, and Hadrian's Arch.",
        "lat": 32.2808,
        "lng": 35.8961,
        "category": "history"
    },
    {
        "id": 5,
        "name": "Amman Citadel",
        "description": "An ancient hilltop site in the heart of Amman featuring ruins from the Roman, Byzantine, and Umayyad periods. Offers panoramic views of the capital city.",
        "lat": 31.9539,
        "lng": 35.9342,
        "category": "history"
    },
    {
        "id": 6,
        "name": "Ajloun",
        "description": "Home to the impressive Ajloun Castle, a 12th-century Islamic fortress built to protect against Crusader attacks. Surrounded by beautiful pine forests.",
        "lat": 32.3333,
        "lng": 35.75,
        "category": "history"
    },
    {
        "id": 7,
        "name": "Salt",
        "description": "A historic town with beautiful Ottoman-era architecture. Known for its traditional stone buildings, markets, and rich cultural heritage.",
        "lat": 32.0389,
        "lng": 35.7272,
        "category": "cultural"
    },
    {
        "id": 8,
        "name": "Dana Biosphere Reserve",
        "description": "Jordan's largest nature reserve with diverse ecosystems, hiking trails, and stunning mountain landscapes. Perfect for nature enthusiasts.",
        "lat": 30.6833,
        "lng": 35.6167,
        "category": "nature"
    },
    {
        "id": 9,
        "name": "Mount Nebo",
        "description": "The biblical site where Moses viewed the Promised Land. Features ancient mosaics and breathtaking views of the Jordan Valley and Dead Sea.",
        "lat": 31.7667,
        "lng": 35.7167,
        "category": "history"
    },
    {
        "id": 10,
        "name": "Karak Castle",
        "description": "A massive Crusader castle built in the 12th century. Explore the underground passages and enjoy panoramic views of the surrounding area.",
        "lat": 31.1833,
        "lng": 35.7,
        "category": "history"
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
    Generates a personalized itinerary based on user preferences using OpenAI
    """
    if preferences.days < 1 or preferences.days > 14:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 14")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
        )
    
    # Build user preferences description
    preferences_text = f"""
    Number of days: {preferences.days}
    Interests: {', '.join(preferences.interests) if preferences.interests else 'No specific interests'}
    Budget: {preferences.budget if preferences.budget else 'Not specified'}
    Include hidden spots: {preferences.include_hidden_spots}
    Include famous places: {preferences.include_famous_places}
    Include cultural experiences: {preferences.include_cultural_experiences}
    """
    
    # System prompt
    system_prompt = """Create a Jordan itinerary based on user preferences. 

Return JSON only in this exact format: [{"day":1, "stops":[{"name":"Location Name", "description":"Detailed description", "tips":"Helpful tips for visitors"}]}].

Make sure to:
- Distribute activities across the specified number of days
- Include 1-3 stops per day depending on the number of days
- Focus on locations that match the user's interests
- Include famous places like Petra, Wadi Rum, Dead Sea, Jerash if requested
- Include hidden gems like Dana Biosphere Reserve, Mount Nebo, Karak Castle, Salt, Ajloun if requested
- Include cultural experiences if requested
- Provide detailed descriptions and practical tips for each location
- Consider travel time between locations
- Return valid JSON only, no additional text."""
    
    # User message
    user_message = f"""Create a {preferences.days}-day Jordan itinerary with the following preferences:
{preferences_text}

Available Jordan destinations include:
- Petra (ancient Nabatean city, one of the New Seven Wonders)
- Wadi Rum (red desert, Valley of the Moon)
- Dead Sea (lowest point on Earth, therapeutic waters)
- Jerash (best-preserved Roman city)
- Amman Citadel (ancient hilltop site in Amman)
- Ajloun (12th-century Islamic castle)
- Salt (historic Ottoman town)
- Dana Biosphere Reserve (nature reserve, hiking)
- Mount Nebo (biblical site with mosaics)
- Karak Castle (Crusader castle)

Return the itinerary as JSON in the specified format."""
    
    try:
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract JSON from response
        response_content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if response_content.startswith("```json"):
            response_content = response_content[7:]
        if response_content.startswith("```"):
            response_content = response_content[3:]
        if response_content.endswith("```"):
            response_content = response_content[:-3]
        response_content = response_content.strip()
        
        # Parse JSON response
        try:
            itinerary_data = json.loads(response_content)
            
            # Handle both direct array and wrapped object formats
            if isinstance(itinerary_data, dict) and "itinerary" in itinerary_data:
                itinerary_list = itinerary_data["itinerary"]
            elif isinstance(itinerary_data, list):
                itinerary_list = itinerary_data
            elif isinstance(itinerary_data, dict):
                # Try to find array in the response
                for key, value in itinerary_data.items():
                    if isinstance(value, list):
                        itinerary_list = value
                        break
                else:
                    itinerary_list = []
            else:
                raise ValueError(f"Unexpected response format. Got: {type(itinerary_data)}")
            
            # Validate we have data
            if not itinerary_list:
                raise ValueError("No itinerary data found in OpenAI response")
            
            # Convert to our model format
            itinerary_days = []
            for day_data in itinerary_list:
                if not isinstance(day_data, dict):
                    continue
                    
                stops = []
                for stop in day_data.get("stops", []):
                    if not isinstance(stop, dict):
                        continue
                    stops.append(Stop(
                        name=stop.get("name", "Unknown Location"),
                        description=stop.get("description", ""),
                        tips=stop.get("tips", "")
                    ))
                
                if stops:  # Only add day if it has stops
                    itinerary_days.append(DayActivity(
                        day=day_data.get("day", len(itinerary_days) + 1),
                        stops=stops
                    ))
            
            if not itinerary_days:
                raise ValueError("No valid itinerary days found in response")
            
            return Itinerary(
                days=preferences.days,
                itinerary=itinerary_days,
                generated_at=datetime.now().isoformat()
            )
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {str(e)}")
            print(f"Response content: {response_content[:500]}")  # Print first 500 chars
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse OpenAI response as JSON: {str(e)}. Response preview: {response_content[:200]}"
            )
        except ValueError as e:
            print(f"Value Error: {str(e)}")
            print(f"Response content: {response_content[:500]}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing OpenAI response: {str(e)}"
            )
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            print(f"Response content: {response_content[:500]}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing OpenAI response: {str(e)}"
            )
            
    except Exception as e:
        error_msg = str(e)
        print(f"OpenAI API Error: {error_msg}")
        # Check for specific OpenAI errors
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key is invalid or missing. Please check your OPENAI_API_KEY environment variable."
            )
        elif "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=429,
                detail="OpenAI API rate limit exceeded. Please try again later."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling OpenAI API: {error_msg}"
            )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

