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
from app.parsers.elements import parse_title, parse_elements
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
        title_match = parse_title(title)
        element_matches = parse_elements(content)

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
                # get or create element type
                element_type = (
                    session.query(ElementTypes)
                    .filter_by(name=element_match.group("type"))
                    .one_or_none()
                )
                if element_type is None:
                    logging.warning(
                        "Element type %s does not exist. Creating a new one.",
                        element_match.group("type"),
                    )
                    element_type = ElementTypes(name=element_match.group("type"))
                    session.add(element_type)
                    session.flush()  # to get element_type.id

                # create element if not exists
                element = (
                    session.query(Element)
                    .filter_by(
                        subsection_id=subsection.id,
                        type_id=element_type.id,
                        number=element_match.group("number").split(".")[-1],
                    )
                    .one_or_none()
                )

                if element is None:
                    element = Element(
                        subsection_id=subsection.id,
                        type_id=element_type.id,
                        number=element_match.group("number").split(".")[-1],
                        content=element_match.group("content").strip(),
                    )
                    session.add(element)
                    new_element_count += 1

    logging.info("Subsections and elements populated successfully.")
    logging.info("New subsections added: %d", new_subsection_count)
    logging.info("New elements added: %d", new_element_count)


def main() -> None:
    # initialize the database
    init_database(engine)

    # populate tables
    populate_from_json(config.SECTION_LIST, Section)
    populate_from_json(config.ELEMENT_TYPES_LIST, ElementTypes)
    populate_subsections_and_elements(config.SUBSECTION_FILES_DIR)


if __name__ == "__main__":
    main()
