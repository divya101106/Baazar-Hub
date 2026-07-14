# Environment Variables to Add in Deployment Platform

## 📋 Copy-Paste Ready List

Add these **exact variable names and values** in your deployment platform's "Environment Variables" section:

---

### **1. DJANGO_SECRET_KEY** ⚠️ **REQUIRED**

**NAME_OF_VARIABLE:** `DJANGO_SECRET_KEY`

**value:** Generate a new secret key by running this command locally:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then copy the output and paste it as the value.

**Example value (DO NOT USE THIS - Generate your own):**
```
django-insecure-abc123xyz789def456ghi012jkl345mno678pqr901stu234vwx567yz
```

---

### **2. DEBUG** ⚠️ **REQUIRED**

**NAME_OF_VARIABLE:** `DEBUG`

**value:** `False`

---

### **3. ALLOWED_HOSTS** ⚠️ **REQUIRED**

**NAME_OF_VARIABLE:** `ALLOWED_HOSTS`

**value:** Replace with your actual domain name

**For Render.com:**
```
your-app-name.onrender.com
```

**For Railway.app:**
```
your-app.up.railway.app
```

**For Heroku:**
```
your-app.herokuapp.com
```

**For custom domain:**
```
yourdomain.com,www.yourdomain.com
```

---

### **4. CSRF_TRUSTED_ORIGINS** (Optional - Auto-detected)

**NAME_OF_VARIABLE:** `CSRF_TRUSTED_ORIGINS`

**value:** Your domain with `https://` protocol (OPTIONAL - will be auto-detected from ALLOWED_HOSTS)

**Note:** If you don't set this variable, the system will automatically:
- Detect your domain from `ALLOWED_HOSTS`
- Add both `https://` and `http://` versions
- Auto-detect Render domains from environment variables
- Add any `.onrender.com` domains found in `ALLOWED_HOSTS`

**For Render.com (Optional - Auto-detected):**
```
https://your-app-name.onrender.com
```

**For Railway.app:**
```
https://your-app.up.railway.app
```

**For Heroku:**
```
https://your-app.herokuapp.com
```

**For custom domain:**
```
https://yourdomain.com,https://www.yourdomain.com
```

**⚠️ IMPORTANT:** If you're using Render.com, you can skip setting this variable - it will be auto-detected from `ALLOWED_HOSTS`!

---

### **5. TIME_ZONE** (Optional)

**NAME_OF_VARIABLE:** `TIME_ZONE`

**value:** `UTC` (or your preferred timezone like `Asia/Kolkata`)

---

### **6. DATABASE_URL** (Auto-provided by most platforms)

**NAME_OF_VARIABLE:** `DATABASE_URL`

**value:** Usually **automatically set** by your hosting platform when you add a PostgreSQL database. You don't need to manually add this in most cases.

**If you need to set it manually:**
```
postgresql://username:password@host:port/database_name
```

---

## ✅ Quick Checklist

1. ✅ Generate `DJANGO_SECRET_KEY` using the command above
2. ✅ Set `DEBUG=False`
3. ✅ Set `ALLOWED_HOSTS` to your domain (e.g., `baazar-hub-1.onrender.com`)
4. ⚠️ `CSRF_TRUSTED_ORIGINS` is **OPTIONAL** - will be auto-detected from `ALLOWED_HOSTS`
5. ✅ (Optional) Set `TIME_ZONE` if you want a different timezone
6. ✅ `DATABASE_URL` is usually auto-provided - check your platform's database settings

**For Render.com users:** Just set `ALLOWED_HOSTS` correctly, and CSRF will work automatically!

---

## 🎯 Example for Render.com

If your app URL is `baazar-hub-1.onrender.com` on Render:

**Minimum Required (CSRF auto-detected):**
```
DJANGO_SECRET_KEY=<your-generated-key>
DEBUG=False
ALLOWED_HOSTS=baazar-hub-1.onrender.com
TIME_ZONE=UTC
```

**With explicit CSRF (optional):**
```
DJANGO_SECRET_KEY=<your-generated-key>
DEBUG=False
ALLOWED_HOSTS=baazar-hub-1.onrender.com
CSRF_TRUSTED_ORIGINS=https://baazar-hub-1.onrender.com
TIME_ZONE=UTC
```

**Note:** The `CSRF_TRUSTED_ORIGINS` line is optional - it will be automatically detected from `ALLOWED_HOSTS`!

---

## 🎯 Example for Railway.app

If your app URL is `baazar-hub.up.railway.app`:

```
DJANGO_SECRET_KEY=<your-generated-key>
DEBUG=False
ALLOWED_HOSTS=baazar-hub.up.railway.app
CSRF_TRUSTED_ORIGINS=https://baazar-hub.up.railway.app
TIME_ZONE=UTC
```

---

## ⚠️ Important Notes

1. **Never commit your SECRET_KEY to Git** - Always use environment variables
2. **Always set DEBUG=False in production** - This prevents exposing sensitive error information
3. **DATABASE_URL is usually auto-provided** - Check your platform's database documentation
4. **After adding variables, restart your deployment** - Changes take effect after restart

---

## 🔧 What Was Updated

The `config/settings.py` file has been updated to read from these environment variables. The project is now ready for deployment!


