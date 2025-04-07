from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, validates
from sqlalchemy.orm.session import Session as SessionType
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any, Type

Base = declarative_base()
engine = create_engine(
    'sqlite:///movies.db',
    connect_args={
        'check_same_thread': False
    }
)
ModelBase: Type[Any] = Base

# Define tables

class Film(ModelBase):
    """
    Represents a film in the database.

    Attributes:
        id (int): The unique identifier for the film.
        title (str): The title of the film.
        year_of_creation (int): The year the film was created.
    """
    __tablename__ = 'films'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    year_of_creation: Mapped[int] = mapped_column(nullable=False)

    crew: Mapped[list["FilmCrew"]] = relationship(
        'FilmCrew',
        back_populates='film',
        cascade='all, delete'
    )

    @validates('year_of_creation')
    def validate_year(self, key: str, value: int) -> int:
        if int(value) < 1888:
            raise ValueError("Year must be 1888 or later")
        return value


class Person(ModelBase):
    """
    Represents a person in the database.

    Attributes:
        id (int): The unique identifier for the person.
        name (str): The name of the person.
        email (str): The email of the person.
    """
    __tablename__ = 'persons'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)

    crew: Mapped[list["FilmCrew"]] = relationship('FilmCrew', back_populates='person')


class Role(ModelBase):
    """
    Represents a role in the database.

    Attributes:
        id (int): The unique identifier for the role.
        role_name (str): The name of the role.
    """
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False)

    crew: Mapped[list["FilmCrew"]] = relationship('FilmCrew', back_populates='role')


class FilmCrew(ModelBase):
    """
    Represents the relationship between the film and the crew in the database.

    Attributes:
        id (int): The unique identifier for the relationship.
        film_id (int): The foreign key of the film table.
        person_id (int): The foreign key of the person table.
        role_id (int): The foreign key of the role table.
    """
    __tablename__ = 'film_crew'
    id: Mapped[int] = mapped_column(primary_key=True)
    film_id: Mapped[int] = mapped_column(
        ForeignKey('films.id', ondelete='CASCADE'),
        nullable=False
    )
    person_id: Mapped[int] = mapped_column(ForeignKey('persons.id'), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), nullable=False)

    film: Mapped["Film"] = relationship('Film', back_populates='crew')
    person: Mapped["Person"] = relationship('Person', back_populates='crew')
    role: Mapped["Role"] = relationship('Role', back_populates='crew')



TABLE_CLASSES = {
    'films': Film,
    'persons': Person,
    'roles': Role,
    'film_crew': FilmCrew
}

Base.metadata.create_all(engine)
Session: sessionmaker = sessionmaker(bind=engine)
session: SessionType = Session()
