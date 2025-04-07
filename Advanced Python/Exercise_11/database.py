from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, validates

Base = declarative_base()
engine = create_engine('sqlite:///movies.db', connect_args={'check_same_thread': False})

# define tables
class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    year_of_creation = Column(Integer, nullable=False)

    crew = relationship('FilmCrew', back_populates='film', cascade='all, delete')

    @validates('year_of_creation')
    def validate_year(self, key, value):
        if int(value) < 1888:
            raise ValueError("Year must be 1888 or later")
        return value

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    crew = relationship('FilmCrew', back_populates='person')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)

    crew = relationship('FilmCrew', back_populates='role')

class FilmCrew(Base):
    __tablename__ = 'film_crew'
    id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey('films.id', ondelete='CASCADE'), nullable=False)
    person_id = Column(Integer, ForeignKey('persons.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    film = relationship('Film', back_populates='crew')
    person = relationship('Person', back_populates='crew')
    role = relationship('Role', back_populates='crew')

TABLE_CLASSES = {
    'films': Film,
    'persons': Person,
    'roles': Role,
    'film_crew': FilmCrew
}

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()