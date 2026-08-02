# Smart Shopping and Price Tracking System — Setup Guide

## 1. Backend Setup (Django + MySQL)

```bash
cd smart_shopping_project

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# copy the env template and fill in real values
cp .env.example .env
```

Edit `.env` with your real MySQL credentials, RapidAPI key, SendGrid key, and Twilio credentials.

Create the MySQL database first (in MySQL shell):
```sql
CREATE DATABASE smart_shopping_db CHARACTER SET utf8mb4;
```

Then run migrations and create an admin user:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Backend now runs at: `http://127.0.0.1:8000/`
Admin panel: `http://127.0.0.1:8000/admin/`

## 2. Background Price-Check Job (Celery)

You need Redis running locally first (e.g. `redis-server`, or Docker: `docker run -p 6379:6379 redis`).

In two separate terminals, from the project root:
```bash
celery -A config worker --loglevel=info
celery -A config beat --loglevel=info
```
This automatically checks tracked product prices every 6 hours (configurable in `config/settings.py` under `CELERY_BEAT_SCHEDULE`) and sends alerts on price drops.

## 3. Frontend Setup (React)

```bash
cd frontend
npm install
npm start
```
Frontend runs at: `http://localhost:3000/` and talks to the Django API at `http://127.0.0.1:8000/api/`.

## 4. Typical First-Run Flow

1. Open `http://localhost:3000/register` → create an account.
2. Log in.
3. Search for a product (e.g. "iPhone 15").
4. Click a product → "Track this product" (optionally set a target price).
5. Add items to your Wishlist.
6. Wait for the Celery job to run (or trigger it manually — see below) to see price-drop alerts appear under Notifications.

## 5. Manually Triggering the Price-Check Job (for testing)

```bash
python manage.py shell
>>> from tracking.tasks import check_prices_job
>>> check_prices_job()
```

## 6. Notes Before Going Live

- Get a real RapidAPI product-search API key and confirm the exact endpoint/response field names — adjust `products/rapidapi_service.py` if your chosen API's fields differ from the example.
- Replace SendGrid/Twilio with your own verified sender email and phone number.
- Set `DEBUG=False` and a real `ALLOWED_HOSTS` list before deploying.
- Never commit your real `.env` file.
