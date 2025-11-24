# Quick Start Deployment Guide

## Backend to Render (5 minutes)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Create Render Service**
   - Go to https://dashboard.render.com
   - New → Web Service
   - Connect GitHub repo
   - Settings:
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variable:
     - `OPENAI_API_KEY` = your OpenAI key
   - Deploy!

3. **Copy your Render URL** (e.g., `https://discover-jordan-api.onrender.com`)

---

## Frontend to Vercel (3 minutes)

1. **Update API URL in plan.html**
   ```javascript
   // Line ~175 in plan.html
   const API_URL = 'https://your-render-api-url.onrender.com';
   ```

2. **Deploy to Vercel**
   - Go to https://vercel.com/dashboard
   - Import GitHub repo
   - Framework: Other
   - Deploy!

3. **Update Backend CORS**
   - Render Dashboard → Your Service → Environment
   - Add: `FRONTEND_URL` = your Vercel URL
   - Redeploy backend

---

## Done! 🎉

Your site is live at your Vercel URL!

