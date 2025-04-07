from argument_parser import parser
import requests
from database import session, Film, Person, Role, FilmCrew, TABLE_CLASSES
from typing import List, Type, TypeVar, Generic

api_url: str = 'http://127.0.0.1:5000'

T = TypeVar('T', bound=Film | Person | Role | FilmCrew)

def search_entries(model_class: Type[T], search_values: List[str]) -> List[T]:
    """
    Searches for entries in the given model class based on search_values.

    Args:
        model_class: The class of the model to query.
        search_values: A list of key-value pairs for filtering the query.

    Returns:
        A list of model objects that match the search criteria.
    """
    query = session.query(model_class)

    if len(search_values) % 2 != 0:
        raise ValueError("Values must be in key-value pairs")

    for i in range(0, len(search_values), 2):
        query = query.filter(getattr(model_class, search_values[i]) == search_values[i + 1])

    return query.all()

if __name__ == "__main__":
    args = parser.parse_args()

    if args.command == 'add':
        if args.api:
            add_url : str = f"{api_url}/{args.table}"
            payload: dict[str, str] = dict(zip(args.values[::2], args.values[1::2]))
            add_response : requests.Response = requests.post(add_url , json=payload)
            print(add_response .json()['message'])
            exit()

        new_entry: Film | Person | Role | FilmCrew
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

        values: list[str] = args.values
        if len(values) % 2 != 0:
            raise ValueError("Values must be in key-value pairs")

        for i in range(0, len(values), 2):
            setattr(new_entry, values[i], values[i + 1])

        session.add(new_entry)
        session.commit()
        print(f"Added to {args.table}: {values}")

    elif args.command == 'delete':
        if args.api:
            delete_url: str = f"{api_url}/{args.table}/{args.id}"
            delete_response: requests.Response = requests.delete(delete_url)
            print(delete_response.json()['message'])
            exit()

        table: str = args.table
        entry_id: int = args.id
        entry: Film | Person | Role | FilmCrew | None = None

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
        if args.api:
            update_url: str = f"{api_url}/{args.table}/{args.id}"
            update_payload: dict[str, str] = dict(zip(args.values[::2], args.values[1::2]))
            update_response: requests.Response = requests.put(update_url, json=update_payload)
            print(update_response.json()['message'])
            exit()

        update_table: str = args.table
        update_entry_id: int = args.id
        update_values: list[str] = args.values

        if len(update_values) % 2 != 0:
            raise ValueError("Values must be in key-value pairs")

        update_entry: Film | Person | Role | FilmCrew | None = None
        if update_table == 'films':
            update_entry = session.query(Film).get(update_entry_id)
        elif update_table == 'persons':
            update_entry = session.query(Person).get(update_entry_id)
        elif update_table == 'roles':
            update_entry = session.query(Role).get(update_entry_id)
        elif update_table == 'film_crew':
            update_entry = session.query(FilmCrew).get(update_entry_id)
        else:
            raise ValueError("Invalid table name")

        if update_entry:
            for i in range(0, len(update_values), 2):
                setattr(update_entry, update_values[i], update_values[i + 1])
            session.commit()
            print(f"Updated entry with ID {update_entry_id} in {update_table}")
        else:
            print(f"No entry found with ID {update_entry_id} in {update_table}")

    elif args.command == 'search':
        if args.api:
            search_url: str = f"{api_url}/{args.table}/search"
            params: dict[str, str] = dict(zip(args.values[::2], args.values[1::2]))
            search_response: requests.Response = requests.get(search_url, params=params)
            print(search_response.json())
            exit()

        search_table: str = args.table
        search_values: list[str] = args.values

        if search_table not in TABLE_CLASSES:
            raise ValueError(f"Invalid table name: {search_table}")

        model_class = TABLE_CLASSES[search_table]

        entries: List[T] = search_entries(model_class, search_values)

        for entry in entries:
            print(entry.__dict__)
"""TEST

add new film:
python3 main.py add --table films --values title "Dunkirk" year_of_creation 2017 --api
python3 main.py add --table films --values title "Interstellar" year_of_creation 2014 --api
check films: curl http://127.0.0.1:5000/films
check films by id: curl http://127.0.0.1:5000/films/2

delete: python3 main.py delete --table films --id 1 --api
check films: curl http://127.0.0.1:5000/films

update: python3 main.py update --table films --id 2 --values title "Tenet" year_of_creation 2020 --api
check films: curl http://127.0.0.1:5000/films

search: python3 main.py search --table films --values title "Interstellar" --api
python3 main.py search --table films --values title "Tenet" --api
"""
