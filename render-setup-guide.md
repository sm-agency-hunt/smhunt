# Render Deployment Guide for SMHUNT
# ===================================

## Step-by-Step Instructions to Create 3 Services on Render:

### 1️⃣ Backend Web Service (FastAPI + Uvicorn)

**Steps:**
1. Go to Render Dashboard → New + → **Web Service**
2. Connect your GitHub repository: `https://github.com/sm-agency-hunt/smhunt`
3. Configure:
   - **Name:** smhunt-backend
   - **Region:** Choose closest to your users
   - **Branch:** main or master
   - **Root Directory:** / (leave blank)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   ```
   DATABASE_URL=<will add after creating database>
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DEBUG=False
   LOG_LEVEL=INFO
   PYTHON_VERSION=3.11.9
   ```
5. Click "Create Web Service"

---

### 2️⃣ PostgreSQL Database

**Steps:**
1. Go to Render Dashboard → New + → **PostgreSQL**
2. Configure:
   - **Name:** smhunt-db
   - **Database Name:** smhunt_prod
   - **User:** smhunt_user
   - **Password:** Generate a strong password
   - **Plan:** Starter (free tier available)
3. After creation, copy the **Internal Database URL**
4. Go back to Backend Web Service settings
5. Add the DATABASE_URL environment variable:
   ```
   DATABASE_URL=postgresql://smhunt_user:YOUR_PASSWORD@db-host:5432/smhunt_prod
   ```

---

### 3️⃣ Frontend Static Site (React)

**Steps:**
1. Go to Render Dashboard → New + → **Static Site**
2. Connect your GitHub repository: `https://github.com/sm-agency-hunt/smhunt`
3. Configure:
   - **Name:** smhunt-frontend
   - **Branch:** main or master
   - **Root Directory:** frontend
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** build
4. Add Environment Variables:
   ```
   REACT_APP_API_URL=<your backend URL from step 1>
   ```
   Example: `REACT_APP_API_URL=https://smhunt-backend.onrender.com`
5. Click "Create Static Site"

---

## 🔗 Connecting Services Together:

### After Creating All 3 Services:

1. **Backend Service** needs:
   - DATABASE_URL from PostgreSQL service
   
2. **Frontend Service** needs:
   - REACT_APP_API_URL pointing to backend URL

3. **Update Backend CORS Settings:**
   - In your backend code, update allowed origins to include frontend URL
   - Example: `https://smhunt-frontend.onrender.com`

---

## 📝 Important Notes:

- **Database Connection:** Use internal database URL for services on same Render account
- **CORS Configuration:** Update backend to allow frontend domain
- **Environment Variables:** Keep all secrets in Render dashboard, not in code
- **Logs:** Monitor logs in Render dashboard for each service
- **Auto-Deploy:** All services will auto-deploy on git push

---

## ✅ Verification Checklist:

- [ ] Backend service is running (check health endpoint)
- [ ] Database is connected (check logs)
- [ ] Frontend is accessible via static site URL
- [ ] Frontend can communicate with backend API
- [ ] All environment variables are set correctly

---

## 🚀 Your Services Will Be:

1. **Backend:** `https://smhunt-backend.onrender.com`
2. **Database:** Internal connection only
3. **Frontend:** `https://smhunt-frontend.onrender.com`
