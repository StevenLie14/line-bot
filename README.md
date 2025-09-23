# line-bot

Line Messaging bot used by the R&D team. This repo contains controller, service, repository and model layers. The bot integrates with REQUEST SLC API to reminder and new ticket notification, RESMAN API to fetch assistant/semester data and maps it to Line mentions.

## Repository layout (important folders)
- `app.py` - application entry (main runner)
- `controllers/` - request handlers for Line events
- `services/` - business logic and integrations (resman, user sync)
- `repositories/` - HTTP / persistence repository abstractions
- `models/` - pydantic and ORM models used across the app
- `database/` - database engine & session helpers
- `routes/` - route registry for mapping commands to handlers

## Prerequisites
- Python 3.12
- A PostgreSQL instance
- A Line channel and credentials if you want to run against Line

## Install dependencies
Open PowerShell in the project root and run:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

If you use a conda environment, create/activate it first.

## Required environment variables
Create a `.env` file in the project root or export these in your environment. Values shown are examples.

- DB_HOST=localhost
- DB_PORT=5432
- DB_NAME=linebot_db
- DB_USER=linebot
- DB_PASSWORD=changeme
- SYNC_USER_TOKEN=TOKEN
- SYNC_GROUP_TOKEN=your_sync_token_here
- LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_token
- DATABASE_URL=postgresql://user:pass@host:5432/dbname
