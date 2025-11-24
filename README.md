# Discover Jordan - Tourism Website

A modern tourism website for exploring Jordan's most spectacular destinations.

## Features

- 🗺️ Interactive map with Leaflet.js
- ✈️ AI-powered itinerary generator using OpenAI
- 📍 Explore popular destinations (Petra, Wadi Rum, Dead Sea, etc.)
- 📱 Fully responsive design
- 🎨 Modern, clean UI

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **AI**: OpenAI GPT-4
- **Maps**: Leaflet.js

## Setup

### Backend

cd backend
pip install -r requirements.txt
# Create .env file with OPENAI_API_KEY
uvicorn main:app --reload --port 8000### Frontend

Simply open `index.html` in a browser or use a local server:

python -m http.server 8080## Deployment

- Backend: Deploy to Render
- Frontend: Deploy to Vercel

See `DEPLOYMENT.md` for detailed instructions.

## License

MIT
