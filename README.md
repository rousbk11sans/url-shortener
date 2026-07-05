# URL Shortener API

A RESTful URL shortening service built with **FastAPI**, **SQLAlchemy**, and **SQLite**. Given a long URL, it generates a short, unique code that redirects to the original link — similar to how bit.ly works — while tracking click analytics.

## Features

- Shorten any valid URL into a random 6-character code
- Redirect from the short code to the original URL
- Track click counts per short URL
- View stats (original URL, click count, timestamps) for any short code
- Delete a short URL
- Auto-generated interactive API docs (Swagger UI) via FastAPI

## Tech Stack

- **FastAPI** – web framework for building the API
- **Uvicorn** – ASGI server that runs the FastAPI app
- **SQLAlchemy** – ORM for talking to the database
- **SQLite** – lightweight file-based database
- **Pydantic** – request/response data validation

## Project Structure

```
url-shortener/
│
├── app/
│   ├── main.py        # API endpoints, wires everything together
│   ├── database.py     # Database connection setup
│   ├── models.py        # SQLAlchemy table definition (URL)
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── crud.py           # Database logic (create, read, update, delete)
│   └── utils.py            # Short code generator
│
├── requirements.txt
└── README.md
```

## Setup & Installation

1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/YOUR_USERNAME/url-shortener.git
   cd url-shortener
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open the interactive API docs in your browser:
   ```
   http://127.0.0.1:8000/docs
   ```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/shorten` | Create a short URL from a given long URL |
| `GET` | `/{code}` | Redirect to the original URL, increments click count |
| `GET` | `/stats/{code}` | Get stats (original URL, clicks, timestamps) for a code |
| `DELETE` | `/{code}` | Delete a short URL |

### Example: Create a short URL

**Request**
```json
POST /shorten
{
  "url": "https://google.com"
}
```

**Response**
```json
{
  "short_url": "http://localhost:8000/Ab21Xz"
}
```

### Example: Get stats

**Request**
```
GET /stats/Ab21Xz
```

**Response**
```json
{
  "original_url": "https://google.com",
  "short_code": "Ab21Xz",
  "clicks": 3,
  "created_at": "2026-07-05T11:55:31",
  "expires_at": null
}
```

## How It Works

1. A client sends a request (browser, curl, or Postman) to Uvicorn, the ASGI server.
2. Uvicorn passes the request to FastAPI, which matches it to the correct endpoint function in `main.py`.
3. Pydantic validates the incoming/outgoing data shape (`schemas.py`).
4. The endpoint calls into `crud.py`, which contains the actual database logic.
5. For new URLs, `utils.py` generates a random short code and checks it's unique.
6. SQLAlchemy (`models.py`, `database.py`) translates Python objects into SQL and reads/writes the SQLite file.
7. The result is formatted back into JSON and returned to the client.

## Future Improvements

- JWT authentication
- PostgreSQL support
- Docker containerization
- Automated tests (Pytest)
- Custom short-code aliases
- URL expiration enforcement
- Redis caching for high-traffic redirects
- Rate limiting

## License

This project is for educational/portfolio purposes.
