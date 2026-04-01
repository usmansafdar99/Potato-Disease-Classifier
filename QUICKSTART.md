# Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)
```bash
cd d:\Potato
pip install -r requirements.txt
```

### Step 2: Start Backend (30 seconds)
```bash
cd backend
python main.py
```
✅ Wait for: `Uvicorn running on http://0.0.0.0:8000`

### Step 3: Open Frontend (30 seconds)
**Option A: Direct file**
- Open: `file:///d:/Potato/frontend/index.html`

**Option B: Via HTTP Server**
```bash
cd frontend
python -m http.server 8080
# Then open: http://localhost:8080
```

### Step 4: Test System (2 minutes)
1. Upload a potato leaf image
2. Click "Analyze Image"
3. See results and recommendations

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| Frontend | `file:///d:/Potato/frontend/index.html` or `http://localhost:8080` |
| Backend | `http://localhost:8000` |
| API Docs | `http://localhost:8000/docs` |
| Health Check | `http://localhost:8000/health` |

## 🛠️ Console Commands for Testing

```bash
# Health check
curl http://localhost:8000/health

# Get model info
curl http://localhost:8000/api/v1/model/info

# List available endpoints
curl http://localhost:8000/docs
```

## 📦 Project Structure at a Glance

```
Potato/
├── 1/                    ← Pre-trained model
├── backend/              ← FastAPI server
│   └── main.py          ← Start here
├── frontend/             ← Web interface
│   └── index.html       ← Open this
└── requirements.txt      ← Dependencies
```

## ⚡ Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | Edit `backend/main.py` port or stop other service |
| "Module not found" errors | Run `pip install -r requirements.txt` again |
| Frontend can't reach backend | Ensure backend is running on `http://localhost:8000` |
| Model not loading | Verify `1/` folder exists with model files |

## 📊 Testing with Sample Data

1. Create a test image folder or use existing potato leaf images
2. Upload through the UI
3. Check `/docs` for API testing interface

## 🔐 Production Deployment

For production use:
```bash
# Backend
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Frontend
# Serve via nginx or Apache with proper caching headers
```

## 📚 Full Documentation

- [Main README](README.md)
- [Backend Structure](backend/BACKEND_STRUCTURE.md)
- [Frontend Details](frontend/FRONTEND_README.md)
- [API Docs](http://localhost:8000/docs)

---

**Need help?** Check the main README.md file or review the error logs in console output.
