from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging
from app import config
from sqlalchemy import create_engine
import os

logger = logging.getLogger(__name__)

# Create the engine
engine = create_engine(config.DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        logger.exception("An error occurred during the session")
        session.rollback()
        raise
    finally:
        session.close()
