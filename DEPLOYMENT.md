# Deployment Instructions

This guide covers deploying the Discover Jordan website with FastAPI backend and static frontend.

## Overview

- **Backend**: FastAPI application deployed to Render
- **Frontend**: Static HTML/CSS/JS deployed to Vercel
- **API Integration**: Frontend connects to backend via environment variable

---

## Part 1: Backend Deployment (Render)

### Prerequisites
- GitHub account
- Render account (sign up at https://render.com)
- OpenAI API key (from https://platform.openai.com/api-keys)

### Step 1: Prepare Backend for Deployment

1. **Create a `render.yaml` file** in the `backend/` directory:

```yaml
services:
  - type: web
    name: discover-jordan-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

2. **Create a `Procfile`** in the `backend/` directory:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Update CORS settings** in `backend/main.py`:

```python
# Update this line in main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-vercel-domain.vercel.app",
        "http://localhost:3000",  # For local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Step 2: Deploy to Render

1. **Push your code to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/discover-jordan.git
   git push -u origin main
   ```

2. **Create a new Web Service on Render**:
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the service**:
   - **Name**: `discover-jordan-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

4. **Add Environment Variables**:
   - Click "Environment" tab
   - Add `OPENAI_API_KEY` with your OpenAI API key value
   - Add `PYTHON_VERSION` = `3.11.0`

5. **Deploy**:
   - Click "Create Web Service"
   - Render will build and deploy your backend
   - Note the public URL (e.g., `https://discover-jordan-api.onrender.com`)

6. **Test the API**:
   - Visit `https://your-api-url.onrender.com/docs` to see the API documentation
   - Test the `/spots` endpoint

---

## Part 2: Frontend Deployment (Vercel)

### Prerequisites
- Vercel account (sign up at https://vercel.com)
- GitHub account (code pushed to GitHub)

### Step 1: Configure Frontend for Production

1. **Create `vercel.json`** in the root directory:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "env": {
    "VITE_API_URL": "@api_url"
  }
```

2. **Create a simple build script** (`build.js`) to inject API URL:

```javascript
// build.js - Simple script to replace API URL in HTML files
const fs = require('fs');
const path = require('path');

const API_URL = process.env.VITE_API_URL || process.env.API_URL || 'http://localhost:8000';

function replaceApiUrl(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  content = content.replace(
    /const API_URL = ['"].*?['"]/g,
    `const API_URL = '${API_URL}'`
  );
  fs.writeFileSync(filePath, content, 'utf8');
}

// Replace in plan.html
const planHtml = path.join(__dirname, 'plan.html');
if (fs.existsSync(planHtml)) {
  replaceApiUrl(planHtml);
  console.log('Updated API URL in plan.html');
}
```

3. **Alternative: Use environment variable in JavaScript**

Update `plan.html` to read from environment:

```javascript
// In plan.html, replace the API_URL line with:
const API_URL = window.API_URL || 'http://localhost:8000';
```

And add to each HTML file's `<head>`:

```html
<script>
  window.API_URL = 'https://your-api-url.onrender.com';
</script>
```

### Step 2: Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard

1. **Push code to GitHub** (if not already done)

2. **Import project on Vercel**:
   - Go to https://vercel.com/dashboard
   - Click "Add New..." → "Project"
   - Import your GitHub repository

3. **Configure project**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (root)
   - **Build Command**: Leave empty (static site)
   - **Output Directory**: `./` (root)

4. **Add Environment Variable**:
   - Go to "Environment Variables"
   - Add `API_URL` = `https://your-render-api-url.onrender.com`

5. **Deploy**:
   - Click "Deploy"
   - Vercel will deploy your site
   - Note your deployment URL

#### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set environment variable**:
   ```bash
   vercel env add API_URL
   # Enter: https://your-render-api-url.onrender.com
   ```

5. **Redeploy with environment variable**:
   ```bash
   vercel --prod
   ```

### Step 3: Update Frontend to Use Production API

Since Vercel doesn't support server-side environment variables for static sites, you have two options:

#### Option 1: Hardcode API URL (Simple)

Update `plan.html` directly with your Render API URL:

```javascript
const API_URL = 'https://your-api-url.onrender.com';
```

#### Option 2: Use Vercel Environment Variables (Advanced)

1. **Create `api/config.js` endpoint** (Vercel Serverless Function):

Create `api/config.js`:
```javascript
export default function handler(req, res) {
  res.status(200).json({
    apiUrl: process.env.API_URL || 'http://localhost:8000'
  });
}
```

2. **Update frontend to fetch config**:

```javascript
// In plan.html
let API_URL = 'http://localhost:8000';

async function initApiUrl() {
  try {
    const response = await fetch('/api/config');
    const config = await response.json();
    API_URL = config.apiUrl;
  } catch (error) {
    console.error('Failed to load API config, using default');
  }
}

// Call before form submission
await initApiUrl();
```

---

## Part 3: Update CORS in Backend

After deploying frontend, update backend CORS to allow your Vercel domain:

1. **Go to Render dashboard** → Your service → Environment
2. **Add environment variable**:
   - `FRONTEND_URL` = `https://your-vercel-app.vercel.app`

3. **Update `backend/main.py`**:

```python
import os

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
        "http://localhost:3000",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

4. **Redeploy backend** on Render

---

## Part 4: Testing Deployment

### Test Backend
1. Visit `https://your-api-url.onrender.com/docs`
2. Test `/spots` endpoint
3. Test `/generate` endpoint with sample data

### Test Frontend
1. Visit your Vercel deployment URL
2. Navigate to "Plan My Trip"
3. Fill out the form and generate an itinerary
4. Verify it connects to the Render API

---

## Troubleshooting

### Backend Issues

**Problem**: API returns 500 errors
- Check Render logs for errors
- Verify `OPENAI_API_KEY` is set correctly
- Check Python version compatibility

**Problem**: CORS errors
- Update `allow_origins` in backend to include your Vercel URL
- Ensure frontend URL is correct

**Problem**: Slow response times
- Render free tier spins down after inactivity
- First request may take 30-60 seconds
- Consider upgrading to paid tier for always-on service

### Frontend Issues

**Problem**: API calls fail
- Check browser console for errors
- Verify API_URL is correct in `plan.html`
- Check CORS settings in backend

**Problem**: Environment variables not working
- Vercel static sites don't support runtime env vars
- Use hardcoded API URL or serverless function approach

---

## Production Checklist

- [ ] Backend deployed to Render with public URL
- [ ] `OPENAI_API_KEY` set in Render environment
- [ ] CORS configured to allow Vercel domain
- [ ] Frontend deployed to Vercel
- [ ] API URL updated in frontend code
- [ ] All pages tested and working
- [ ] Form submission works end-to-end
- [ ] Map page loads correctly
- [ ] Navigation works on all pages

---

## Quick Reference

### Backend (Render)
- **Service URL**: `https://your-service.onrender.com`
- **API Docs**: `https://your-service.onrender.com/docs`
- **Environment**: Python 3.11
- **Required Env Var**: `OPENAI_API_KEY`

### Frontend (Vercel)
- **Deployment URL**: `https://your-app.vercel.app`
- **Framework**: Static HTML
- **Build**: None required (static files)

### API Endpoints
- `GET /spots` - List all Jordan spots
- `POST /generate` - Generate itinerary
- `GET /docs` - API documentation

---

## Support

For issues:
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs
- FastAPI: https://fastapi.tiangolo.com

