import argparse

# Define the parser
parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Manage movies, crew, and roles")
subparsers: argparse._SubParsersAction = parser.add_subparsers(dest='command')

# Command: add
# Allows adding a new entry to a specified table (e.g., films, persons, etc.)
add_parser: argparse.ArgumentParser = subparsers.add_parser('add', help='Add a new entry')
add_parser.add_argument(
    '--table',
    required=True,
    type=str,
    help='Table to add to (films, persons, roles, film_crew)'
)
add_parser.add_argument(
    '--values',
    required=True,
    nargs='+',
    type=str,
    help='Column-value pairs to add'
)
add_parser.add_argument(
    '--api',
    required=False,
    action='store_true',
    help='API for adding'  # extra
)

# Command: delete
# Deletes an entry from the specified table by its ID
delete_parser: argparse.ArgumentParser = subparsers.add_parser('delete', help='Delete entries from a table')
delete_parser.add_argument(
    '--table',
    required=True,
    type=str,
    help='Table to delete from (films, persons, roles, film_crew)'
)
delete_parser.add_argument(
    '--id',
    required=True,
    type=int,
    help='ID of the entry to delete'
)
delete_parser.add_argument(
    '--api',
    required=False,
    action='store_true',
    help='API for deleting'  # extra
)

# Command: update
# Updates an existing entry in the specified table
update_parser: argparse.ArgumentParser = subparsers.add_parser('update', help='Update an entry in a table')
update_parser.add_argument(
    '--table',
    required=True,
    type=str,
    help='Table to update (films, persons, roles, film_crew)'
)
update_parser.add_argument(
    '--id',
    required=True,
    type=int,
    help='ID of the entry to update'
)
update_parser.add_argument(
    '--values',
    required=True,
    nargs='+',
    type=str,
    help='Column-value pairs to update'
)
update_parser.add_argument(
    '--api',
    required=False,
    action='store_true',
    help='API for updating'  # extra
)

# Command: search
# Searches for entries in the specified table based on column-value filters
search_parser: argparse.ArgumentParser = subparsers.add_parser('search', help='Search for entries in a table')
search_parser.add_argument(
    '--table',
    required=True,
    type=str,
    help='Table to search in (films, persons, roles, film_crew)'
)
search_parser.add_argument(
    '--values',
    required=True,
    nargs='+',
    type=str,
    help='Column-value pairs to search for'
)
search_parser.add_argument(
    '--api',
    required=False,
    action='store_true',
    help='API for searching'  # extra
)

if __name__ == "__main__":
    args: argparse.Namespace = parser.parse_args()
