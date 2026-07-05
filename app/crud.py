from sqlalchemy.orm import Session
from datetime import datetime
from . import models, utils


def get_url_by_code(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()


def create_short_url(db: Session, original_url: str, expires_at=None):
    code = utils.generate_short_code()
    while get_url_by_code(db, code) is not None:
        code = utils.generate_short_code()

    db_url = models.URL(
        original_url=original_url,
        short_code=code,
        expires_at=expires_at,
    )

    db.add(db_url)      
    db.commit()          
    db.refresh(db_url)   

    return db_url


def increment_clicks(db: Session, db_url):
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def delete_url(db: Session, db_url):
    db.delete(db_url)
    db.commit()


def is_expired(db_url) -> bool:
    if db_url.expires_at is None:
        return False
    return datetime.utcnow() > db_url.expires_at.replace(tzinfo=None)