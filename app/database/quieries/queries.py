from app.database.models import Exercise
from app.database.quieries.utils import session_scope
from sqlalchemy.sql.expression import func


def get_random_exercise():
    """
    Retrieve a random exercise from the database.
    """
    with session_scope() as session:
        random_exercise = session.query(Exercise).order_by(func.random()).first()
        return random_exercise
