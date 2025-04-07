from parser import *
import requests

api_url = 'http://127.0.0.1:5000'

if args.command == 'add':
    if args.api:
        url = f"{api_url}/{args.table}"
        payload = dict(zip(args.values[::2], args.values[1::2]))
        response = requests.post(url, json=payload)
        print(response.json()['message'])
        exit()

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
    if args.api:
        url = f"{api_url}/{args.table}/{args.id}"
        response = requests.delete(url)
        print(response.json()['message'])
        exit()

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
    if args.api:
        url = f"{api_url}/{args.table}/{args.id}"
        payload = dict(zip(args.values[::2], args.values[1::2]))
        response = requests.put(url, json=payload)
        print(response.json()['message'])
        exit()

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
    if args.api:
        url = f"{api_url}/{args.table}/search"
        params = dict(zip(args.values[::2], args.values[1::2]))
        response = requests.get(url, params=params)
        print(response.json())
        exit()

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