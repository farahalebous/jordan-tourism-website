# Discover Jordan API

A simple FastAPI backend for the Discover Jordan tourism website with OpenAI integration.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up OpenAI API key:
   - Get your API key from https://platform.openai.com/api-keys
   - Create a `.env` file in the backend directory:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

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
Generates a personalized itinerary based on user preferences using OpenAI GPT.

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

**Note:** This endpoint requires an OpenAI API key to be set in the `.env` file.

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

