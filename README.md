# Event Management System

A Django-based event management system with user authentication, event creation, and ticket booking capabilities.

## Features

- User authentication (email/password and social auth)
- Event creation and management
- Ticket booking and management
- Payment integration with Stripe
- Email notifications
- Responsive design

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

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

5. Create a .env file:
```bash
cp .env.example .env
```
Edit the .env file with your configuration:
- Set your SECRET_KEY
- Update DATABASE_URL with your PostgreSQL credentials
- Configure email settings
- Add Stripe and social auth credentials

6. Run migrations:
```bash
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Collect static files:
```bash
python manage.py collectstatic
```

9. Run the development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to see the application.

## Deployment

This application is configured for deployment on Vercel with PostgreSQL on Supabase:

1. Create a Supabase account and project
2. Get your PostgreSQL connection string from Supabase
3. Set up environment variables on Vercel
4. Deploy to Vercel using their CLI or GitHub integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 