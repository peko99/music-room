# Copyright 2021 Group 21 @ PI (120)


from api.core.database.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
