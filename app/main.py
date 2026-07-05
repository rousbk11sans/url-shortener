from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse

from . import models, schemas, crud
from .database import engine, SessionLocal 


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(request: schemas.URLCreate, db: Session = Depends(get_db)):
    db_url = crud.create_short_url(db, original_url=str(request.url))
    return {"short_url": f"http://localhost:8000/{db_url.short_code}"}


@app.get("/{code}")
def redirect_to_url(code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, code)

    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if crud.is_expired(db_url):
        raise HTTPException(status_code=410, detail="This short URL has expired")

    crud.increment_clicks(db, db_url)
    return RedirectResponse(url=db_url.original_url)


@app.get("/stats/{code}", response_model=schemas.URLStats)
def get_stats(code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, code)

    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return db_url


@app.delete("/{code}")
def delete_url(code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, code)

    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    crud.delete_url(db, db_url)
    return {"detail": "Short URL deleted successfully"}