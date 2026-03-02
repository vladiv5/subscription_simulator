# Subscription Simulator Backend

I built this project to deepen my understanding of Django and to simulate a real-world, production-ready backend structure. It serves as a practical exploration of scalable architecture, secure API design, and automated deployment, marking my transition from previous environments into the Python and Django ecosystem.

## Tech Stack
* **Framework:** Python, Django, Django REST Framework
* **Database:** PostgreSQL for local and production, SQLite for automated CI/CD testing
* **Authentication:** JSON Web Tokens (JWT) for APIs, Session Auth for the Web UI
* **CI/CD:** GitHub Actions
* **Frontend:** HTML and Bootstrap 5 for the simulator UI

## Features Implemented

### 1. Core Architecture and Role-Based Access Control
I designed a one-to-one relational database schema linking users to their subscription tiers (FREE or PREMIUM). To ensure accountability, every upgrade or cancellation generates an immutable PaymentTransaction record to track financial history. 

I also implemented a role-based UI: Admins have a dedicated control panel to search the database and force upgrades or downgrades on any user, while regular users get a secure, self-service dashboard to manage only their own subscriptions.

### 2. API and Third-Party Webhooks
I created a dedicated endpoint (`/api/subscriptions/webhook/payment/`) to simulate receiving asynchronous events from an external payment provider, like Stripe.

### 3. Security
The webhook endpoint is strictly secured using Bearer tokens. Unauthenticated requests are rejected with a 401 Unauthorized status. I also used dynamic database configuration to ensure credentials are kept safe and out of version control.

### 4. Observability
To monitor performance, I implemented a custom RequestTimingMiddleware. It intercepts every HTTP request, calculates the exact execution time in milliseconds, and logs it to the console for real-time tracking.

### 5. DevOps and CI/CD
I wrote automated unit tests to verify the security of the webhook endpoints. Furthermore, I configured a GitHub Actions pipeline that spins up an Ubuntu server, installs dependencies, dynamically switches to an in-memory SQLite database, and runs the test suite on every push to the main branch.

## Local Setup

If you want to run my code locally, here is how you can set it up.

### Step 1: Clone the repository
```bash
git clone https://github.com/vladiv5/subscription_simulator_backend.git
cd subscription_simulator_backend
```

### Step 2: Set up the virtual environment
I create my isolated Python environment by running:
```bash
python -m venv venv
```

On Windows, I activate it using:
```bash
.\venv\Scripts\activate
```

On macOS or Linux, I activate it using:
```bash
source venv/bin/activate
```

### Step 3: Install dependencies
I install all required packages for the project to run:
```bash
pip install -r requirements.txt
```

### Step 4: Database Configuration
By default, the project expects a local PostgreSQL database named `subscriptions_simulator_db` with the user `postgres`. Ensure your `core/settings.py` matches your local Postgres credentials. Then, I apply the database migrations to build the tables:
```bash
python manage.py migrate
```

### Step 5: Create an Admin and Run the Server
I create a superuser account to access the Admin Control Panel:
```bash
python manage.py createsuperuser
```

Then, I start the development server:
```bash
python manage.py runserver
```

### Step 6: Useful Endpoints
Once the server is running, you can check the Simulator Dashboard at `http://127.0.0.1:8000/api/subscriptions/` or access the Django Admin at `http://127.0.0.1:8000/admin/`.
