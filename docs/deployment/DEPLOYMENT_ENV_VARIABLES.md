# Environment Variables for Deployment - BAAZAR-HUB

## 🔐 Required Environment Variables

### **Critical (Must Set for Production)**

1. **`DJANGO_SECRET_KEY`** ⚠️ **REQUIRED**
   - **Purpose**: Django's secret key for cryptographic signing
   - **Current Value**: Hardcoded in settings.py (INSECURE)
   - **Generate New Key**: 
     ```python
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - **Example**: `django-insecure-yk&pm*cfwk6*ebxatsxx^8s)a4n2+!uu_fq9_1r5*yrqu_o#@3`
   - **Security**: ⚠️ **CRITICAL** - Never commit this to version control

2. **`DEBUG`** ⚠️ **REQUIRED**
   - **Purpose**: Enable/disable debug mode
   - **Production Value**: `False`
   - **Development Value**: `True`
   - **Example**: `False`

3. **`ALLOWED_HOSTS`** ⚠️ **REQUIRED**
   - **Purpose**: List of allowed hostnames for the site
   - **Format**: Comma-separated list
   - **Example**: `yourdomain.com,www.yourdomain.com,baazar-hub.onrender.com`
   - **For Render/Railway**: `your-app-name.onrender.com` or `your-app.up.railway.app`

### **Database Configuration (If using PostgreSQL)**

4. **`DATABASE_URL`** (Recommended) or individual variables:
   - **Format**: `postgresql://user:password@host:port/dbname`
   - **Example**: `postgresql://baazar_user:secure_pass@localhost:5432/baazar_db`
   
   **OR use individual variables:**
   
5. **`DB_NAME`**
   - **Example**: `baazar_production`

6. **`DB_USER`**
   - **Example**: `baazar_user`

7. **`DB_PASSWORD`**
   - **Example**: `your_secure_password_here`

8. **`DB_HOST`**
   - **Example**: `localhost` or `your-db-host.com`

9. **`DB_PORT`**
   - **Example**: `5432`

### **Optional but Recommended**

10. **`TIME_ZONE`**
    - **Default**: `UTC`
    - **Example**: `Asia/Kolkata` or `America/New_York`

11. **`CSRF_TRUSTED_ORIGINS`**
    - **Format**: Comma-separated URLs
    - **Example**: `https://yourdomain.com,https://www.yourdomain.com`

12. **`STATIC_ROOT`** (For production static file serving)
    - **Default**: `BASE_DIR / 'staticfiles'`
    - **Example**: `/app/staticfiles`

13. **`MEDIA_ROOT`** (For production media file storage)
    - **Default**: `BASE_DIR / 'media'`
    - **Example**: `/app/media` or use cloud storage (AWS S3, Cloudinary)

---

## 📝 Example `.env` File (Local Development)

Create a `.env` file in the project root (add to `.gitignore`):

```env
# Django Settings
DJANGO_SECRET_KEY=django-insecure-yk&pm*cfwk6*ebxatsxx^8s)a4n2+!uu_fq9_1r5*yrqu_o#@3
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
# For PostgreSQL in production, use:
# DB_NAME=baazar_production
# DB_USER=baazar_user
# DB_PASSWORD=your_secure_password
# DB_HOST=localhost
# DB_PORT=5432
# Or use DATABASE_URL=postgresql://user:pass@host:port/dbname

# Time Zone
TIME_ZONE=UTC

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

---

## 🚀 Platform-Specific Deployment

### **Render.com**

1. Go to your service → **Environment** tab
2. Add these environment variables:

```
DJANGO_SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://user:pass@host:port/dbname  # Provided by Render
```

**Note**: Render automatically provides `DATABASE_URL` if you add a PostgreSQL database.

### **Railway.app**

1. Go to your project → **Variables** tab
2. Add these environment variables:

```
DJANGO_SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.up.railway.app
DATABASE_URL=postgresql://user:pass@host:port/dbname  # Provided by Railway
```

### **Heroku**

1. Use Heroku CLI:
```bash
heroku config:set DJANGO_SECRET_KEY=your-generated-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
```

2. Or use Heroku Dashboard → Settings → Config Vars

### **DigitalOcean App Platform**

1. Go to App → Settings → App-Level Environment Variables
2. Add:
```
DJANGO_SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.ondigitalocean.app
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### **AWS Elastic Beanstalk**

1. Go to Configuration → Software → Environment Properties
2. Add:
```
DJANGO_SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.elasticbeanstalk.com
```

---

## 🔧 Updating settings.py to Use Environment Variables

You'll need to update `config/settings.py` to read from environment variables. Here's what needs to be changed:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-fallback-key-for-dev-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database
if 'DATABASE_URL' in os.environ:
    # Use PostgreSQL (production)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Use SQLite (development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Time Zone
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000').split(',')
```

**Note**: For `DATABASE_URL` parsing, you'll need to install `dj-database-url`:
```bash
pip install dj-database-url
```

Add to `requirements.txt`:
```
dj-database-url>=2.1.0
```

---

## ✅ Quick Checklist for Deployment

- [ ] Generate a new `DJANGO_SECRET_KEY` (never use the default)
- [ ] Set `DEBUG=False` in production
- [ ] Set `ALLOWED_HOSTS` to your domain(s)
- [ ] Configure PostgreSQL database (if not using SQLite)
- [ ] Set up `DATABASE_URL` or individual DB variables
- [ ] Update `CSRF_TRUSTED_ORIGINS` with your domain
- [ ] Configure static file serving (WhiteNoise or CDN)
- [ ] Set up media file storage (local or cloud)
- [ ] Test all environment variables are loaded correctly
- [ ] Run `python manage.py check --deploy` to verify production readiness

---

## 🛡️ Security Best Practices

1. **Never commit `.env` files** - Add to `.gitignore`
2. **Use different SECRET_KEY for each environment** (dev, staging, production)
3. **Rotate SECRET_KEY periodically** in production
4. **Use environment-specific values** for `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
5. **Enable HTTPS** in production (most platforms do this automatically)
6. **Use strong database passwords** (16+ characters, mixed case, numbers, symbols)

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Django Environment Variables Best Practices](https://docs.djangoproject.com/en/5.2/topics/settings/#using-environment-variables)
- [python-decouple](https://github.com/henriquebastos/python-decouple) - Alternative library for managing environment variables


