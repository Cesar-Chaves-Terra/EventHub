# EventHub

A REST API for managing events, organizers, participants, and registrations, developed with Django and Django REST Framework.

## Features

- Event and organizer management.
- Participant registration and management.
- Event registration management.
- Many-to-many relationship between events and participants through the `Registration` model.
- Automatic event seat availability management using Django Signals.
- JWT-based authentication.
- CRUD operations through Django REST Framework ViewSets and routers.
- Custom database managers and aggregate queries.
- Django Admin integration.

## Technologies

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite

## Project Structure

```text
EventHub/
├── config/
├── events/
│   ├── migrations/
│   ├── admin.py
│   ├── managers.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── participants/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```

## Requirements

- Python installed.
- Git installed.
- Access to the project repository.

## Installation

### 1. Clone the repository

```powershell
git clone <REPOSITORY_URL>
cd EventHub
```

Replace `<REPOSITORY_URL>` with the actual GitHub repository URL.

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Apply database migrations

```powershell
python manage.py migrate
```

### 6. Create an administrator account

```powershell
python manage.py createsuperuser
```

### 7. Start the development server

```powershell
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

The Django administration panel will be available at:

`http://127.0.0.1:8000/admin/`

## Data Models

### Event

Represents an event and stores information such as its name, description, date, capacity, available seats, and organizer.

### OrganizerProfile

Connects a Django user to an organizer profile through a one-to-one relationship.

### Participant

Represents a person who can register for events.

### Registration

Connects a participant to an event and stores the registration date and status.

Registration statuses:

- `ACTIVE`: The registration is active.
- `CANCELLED`: The registration has been cancelled.

## Django Signals

The project uses Django Signals to automatically maintain event seat availability when registrations change.

The signal handlers in `participants/signals.py` implement the following behaviors:

- **Active registration created:** decreases the number of available seats by one.
- **Active registration cancelled:** restores one available seat.
- **Cancelled registration reactivated:** decreases the number of available seats by one.
- **Active registration deleted:** restores one available seat.

The signal handlers are registered through the `ParticipantsConfig.ready()` method in `participants/apps.py`.

Database expressions and atomic transactions are used to help maintain consistency when updating available seats.

## JWT Authentication

The API uses JSON Web Tokens (JWT) to authenticate protected requests.

The authentication workflow is:

1. Submit user credentials to the token obtain endpoint.
2. Receive the access and refresh tokens.
3. Include the access token in authenticated requests.

Send the access token using the following HTTP header:

```http
Authorization: Bearer <ACCESS_TOKEN>
```

The exact token obtain and refresh endpoints are defined in the project's URL configuration.

## API Endpoints

API endpoints are configured through Django URL configurations and Django REST Framework routers.

The events endpoint is available at:

`http://127.0.0.1:8000/api/events/`

Other endpoints, including participants, registrations, and JWT authentication, are defined in the project's URL configuration.

## Running Tests

Check the Django project configuration:

```powershell
python manage.py check
```

Display migration status:

```powershell
python manage.py showmigrations
```

Apply pending migrations:

```powershell
python manage.py migrate
```

Run automated tests:

```powershell
python manage.py test
```

## Database

The default configuration uses SQLite. The local database is stored in `db.sqlite3`.

Django migrations are used to create and update the database schema.

## Academic Project

EventHub was developed as an academic project to practice REST API development, data modeling, model relationships, authentication, CRUD operations, database aggregation, and business rule automation using Django Signals.
