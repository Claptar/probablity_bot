"Contains the Exercise class that represents an exercise from the book, stored in the database"

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint
from app.database.models.base import Base


class Section(Base):
    __tablename__ = "sections"

    # Attributes
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    # Relationships
    subsections = relationship(
        "Subsection", back_populates="section", uselist=True, cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Section(number={self.number}, title={self.title})"


class Subsection(Base):
    __tablename__ = "subsections"

    # Attributes
    id = Column(Integer, primary_key=True)
    section_id = Column(
        Integer,
        ForeignKey("sections.id"),
        nullable=False,
    )
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    # Relationships
    section = relationship("Section", back_populates="subsections", uselist=False)
    elements = relationship(
        "Element", back_populates="subsection", uselist=True, cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Subsection(number={self.number}, title={self.title})"


class ElementTypes(Base):
    __tablename__ = "element_types"

    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Relationships
    elements = relationship(
        "Element", back_populates="element_type", uselist=True, cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"ElementType(name={self.name})"


class Element(Base):
    __tablename__ = "elements"
    __table_args__ = (
        UniqueConstraint(
            "subsection_id",
            "type_id",
            "number",
            name="_element_subsection_type_number_uc",
        ),
    )

    # Attributes
    id = Column(Integer, primary_key=True)
    subsection_id = Column(
        Integer,
        ForeignKey("subsections.id"),
        nullable=False,
    )
    type_id = Column(
        Integer,
        ForeignKey("element_types.id"),
        nullable=False,
    )
    number = Column(Integer, nullable=False)
    content = Column(String, nullable=False)

    # Relationships
    subsection = relationship("Subsection", back_populates="elements", uselist=False)
    element_type = relationship(
        "ElementTypes", back_populates="elements", uselist=False
    )
    links = relationship(
        "ElementLinks",
        back_populates="source_element",
        uselist=True,
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"Element(type={self.element_type.name}, content={self.content[:30]}...)"


class ElementLinks(Base):
    __tablename__ = "element_links"
    __table_args__ = (
        UniqueConstraint(
            "element_id",
            "linked_element_id",
            name="_element_link_uc",
        ),
    )

    # Attributes
    id = Column(Integer, primary_key=True)
    source_element_id = Column(
        Integer,
        ForeignKey("elements.id"),
        nullable=False,
    )
    target_element_id = Column(
        Integer,
        ForeignKey("elements.id"),
        nullable=False,
    )

    # Relationships
    source_element = relationship(
        "Element",
        foreign_keys=[source_element_id],
        back_populates="links",
        uselist=False,
    )
    target_element = relationship(
        "Element",
        foreign_keys=[target_element_id],
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"ElementLink(source_element_id={self.source_element_id}, target_element_id={self.target_element_id})"
