"A module for database queries"
import logging
from typing import Tuple
from sqlalchemy.sql.expression import func
from app.database.models import Exercise, User
from app.database.quieries.utils import session_scope


def get_random_exercise(
    first_name: str, telegram_id: int, username: str
) -> Tuple[int, str]:
    """
    Retrieve a random exercise from the database.
    Args:
        first_name (str): user's first name
        telegram_id (int): user's telegram_id
        username (str): user's username
    Returns:
        Tuple[int, str]: exercise id and contents
    """
    with session_scope() as session:
        # get user
        user = User.user_by_telegram_id(telegram_id, session)

        if user is None:
            logging.error(
                "User with telegram id %s not found in the database", telegram_id
            )
            user = User.create(
                first_name=first_name,
                telegram_id=telegram_id,
                username=username,
            )

        # Extract the IDs of solved exercises
        solved_exercise_ids = [
            solved_exercise.exercise_id for solved_exercise in user.solved_exercises
        ]

        # get a random exercise that user hasn't solved yet
        exercise = (
            session.query(Exercise)
            .filter(~Exercise.id.in_(solved_exercise_ids))
            .order_by(func.random())
            .first()
        )

        if exercise is None:
            error_message = "No unsolved exercises found for the user"
            logging.error(error_message)
            raise ValueError(error_message)

        return exercise.id, exercise.contents, exercise.paragraph.title
