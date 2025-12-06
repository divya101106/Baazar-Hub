# 🛒 BAAZAR-HUB

A modern, secure, and feature-rich classifieds marketplace built with Django.  
Buy, sell, chat, negotiate, and manage transactions effortlessly.

![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)

---

## 🔗 Demo Link
🚀 **Live Demo:** *[BAAZAR-HUB*](https://baazar-hub-1.onrender.com)  

---

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Project Status](#project-status)

---

## ✨ Features

### 🏪 Marketplace
- Create, edit, delete listings  
- Upload up to 5 images  
- Category-based browsing and filters  
- Search by keywords, categories, and price range  
- Saved searches + automatic alerts  

### 💬 Communication
- Real-time chat between buyers & sellers  
- Offer-based conversations  
- Timestamped message history  

### 💸 Offers & Transactions
- Make/Accept/Reject offers  
- Offer history  
- “Buy Now” + shopping cart system  
- Dummy UPI-based payment simulation  

### ⭐ Ratings & Profiles
- Rate users after completed transactions  
- 5-star rating with comments  
- Profile stats, listings, offers, and disputes view  

### 🛡 Moderation & Safety
- Auto spam/image/text detection  
- Admin approval queue  
- Manual moderation dashboard  
- User flagging  

### ⚖ Dispute Management
- File disputes  
- Admin review  
- Resolution tracking  

### 🔔 Notifications
- Real-time notifications for offers, messages, approvals  
- Badge & preview dropdown  
- Mark as read  

---

## 🛠 Tech Stack

### Backend
- Django 5.2.8  
- Django REST Framework (DRF)  
- SQLite / PostgreSQL  
- Pillow for images  

### Frontend
- HTML, CSS, JavaScript  
- Django Templates  

### Architecture
- Django MTV pattern  
- REST API  
- Service Layer Architecture  

---

## 🚀 Installation

### 1. Clone Repo
```bash
git clone <(https://github.com/divya101106/Baazar-Hub.git)>
cd BAAZAR-HUB
```
### 2. python -m venv venv
```bash
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```
### 3. Install dependencies 
```bash
pip install -r requirements.txt
```
### 4. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Run Server
```bash
python manage.py runserver
```

## 📖 Usage

### **For Users**
- Register/Login  
- Browse/search listings  
- Create listings  
- Make offers, chat with sellers  
- Add to cart or Buy Now  
- Make dummy UPI payment  
- Rate seller after completion  

### **For Admins**
- `/admin/` dashboard  
- Review & approve listings  
- Manage disputes, users, and moderation queue  

---

## 📁 Project Structure



## 📁 Project Structure
```markdown
- BAAZAR-HUB/
  - config/ — Core settings & project config  
  - users/ — Auth, profiles, ratings  
  - listings/ — Listings & images  
  - offers/ — Offer system + API  
  - chat/ — Messaging system  
  - cart/ — Shopping cart  
  - payments/ — Dummy payment gateway  
  - ratings/ — Rating system  
  - disputes/ — Dispute resolution  
  - moderation/ — Moderation tools  
  - search/ — Search + saved alerts  
  - notifications/ — Notification system  
  - services/ — Business logic layer  
  - templates/ — Global templates  
  - static/ — CSS, JS  
  - media/ — User uploaded files 
```


---

## 📚 API Documentation

**Base URL:** `/api/`

| Feature | Endpoint |
|--------|----------|
| Listings | `/api/listings/` |
| Offers | `/api/offers/` |
| Messages | `/api/messages/` |
| Ratings | `/api/ratings/` |
| Notifications | `/api/notifications/` |

---

## 🎯 Project Status

**Version:** 1.0.0  
**Status:** ✔ Production Ready  

### ✔ Completed
- Listings  
- Offers  
- Chat  
- Cart & Buy Now  
- Ratings  
- Notifications  
- Moderation  
- Disputes  
- Payment Simulation  

### 🚀 Future Plans
- Real payment gateway  
- Email alerts  
- Analytics dashboard  
- Mobile-app-ready API  
- Image compression  
- Rate limiting  
