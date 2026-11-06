# Flask Blog

A simple blogging application built with the Python Flask framework and an SQLite database.
Users can create, view, edit, and delete blog posts.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py      # creates database.db with sample posts
flask --app app run    # or: python app.py
```

Then open http://127.0.0.1:5000 (on macOS, if port 5000 is taken by AirPlay, use `flask --app app run --port 5001`).

## Routes

| Route | Method | Purpose |
|---|---|---|
| `/` | GET | List all posts |
| `/create/` | GET, POST | Create a new post |
| `/<id>/` | GET | View a single post |
| `/<id>/edit/` | GET, POST | Edit a post |
| `/<id>/delete/` | POST | Delete a post |
