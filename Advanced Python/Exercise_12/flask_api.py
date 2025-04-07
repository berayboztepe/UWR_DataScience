from flask import Flask, request, jsonify
from database import Film, session
from sqlalchemy import and_
from typing import Any, Dict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "connect_args": {"check_same_thread": False}
}


@app.route('/films', methods=['GET'])
def get_films() -> Any:
    """
    Retrieve all films from the database.

    Returns:
        A JSON response containing a list of all films with their details
        (id, title, and year_of_creation).
    """
    films = session.query(Film).all()
    return jsonify([
        {'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation}
        for film in films
    ])


@app.route('/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id: int) -> Any:
    """
    Retrieve a specific film by its ID.

    Args:
        film_id (int): The ID of the film to retrieve.

    Returns:
        A JSON response with the film's details (id, title, and year_of_creation)
        if found, otherwise a 404 error message.
    """
    film = session.query(Film).get(film_id)
    if film:
        return jsonify({'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation})
    return jsonify({'message': 'Film not found'}), 404


@app.route('/films', methods=['POST'])
def create_film() -> Any:
    """
    Create a new film entry in the database.

    The JSON payload must include:
        - title (str): The title of the film.
        - year_of_creation (int): The year the film was created.

    Returns:
        A JSON response confirming the creation of the film with its ID and a 201 status code.
    """
    data: Dict[str, Any] = request.json or {}
    if not data:
        return jsonify({'message': 'Invalid JSON data provided'}), 400

    new_film = Film(title=data['title'], year_of_creation=data['year_of_creation'])
    session.add(new_film)
    session.commit()
    return jsonify({'message': 'Film created successfully', 'id': new_film.id}), 201


@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id: int) -> Any:
    """
    Update the details of an existing film.

    Args:
        film_id (int): The ID of the film to update.

    The JSON payload must include:
        - title (str): The updated title of the film.
        - year_of_creation (int): The updated year of creation.

    Returns:
        A JSON response confirming the update, or a 404 error message if the film is not found.
    """
    data: Dict[str, Any] = request.json or {}
    if not data:
        return jsonify({'message': 'Invalid JSON data provided'}), 400

    film = session.query(Film).get(film_id)
    if film:
        film.title = data['title']
        film.year_of_creation = data['year_of_creation']
        session.commit()
        return jsonify({'message': 'Film updated successfully'})
    return jsonify({'message': 'Film not found'}), 404


@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id: int) -> Any:
    """
    Delete a film from the database.

    Args:
        film_id (int): The ID of the film to delete.

    Returns:
        A JSON response confirming the deletion, or a 404 error message if the film is not found.
    """
    film = session.query(Film).get(film_id)
    if film:
        session.delete(film)
        session.commit()
        return jsonify({'message': 'Film deleted successfully'})
    return jsonify({'message': 'Film not found'}), 404


@app.route('/films/search', methods=['GET'])
def search_films() -> Any:
    """
    Search for films based on title and/or year_of_creation.

    Query Parameters:
        - title (str): The title of the film to search for (optional).
        - year_of_creation (int): The year of creation to filter films (optional).

    Returns:
        A JSON response containing a list of films that match the search criteria.
    """
    filters = []
    title = request.args.get('title')
    year_of_creation = request.args.get('year_of_creation')

    if title:
        filters.append(Film.title == title)
    if year_of_creation:
        filters.append(Film.year_of_creation == int(year_of_creation))

    films = session.query(Film).filter(and_(*filters)).all()
    return jsonify([
        {'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation}
        for film in films
    ])


if __name__ == '__main__':
    app.run()
