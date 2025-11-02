# FastAPI Backend with Redis Cache and PostgreSQL

This is a FastAPI backend project with Redis cache and PostgreSQL database, containerized using Docker Compose.

## Features

- FastAPI framework
- PostgreSQL database
- Redis cache
- Docker Compose setup
- Alembic migrations
- Pydantic models
- SQLAlchemy ORM
- CORS middleware
- Environment variables support

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- pip (Python package installer)

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a `.env` file:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/fastapi_db
REDIS_URL=redis://localhost:6379/0
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
alembic upgrade head
```

3. Start the development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
.
├── alembic/                 # Database migrations
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── database.py         # Database and Redis connections
│   ├── models.py           # SQLAlchemy models
│   └── schemas.py          # Pydantic models
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── alembic.ini            # Alembic configuration
└── README.md
```

## Testing

Coming soon...

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.