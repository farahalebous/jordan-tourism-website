# Quick Setup Guide

## Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Step 2: Set Up OpenAI API Key

1. Get your API key from https://platform.openai.com/api-keys
2. Create a `.env` file in the `backend/` directory:
   ```bash
   touch .env
   ```
3. Add your API key to the `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## Step 3: Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Step 4: Test the API

### Option A: Use the test script
```bash
cd backend
python test_api.py
```

### Option B: Test in browser
1. Open http://localhost:8000/docs
2. Try the `/spots` endpoint (should work immediately)
3. Try the `/generate` endpoint with this test data:
   ```json
   {
     "days": 3,
     "interests": ["history"],
     "include_famous_places": true,
     "include_hidden_spots": false,
     "include_cultural_experiences": true
   }
   ```

## Step 5: Test the Frontend

1. Open `plan.html` in your browser (or serve it with a local server)
2. Fill out the form
3. Click "Generate Itinerary"
4. Check the browser console (F12) for any errors

## Common Issues

### "OpenAI API key not configured"
- Make sure `.env` file exists in `backend/` directory
- Make sure it contains `OPENAI_API_KEY=your_key`
- Restart the uvicorn server after creating `.env`

### "Failed to fetch" or CORS errors
- Make sure backend is running on port 8000
- Make sure you're opening the HTML file through a web server, not directly
- Try using a simple HTTP server:
  ```bash
  # Python 3
  python -m http.server 8080
  
  # Then open http://localhost:8080/plan.html
  ```

### Backend not starting
- Check if port 8000 is already in use
- Try a different port: `uvicorn main:app --reload --port 8001`
- Update `API_URL` in `plan.html` to match

### OpenAI errors
- Check your OpenAI account has credits
- Verify the API key is correct
- Check the backend console for detailed error messages

## Debugging Tips

1. **Check backend console** - All errors are printed there
2. **Check browser console** (F12) - Network errors appear there
3. **Test endpoints directly** - Use http://localhost:8000/docs
4. **Use the test script** - `python test_api.py` will check everything

## File Structure

```
backend/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env                 # Your API keys (create this!)
├── test_api.py          # Test script
└── README.md            # Full documentation
```

