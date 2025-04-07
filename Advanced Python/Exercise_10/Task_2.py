from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, validates
import argparse
import json

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

# parsing arguments 
parser = argparse.ArgumentParser(description="Manage movies, crew, and roles")
subparsers = parser.add_subparsers(dest='command')

# command add
add_parser = subparsers.add_parser('add', help='Add a new entry')
add_parser.add_argument('--table', required=True, help='Table to add to (films, persons, roles, film_crew)')
add_parser.add_argument('--values', required=True, nargs='+', help='Column-value pairs to add')

# command delete
delete_parser = subparsers.add_parser('delete', help='Delete entries from a table')
delete_parser.add_argument('--table', required=True, help='Table to delete from (films, persons, roles, film_crew)')
delete_parser.add_argument('--id', required=True, type=int, help='ID of the entry to delete')

# command update
update_parser = subparsers.add_parser('update', help='Update an entry in a table')
update_parser.add_argument('--table', required=True, help='Table to update (films, persons, roles, film_crew)')
update_parser.add_argument('--id', required=True, type=int, help='ID of the entry to update')
update_parser.add_argument('--values', required=True, nargs='+', help='Column-value pairs to update')

# command search
search_parser = subparsers.add_parser('search', help='Search for entries in a table')
search_parser.add_argument('--table', required=True, help='Table to search in (films, persons, roles, film_crew)')
search_parser.add_argument('--values', required=True, nargs='+', help='Column-value pairs to search for')

# command list
list_parser = subparsers.add_parser('list', help='List entries from a table')
list_parser.add_argument('--table', required=True, help='Table to list from (films, persons, roles, film_crew)')

# command load
load_parser = subparsers.add_parser('load', help='Load test data from a JSON file')
load_parser.add_argument('--file', required=True, help='Path to the JSON file')

args = parser.parse_args()

if args.command == 'add':
    if args.table == 'films':
        new_entry = Film()
    elif args.table == 'persons':
        new_entry = Person()
    elif args.table == 'roles':
        new_entry = Role()
    elif args.table == 'film_crew':
        new_entry = FilmCrew()
    else:
        raise ValueError("Invalid table name")
    
    values = args.values
    if len(values) % 2 != 0:
        raise ValueError("Values must be in key-value pairs")
    
    for i in range(0, len(values), 2):
        setattr(new_entry, values[i], values[i + 1])
    
    session.add(new_entry)
    session.commit()
    print(f"Added to {args.table}: {values}")

elif args.command == 'delete':
    table = args.table
    entry_id = args.id
    if table == 'films':
        entry = session.query(Film).get(entry_id)
    elif table == 'persons':
        entry = session.query(Person).get(entry_id)
    elif table == 'roles':
        entry = session.query(Role).get(entry_id)
    elif table == 'film_crew':
        entry = session.query(FilmCrew).get(entry_id)
    else:
        raise ValueError("Invalid table name")
    
    if entry:
        session.delete(entry)
        session.commit()
        print(f"Deleted entry with ID {entry_id} from {table}")
    else:
        print(f"No entry found with ID {entry_id} in {table}")

elif args.command == 'update':
    table = args.table
    entry_id = args.id
    values = args.values
    if len(values) % 2 != 0:
        raise ValueError("Values must be in key-value pairs")

    if table == 'films':
        entry = session.query(Film).get(entry_id)
    elif table == 'persons':
        entry = session.query(Person).get(entry_id)
    elif table == 'roles':
        entry = session.query(Role).get(entry_id)
    elif table == 'film_crew':
        entry = session.query(FilmCrew).get(entry_id)
    else:
        raise ValueError("Invalid table name")
    
    if entry:
        for i in range(0, len(values), 2):
            setattr(entry, values[i], values[i + 1])
        session.commit()
        print(f"Updated entry with ID {entry_id} in {table}")
    else:
        print(f"No entry found with ID {entry_id} in {table}")

elif args.command == 'search':
    table = args.table
    values = args.values

    if table not in TABLE_CLASSES:
        raise ValueError(f"Invalid table name: {table}")

    model_class = TABLE_CLASSES[table]
    query = session.query(model_class)

    if len(values) % 2 != 0:
        raise ValueError("Values must be in key-value pairs")
    
    for i in range(0, len(values), 2):
        query = query.filter(getattr(model_class, values[i]) == values[i + 1])
    
    entries = query.all()
    for entry in entries:
        print(entry.__dict__)


elif args.command == 'list':
    table = args.table
    if table == 'films':
        entries = session.query(Film).all()
    elif table == 'persons':
        entries = session.query(Person).all()
    elif table == 'roles':
        entries = session.query(Role).all()
    elif table == 'film_crew':
        entries = session.query(FilmCrew).all()
    else:
        raise ValueError("Invalid table name")
    
    for entry in entries:
        print(entry.__dict__)

elif args.command == 'load':
    with open(args.file, 'r') as f:
        data = json.load(f)
    
    for table, rows in data.items():
        for row in rows:
            if table == 'films':
                entry = Film(**row)
            elif table == 'persons':
                entry = Person(**row)
            elif table == 'roles':
                entry = Role(**row)
            elif table == 'film_crew':
                entry = FilmCrew(**row)
            else:
                raise ValueError("Invalid table name")
            session.add(entry)
    session.commit()
    print("Test data loaded successfully")


"""TEST
read json file: python3 Task_2.py load --file db.json

list after reading json file: 
python3 Task_2.py list --table films
python3 Task_2.py list --table persons
python3 Task_2.py list --table roles

add new film: python3 Task_2.py add --table films --values title "Dunkirk" year_of_creation 2017
python3 Task_2.py list --table films 

delete: python3 Task_2.py delete --table films --id 1
python3 Task_2.py list --table films 

update: python3 Task_2.py update --table films --id 2 --values title "Tenet"
python3 Task_2.py list --table films 

search: python3 Task_2.py search --table films --values title "Interstellar"
python3 Task_2.py search --table films --values title "Dunkirk"

"""