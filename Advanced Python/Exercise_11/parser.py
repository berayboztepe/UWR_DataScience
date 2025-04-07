import argparse
from database import *

# parsing arguments 
parser = argparse.ArgumentParser(description="Manage movies, crew, and roles")
subparsers = parser.add_subparsers(dest='command')

# command add
add_parser = subparsers.add_parser('add', help='Add a new entry')
add_parser.add_argument('--table', required=True, help='Table to add to (films, persons, roles, film_crew)')
add_parser.add_argument('--values', required=True, nargs='+', help='Column-value pairs to add')
add_parser.add_argument('--api', required=False, action='store_true', help='API for adding') # extra

# command delete
delete_parser = subparsers.add_parser('delete', help='Delete entries from a table')
delete_parser.add_argument('--table', required=True, help='Table to delete from (films, persons, roles, film_crew)')
delete_parser.add_argument('--id', required=True, type=int, help='ID of the entry to delete')
delete_parser.add_argument('--api', required=False, action='store_true', help='API for deleting') # extra

# command update
update_parser = subparsers.add_parser('update', help='Update an entry in a table')
update_parser.add_argument('--table', required=True, help='Table to update (films, persons, roles, film_crew)')
update_parser.add_argument('--id', required=True, type=int, help='ID of the entry to update')
update_parser.add_argument('--values', required=True, nargs='+', help='Column-value pairs to update')
update_parser.add_argument('--api', required=False, action='store_true', help='API for updating') # extra

# command search
search_parser = subparsers.add_parser('search', help='Search for entries in a table')
search_parser.add_argument('--table', required=True, help='Table to search in (films, persons, roles, film_crew)')
search_parser.add_argument('--values', required=True, nargs='+', help='Column-value pairs to search for')
search_parser.add_argument('--api', required=False, action='store_true', help='API for searching') # extra

args = parser.parse_args()