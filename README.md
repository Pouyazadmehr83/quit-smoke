# QuitSmoke (Quit-Yar) — Minimum Viable Product (MVP)

A platform that helps people quit smoking by focusing on **financial motivation**. Every smoke-free day, the app calculates how much money the user has saved instead of spending on cigarettes, tracks their **streak**, and allows them to set financial goals (such as buying a motorcycle) to stay motivated.

---

# Documentation

| Document               | Description                                                                         |
| ---------------------- | ----------------------------------------------------------------------------------- |
| This README            | Quick project setup using Docker                                                    |
| `docs/ARCHITECTURE.md` | Complete system architecture, database design, design decisions, and future roadmap |
| `docs/API.md`          | Complete API documentation for all endpoints                                        |

---

# Prerequisites

* Docker
* Docker Compose

---

# Quick Start

```bash
# 1. Clone the repository and enter the project directory
cd quitsmoke

# 2. Create the environment file
cp .env.example .env

# 3. Build and start all services
docker compose up --build
```

After the containers are running:

* **Backend API:** http://localhost:8000/api/
* **Swagger API Documentation:** http://localhost:8000/api/docs/
* **Django Admin:** http://localhost:8000/admin/
* **Frontend (React):** http://localhost:3000/

---

# Create an Admin User (Optional)

```bash
docker compose exec backend python manage.py createsuperuser
```

---

# Run Backend Tests

```bash
docker compose exec backend python manage.py test
```

The existing tests cover the core business logic of the application, including:

* Smoke-free streak calculation
* Money saved calculation
* Correct behavior after a relapse

These tests represent the heart of the project and should always remain passing.

---

# Project Structure

```
quitsmoke/
├── docker-compose.yml
├── .env.example
├── backend/                  # Django + Django REST Framework
│   ├── config/               # Project configuration
│   ├── apps/
│   │   ├── users/            # Custom email-based authentication & smoking profile
│   │   ├── tracking/         # Daily check-ins, streak & savings calculation
│   │   ├── goals/            # Financial goals
│   │   ├── leaderboard/      # Streak & savings leaderboards
│   │   └── core/             # Reserved for future features
│   └── requirements.txt
├── frontend/                 # React + Vite
│   └── src/
│       ├── api/              # Axios API client
│       ├── pages/            # Application pages
│       ├── components/       # Shared UI components
│       └── context/          # Authentication context
└── docs/
    ├── ARCHITECTURE.md
    └── API.md
```

---

# Current MVP Features

* ✅ User registration and login (Email + JWT Authentication)
* ✅ Smoking profile setup (brand, cigarette pack price, cigarettes per day)
* ✅ Daily check-in with automatic streak and savings calculation
* ✅ Financial goal tracking with estimated completion date
* ✅ Leaderboards for longest streak and highest savings
* ✅ Clean turquoise & white user interface
* ✅ Auto-generated Swagger API documentation

---

# Planned for Future Versions

The following features were intentionally postponed to keep the MVP focused. The project architecture is already prepared to support them without major refactoring (see `docs/ARCHITECTURE.md`).

* 📋 Daily reminder emails (Celery + SMTP)
* 📋 "What can you buy with your savings?" feature using real-time exchange rates and Iranian market prices

---

# Tech Stack

### Backend

* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication
* drf-spectacular (Swagger/OpenAPI)

### Frontend

* React
* Vite
* Axios
* React Router

### DevOps

* Docker
* Docker Compose

---

# Project Goal

QuitSmoke aims to transform the money normally spent on cigarettes into a visible source of motivation. Instead of simply counting smoke-free days, the platform helps users visualize their financial progress, build healthy habits, and stay committed to quitting through measurable achievements.
