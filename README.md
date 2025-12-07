# 🛒 BAAZAR-HUB


A modern, secure, and feature-rich classifieds marketplace built with Django.  
Buy, sell, chat, negotiate, and manage transactions effortlessly.

![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)

---

## 🔗 Demo Link
🚀 **Live Demo:** *[BAAZAR-HUB*](https://baazar-hub-3.onrender.com)  

A modern, secure, and feature-rich classifieds marketplace platform built with Django. BAAZAR-HUB enables users to buy and sell items locally with built-in moderation, real-time chat, offer management, and dispute resolution.

![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.14+-red?style=flat&logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)


---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Project Status](#project-status)


- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)


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

### 🏪 Core Marketplace Features

- **Listing Management**
  - Create, edit, and manage product listings
  - Multiple image uploads (up to 5 images per listing)
  - Category-based organization
  - Price and description management
  - Listing status workflow (Pending → Approved/Rejected)

- **Advanced Search & Discovery**
  - Keyword-based search
  - Category filtering
  - Price range filtering
  - Saved searches with automatic alerts
  - Category browsing

- **Offer System**
  - Make offers on listings
  - Accept/Reject offers
  - Offer history tracking
  - Privacy restrictions (users only see their own offers)

- **Shopping Cart & Buy Now**
  - Add/remove items from cart
  - Cart persistence across sessions
  - Instant "Buy Now" feature
  - Direct checkout flow

### 💬 Communication Features

- **Real-time Chat**
  - Direct messaging between buyers and sellers
  - Offer-linked conversations
  - Message history and timestamps
  - Secure message storage

- **Notification System**
  - Real-time notifications for offers, messages, and listings
  - Notification badge on profile icon
  - Hover preview of notifications
  - Mark as read functionality

### ⭐ Rating & Reputation

- **Transaction-based Ratings**
  - 5-star rating system with optional comments
  - Only users involved in completed transactions can rate
  - Average rating calculation
  - Rating history display

### 🛡️ Safety & Moderation

- **Automatic Moderation**
  - Spam detection algorithms
  - Image safety validation
  - Text heuristics
  - Automatic flagging

- **Manual Moderation**
  - Admin review queue
  - Approve/Reject functionality
  - Moderation dashboard
  - User flagging system

### ⚖️ Dispute Resolution

- **Dispute Management**
  - Submit disputes for transactions
  - Admin review and resolution
  - Dispute history tracking
  - Privacy restrictions

### 💳 Payment Integration

- **Dummy Payment Gateway**
  - UPI payment simulation
  - Transaction tracking
  - Payment status management
  - Test credentials: `pay@paytm` / `1234`

### 👤 User Management

- **User Profiles**
  - Edit profile functionality
  - View listings, offers, ratings, and disputes
  - Profile statistics
  - User reputation display

- **Authentication**
  - Secure login/logout
  - User registration
  - Session management
  - Admin session preservation

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.2.8
- **API**: Django REST Framework (DRF) 3.14+
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django Built-in Authentication System
- **Image Processing**: Pillow 10.0+

### Frontend
- **HTML5/CSS3**: Modern, responsive design
- **JavaScript**: Vanilla JS for dynamic interactions
- **Templates**: Django Template Engine

### Architecture
- **Pattern**: Django MTV (Model-Template-View) + Service Layer
- **API Design**: RESTful architecture
- **Middleware**: Custom session preservation middleware

### Deployment
- **Static Files**: WhiteNoise
- **Database URL Parsing**: dj-database-url
- **Production Ready**: Environment variable configuration


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
