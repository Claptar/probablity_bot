from sqlalchemy.orm import Session
from contextlib import contextmanager


@contextmanager
def session_scope(engine):
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
