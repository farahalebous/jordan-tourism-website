# Discover Jordan API

A simple FastAPI backend for the Discover Jordan tourism website with rule-based itinerary generation.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note:** No API keys or external services required! The system uses a free rule-based algorithm.

## Running the Server

```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /spots
Returns a list of all Jordan tourist spots with their details.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Petra",
    "description": "...",
    "lat": 30.3285,
    "lng": 35.4444,
    "category": "history"
  }
]
```

### POST /generate
Generates a personalized itinerary based on user preferences using a rule-based system (no external APIs required).

**Request Body:**
```json
{
  "days": 5,
  "interests": ["history", "nature"],
  "budget": "comfort",
  "include_hidden_spots": true,
  "include_famous_places": true,
  "include_cultural_experiences": true
}
```

**Response:**
```json
{
  "days": 5,
  "itinerary": [
    {
      "day": 1,
      "stops": [
        {
          "name": "Petra",
          "description": "The ancient Nabatean city carved into rose-red cliffs...",
          "tips": "Arrive early to avoid crowds. Wear comfortable walking shoes. Allow at least 4-5 hours to explore."
        }
      ]
    }
  ],
  "generated_at": "2025-01-10T12:00:00"
}
```

**Note:** This endpoint uses a free rule-based system - no API keys or external services required!

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

