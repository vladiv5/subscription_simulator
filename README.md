# Smartheads Subscription Simulator (Backend)

I built this REST API to understand how backend systems power subscriptions, authentication, and core consumer product flows. This project serves as a practical exploration of scalable backend architecture, transitioning from my previous experience with Spring Boot to the Python/Django ecosystem.

## Tech Stack
* **Framework:** Python, Django, Django REST Framework
* **Database:** PostgreSQL
* **Architecture:** MVC (Model-View-Controller) adapted to Django's MTV (Model-Template-View) with a focus on API-first design.

## Features Implemented
* **User & Subscription Modeling:** I designed a 1-to-1 relational database schema to link users to their subscription tiers (FREE/PREMIUM).
* **Admin Dashboard:** I integrated Django's automated admin panel for real-time CRUD operations on user subscriptions.
* **REST API Endpoints:** I built serialization logic to expose subscription statuses securely via JSON.

## Local Setup

If you want to run my code locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/vladiv5/subscription_simulator_backend.git](https://github.com/vladiv5/subscription_simulator_backend.git)
   cd subscription_simulator_backend
   ```
2. **Set up the virtual environment:**
  ```bash
  # I create and activate my isolated Python environment
  python -m venv venv
  source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
  ```
