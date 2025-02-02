from app.database.models import Exercise, SolvedExercise, User
from app.database.quieries.utils import session_scope
from sqlalchemy.sql.expression import func
from typing import Tuple


def get_random_exercise(telegram_id: int) -> Tuple[int, str]:
    """
    Retrieve a random exercise from the database.
    Args:
        telegram_id (int): user's telegram_id
    Returns:
        Tuple[int, str]: exercise id and contents
    """
    with session_scope() as session:
        # get user
        user = session.query(User).filter_by(telegram_id=telegram_id).one_or_none()

        # get a random exercise that user hasn't solved yet
        exercise = (
            session.query(Exercise)
            .filter(~Exercise.id.in_(user.solved_exercises))
            .order_by(func.random())
            .first()
        )
        return exercise.id, exercise.contents, exercise.paragraph.title
