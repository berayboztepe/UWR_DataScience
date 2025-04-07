from flask import Flask, request, jsonify
from database import Film, session
from sqlalchemy import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"check_same_thread": False}}

# I did just for films

@app.route('/films', methods=['GET'])
def get_films():
    films = session.query(Film).all()
    return jsonify([{'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation} for film in films])

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id):
    film = session.query(Film).get(film_id)
    if film:
        return jsonify({'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation})
    return jsonify({'message': 'Film not found'}), 404

@app.route('/films', methods=['POST'])
def create_film():
    data = request.json
    new_film = Film(title=data['title'], year_of_creation=data['year_of_creation'])
    session.add(new_film)
    session.commit()
    return jsonify({'message': 'Film created successfully'}), 201

@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    film = session.query(Film).get(film_id)
    if film:
        data = request.json
        film.title = data['title']
        film.year_of_creation = data['year_of_creation']
        session.commit()
        return jsonify({'message': 'Film updated successfully'})
    return jsonify({'message': 'Film not found'}), 404

@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film = session.query(Film).get(film_id)
    if film:
        session.delete(film)
        session.commit()
        return jsonify({'message': 'Film deleted successfully'})
    return jsonify({'message': 'Film not found'}), 404

@app.route('/films/search', methods=['GET'])
def search_films():
    filters = []
    title = request.args.get('title')
    year_of_creation = request.args.get('year_of_creation')

    if title:
        filters.append(Film.title == title)
    if year_of_creation:
        filters.append(Film.year_of_creation == int(year_of_creation))

    films = session.query(Film).filter(and_(*filters)).all()
    return jsonify([{'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation} for film in films])
    
if __name__ == '__main__':
    app.run()