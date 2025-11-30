#!/usr/bin/env python3
import os
import glob
import logging
import json
from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from tqdm import tqdm
from app import config
from app.database.models import (
    Base,
    Section,
    Subsection,
    ElementTypes,
    Element,
    ElementLinks,
)
from app.parsers import match_title, match_elements, match_subsections, match_exercises, get_subsection_data
from app.database.queries.utils import engine, session_scope

logging.basicConfig(level=logging.INFO)


def init_database(engine: Engine) -> None:
    """
    Initialize the database by creating all tables defined in the ORM models.
    Args:
        engine (Engine): SQLAlchemy Engine instance to connect to the database.
    """
    # Check if tables already exist
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()

    # Create tables if they do not exist
    if not existing_tables:
        logging.info("Creating database tables...")
        Base.metadata.create_all(engine)
        logging.info("Database tables created successfully.")
    else:
        logging.info("Database tables already exist. No action taken.")


def populate_from_json(json_file: str, cls: Base) -> None:
    """
    Populate the database with sections from JSON file
    Args:
        section_list_file (str): Path to the JSON file containing section data.
    """
    # Load sections from JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Insert sections into the database
    count = 0
    logging.info("Populating %s table...", cls.__tablename__.upper())
    with session_scope() as session:
        for element in data:
            if not session.query(cls).filter_by(**element).one_or_none():
                new_element = cls(**element)
                session.add(new_element)
                count += 1
    logging.info(
        "Table %s populated successfully. %d new records added.",
        cls.__tablename__.upper(),
        count,
    )


def add_element(session, number:  int | str, content: str, section_number: int | str=None, subsection_number: int | str=None, subsection_id: int | str=None, type: str=None) -> bool:
    """
    Add a new element to the database.
    Args:
        session: SQLAlchemy session object.
        number (int | str): Element number.
        content (str): Content of the element.
        section_number (int | str): Section number the element belongs to.
        subsection_number (int | str): Subsection number the element belongs to.
        subsection_id (int | str): ID of the subsection the element belongs to.
        type (str): element type.

    Returns:
        bool: True if a new Element was created, False if it already existed.
    """
    # Get subsection_id if not provided
    if subsection_id is None and (section_number is None or subsection_number is None):
        raise ValueError("Either subsection_id or both section_number and subsection_number must be provided.")
    elif subsection_id is None:
        subsection = (
            session.query(Subsection)
            .join(Section)
            .filter(
                Section.number == section_number,
                Subsection.number == subsection_number,
            )
            .one()
        )
        subsection_id = subsection.id
    
    # Get or create element type
    element_type = (
        session.query(ElementTypes)
        .filter_by(name=type)
        .one_or_none()
    )
    if element_type is None:
        logging.warning(
            "Element type %s does not exist. Creating a new one.",
            type,
        )
        element_type = ElementTypes(name=type)
        session.add(element_type)
        session.flush()  # to get element_type.id
    
    # Create element if does not exist
    element = (
        session.query(Element)
        .filter_by(
            subsection_id=subsection_id,
            type_id=element_type.id,
            number=number,
        )
        .one_or_none()
    )
    exists = element is not None
    if not exists:
        element = Element(
            subsection_id=subsection_id,
            type_id=element_type.id,
            number=number,
            content=content,
        )
        session.add(element)
    return not exists



def populate_subsections_and_elements(dirpath: str) -> None:
    """
    Populate the database with subsections and elements.
    Args:
        dirpath (str): Directory containing subsection markdown files.
    """
    # get a list of all subsection files
    path = os.path.join(dirpath, "*.md")
    subsections = glob.glob(path)

    logging.info("Populating subsections and elements into the database...")
    new_element_count = 0
    new_subsection_count = 0
    for file in tqdm(subsections):
        # read subsection file
        with open(file, "r", encoding="utf-8") as f:
            title = f.readline().strip()
            content = f.read()

        # parse elements and title
        title_match = match_title(title)
        element_matches = match_elements(content)

        section_number, subsection_number = map(
            int, title_match.group("number").split(".")
        )
        subsection_title = title_match.group("title").strip()

        # open a session
        with session_scope() as session:
            # get section from DB
            section = session.query(Section).filter_by(number=section_number).one()

            # create subsection if not exists
            subsection = (
                session.query(Subsection)
                .filter_by(section_id=section.id, number=subsection_number)
                .one_or_none()
            )

            if subsection is None:
                subsection = Subsection(
                    section_id=section.id,
                    number=subsection_number,
                    title=subsection_title,
                )
                session.add(subsection)
                session.flush()  # to get subsection.id
                new_subsection_count += 1

            # create elements
            for element_match in element_matches:
                status = add_element(
                    session,
                    number=element_match.group("number").split(".")[-1],
                    content=element_match.group("content").strip(),
                    subsection_id=subsection.id,
                    type=element_match.group("type").lower(),
                )
                if status:
                    new_element_count += 1

    logging.info("Subsections and elements populated successfully.")
    logging.info("New subsections added: %d", new_subsection_count)
    logging.info("New elements added: %d", new_element_count)


def populate_solutions(filepath: str) -> None:
    """
    Populate the database with solutions from a solution mannual file.
    Args:
        filepath (str): Path to the solution mannual file in markdown format
    """
    # read the solution mannual file
    logging.debug("Reading solution mannual from %s", filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        contents = file.read()
    
    # parse solution subsections
    subsection_matches = match_subsections(contents)
    
    # add solutions to the database
    new_solution_count = 0
    logging.info("Populating solutions into the database...")
    with session_scope() as session:
        for subsection_match in subsection_matches:
            subsection_data = get_subsection_data(subsection_match)
            for exercise_match in match_exercises(subsection_data["exercises"]):
                # add solution to the database
                status = add_element(
                    session,
                    number=exercise_match.group("number"),
                    content=exercise_match.group("contents").strip(),
                    section_number=subsection_data["section"],
                    subsection_number=subsection_data["number"],
                    type="solution",
                )
                if status:
                    new_solution_count += 1
    logging.info("Solutions populated successfully. New solutions added: %d", new_solution_count)
    


    


def main() -> None:
    # initialize the database
    init_database(engine)

    # populate tables
    populate_from_json(config.SECTION_LIST, Section)
    populate_from_json(config.ELEMENT_TYPES_LIST, ElementTypes)
    populate_subsections_and_elements(config.SUBSECTION_FILES_DIR)
    populate_solutions(config.SOLUTION_MANNUAL_FILE)


if __name__ == "__main__":
    main()
