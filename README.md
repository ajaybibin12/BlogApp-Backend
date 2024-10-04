# BlogApp Backend

# Project Overview
The BlogApp backend provides a REST API for the frontend to interact with. It handles user authentication, blog creation, editing, deletion, and retrieval. The backend is built using Python with the Flask framework, and the database is PostgreSQL.

The backend is responsible for handling requests from the frontend, performing database operations, and ensuring the security of the application with user authentication and role-based access control.

## Tech Stack
- Python: Programming language.
- Flask: Web framework for building the API.
- PostgreSQL: Relational database for storing blog data.
- SQLAlchemy: ORM for database management.
- Docker: Containerization for easy deployment and scalability.
- Render: Deployed live on Render.

## Setup and Installation
- Prerequisites
- Python (version 3.8 or higher)
- PostgreSQL
- Docker (optional but recommended)
- Installation Steps


## Clone the repository:
```bash

git clone https://github.com/yourusername/BlogApp-Backend.git
```
## Navigate to the project directory:

```bash

cd BlogApp-Backend
```

## Set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
## Install dependencies:

```bash
pip install -r requirements.txt
Configure environment variables:
```

### Create a .env file in the root directory with the following content:
makefile
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/blogapp


### Initialize the database:

```bash
flask db upgrade
Run the Flask development server:
```

```bash
flask run
Running with Docker
Build the Docker image:
```

```bash

docker build -t blogapp-backend .
Start the container using Docker Compose:
```

```bash
docker-compose up
```


# H1 Heading (Deployment)
The backend is deployed on Render. You can access the live API at: https://your-render-backend-link.com
