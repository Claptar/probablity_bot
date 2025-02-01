from app.database.models import Base
from app.database.quieries.utils import engine


def initialize_database():
    Base.metadata.create_all(engine)
