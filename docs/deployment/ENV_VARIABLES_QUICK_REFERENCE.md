# Environment Variables for Deployment - Quick Reference

## 🔐 Required Environment Variables to Add

Add these variables in your deployment platform's "Environment Variables" section:

### **1. DJANGO_SECRET_KEY** ⚠️ **CRITICAL - REQUIRED**

**Variable Name:** `DJANGO_SECRET_KEY`

**Variable Value:** Generate a new secret key using:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Example Value:**
```
django-insecure-abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567yz
```

**⚠️ IMPORTANT:** Never use the default key from settings.py in production!

---

### **2. DEBUG** ⚠️ **REQUIRED**

**Variable Name:** `DEBUG`

**Variable Value:** `False`

**Note:** Must be `False` for production. Set to `True` only for development.

---

### **3. ALLOWED_HOSTS** ⚠️ **REQUIRED**

**Variable Name:** `ALLOWED_HOSTS`

**Variable Value:** Your domain name(s), comma-separated

**Examples:**
- For Render: `your-app-name.onrender.com`
- For Railway: `your-app.up.railway.app`
- For Heroku: `your-app.herokuapp.com`
- For custom domain: `yourdomain.com,www.yourdomain.com`

**Example Value:**
```
baazar-hub.onrender.com
```

---

### **4. DATABASE_URL** (If using PostgreSQL - Recommended for Production)

**Variable Name:** `DATABASE_URL`

**Variable Value:** Provided by your hosting platform or your PostgreSQL connection string

**Format:** `postgresql://username:password@host:port/database_name`

**Example Value:**
```
postgresql://baazar_user:secure_password@dpg-xxxxx-a.oregon-postgres.render.com:5432/baazar_db
```

**Note:** Most platforms (Render, Railway, Heroku) automatically provide this when you add a PostgreSQL database.

---

### **5. CSRF_TRUSTED_ORIGINS** (Recommended)

**Variable Name:** `CSRF_TRUSTED_ORIGINS`

**Variable Value:** Your domain URL(s), comma-separated, with `https://` or `http://`

**Example Value:**
```
https://baazar-hub.onrender.com,https://www.yourdomain.com
```

---

### **6. TIME_ZONE** (Optional)

**Variable Name:** `TIME_ZONE`

**Variable Value:** Your preferred timezone

**Example Values:**
- `UTC` (default)
- `Asia/Kolkata`
- `America/New_York`
- `Europe/London`

---

## 📋 Quick Copy-Paste List

Here's a formatted list you can use:

```
DJANGO_SECRET_KEY=<generate-new-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app-name.onrender.com
TIME_ZONE=UTC
```

**Note:** `DATABASE_URL` is usually auto-provided by the platform when you add a PostgreSQL database.

---

## 🚀 Platform-Specific Notes

### **Render.com**
- `DATABASE_URL` is automatically set when you add a PostgreSQL database
- `ALLOWED_HOSTS` should be: `your-app-name.onrender.com`

### **Railway.app**
- `DATABASE_URL` is automatically set when you add a PostgreSQL database
- `ALLOWED_HOSTS` should be: `your-app.up.railway.app`

### **Heroku**
- `DATABASE_URL` is automatically set when you add a Heroku Postgres addon
- `ALLOWED_HOSTS` should be: `your-app.herokuapp.com`

---

## ⚠️ Important: Update settings.py First

Before deploying, you need to update `config/settings.py` to read these environment variables. The current settings.py has hardcoded values that won't work in production.

**See:** `DEPLOYMENT_ENV_VARIABLES.md` for instructions on updating settings.py


