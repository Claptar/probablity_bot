from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base


DB_URL = "sqlite:///database.db"
Base = declarative_base()


class Exercise(Base):
    """
    This class represents an exercise table in the database
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    paragraph = Column(String)
    problem_text = Column(String)
    solution_text = Column(String)


def main():
    # create engine
    engine = create_engine(DB_URL)

    # create DB
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
