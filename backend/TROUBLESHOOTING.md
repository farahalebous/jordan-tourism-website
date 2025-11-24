# Troubleshooting Guide

## Common Errors and Solutions

### Error: "OpenAI API key not configured"

**Solution:**
1. Create a `.env` file in the `backend/` directory
2. Add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
3. Make sure `python-dotenv` is installed:
   ```bash
   pip install python-dotenv
   ```

### Error: "Failed to parse OpenAI response as JSON"

**Possible causes:**
- OpenAI returned text instead of JSON
- Response format doesn't match expected structure

**Solution:**
- Check the backend console logs for the actual response
- The error message will show a preview of what was received
- Try generating again - sometimes OpenAI returns markdown that needs cleaning

### Error: CORS errors in browser

**Symptoms:**
- Browser console shows "CORS policy" errors
- Requests fail with network errors

**Solution:**
1. Make sure backend is running on `http://localhost:8000`
2. Make sure frontend is being served (not just opening HTML file)
3. Update CORS in `backend/main.py` to include your frontend URL
4. For local development, the code already allows all origins in dev mode

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Error: Connection refused or network errors

**Symptoms:**
- Frontend can't connect to backend
- "Failed to fetch" errors

**Solution:**
1. Check backend is running:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```
2. Verify API URL in `plan.html` is correct:
   ```javascript
   const API_URL = 'http://localhost:8000';
   ```
3. Test backend directly:
   - Visit `http://localhost:8000/docs` in browser
   - Try the `/spots` endpoint

### Error: OpenAI API rate limit

**Solution:**
- Wait a few minutes and try again
- Check your OpenAI account usage limits
- Consider upgrading your OpenAI plan

### Error: Invalid response format from OpenAI

**Symptoms:**
- Backend receives response but can't parse it
- Error mentions "Unexpected response format"

**Solution:**
- Check backend console for the actual response
- The system prompt may need adjustment
- Try generating again - responses can vary

## Testing the Backend

### Test 1: Check if backend is running
```bash
curl http://localhost:8000/
```

Should return:
```json
{"message":"Discover Jordan API","version":"1.0.0",...}
```

### Test 2: Check spots endpoint
```bash
curl http://localhost:8000/spots
```

Should return array of Jordan spots.

### Test 3: Test generate endpoint
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "days": 3,
    "interests": ["history"],
    "include_famous_places": true,
    "include_hidden_spots": false,
    "include_cultural_experiences": true
  }'
```

## Debug Mode

To see more detailed error messages, check the terminal where you're running `uvicorn`. All errors are printed to the console.

## Quick Fix Checklist

- [ ] Backend is running (`uvicorn main:app --reload --port 8000`)
- [ ] `.env` file exists in `backend/` directory
- [ ] `OPENAI_API_KEY` is set in `.env` file
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend API_URL matches backend port
- [ ] Browser console shows no CORS errors
- [ ] Test `/docs` endpoint works in browser

