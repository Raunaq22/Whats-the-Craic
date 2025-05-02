<div align="center">
  <a href="https://whats-the-craic.vercel.app" target="_blank">
    <img src="event_management/staticfiles/icon/ms-icon-310x310.png" alt="Event Management System Logo" width="200">
  </a>
  <br>
  <a href="https://whats-the-craic.vercel.app" target="_blank">
    <img src="event_management/staticfiles/icon/wtc-logo.png" alt="WTC Logo" width="200">
  </a>
  <br><br>
  <h3>
    <a href="https://whats-the-craic.vercel.app" target="_blank">☘️ Live Demo</a>
  </h3>
</div>

A Django-based event management system with user authentication, event creation, and ticket booking capabilities.

## Features

- User authentication (email/password and social auth)
- Event creation and management
- Ticket booking and management
- Payment integration with Stripe
- Email notifications
- Responsive design

## Tech Stack

- **Backend**: Django, PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Django-allauth
- **Payments**: Stripe
- **Deployment**: Vercel, Supabase

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd event_management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
   - Install PostgreSQL if not already installed
   - Create a new database:
     ```bash
     createdb event_management
     ```
   - Or use an existing database and update the DATABASE_URL in .env

5. Create a .env file with the following content:
```bash
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DATABASE_URL=postgresql://username:password@localhost:5432/event_management

# Email settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe settings
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# Social auth settings
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_SECRET=your-github-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_SECRET=your-google-secret
```

6. Run migrations and create a superuser:
```bash
python manage.py migrate
python manage.py createsuperuser
```

7. Collect static files and start the development server:
```bash
python manage.py collectstatic
python manage.py runserver
```

The development server will be available at http://localhost:8000

## License

This project is licensed under the MIT License.

## Author 👨‍💻

Raunaq Singh Gandhi 