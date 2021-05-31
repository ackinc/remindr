# remindr

This will be a monorepo containing 2 sub-packages

## API

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy

## Frontend

- ES2021
- React
- Redux

## Notes

- Every hour, we read all users' calendars and retrieve events happening in the next day. Retrieved events are synced with what's already in the `Events` table

- Every minute, a bg process checks the `Events` table for events starting in the next 10 minutes. For each such event, a reminder is sent

## Side-quests

- configure flake8 and flake8-bugbear
- should I make this a monorepo
- sqlalchemy tutorial
- mypy
- python modules/imports, particularly relative imports
  - to get scripts/reset-db.py script to work, since it imports models.py
- sqlalchemy: table inheritance (for logs table)
