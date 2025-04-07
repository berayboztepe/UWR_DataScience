from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import database


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"check_same_thread": False}}
database = SQLAlchemy(app)

@app.route('/films', methods=['GET'])
def get_films():
    films = database.Film.query.all()
    return jsonify([{'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation} for film in films])

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id):
    film = database.Film.query.get(film_id)
    if film:
        return jsonify({'id': film.id, 'title': film.title, 'year_of_creation': film.year_of_creation})
    return jsonify({'message': 'Film not found'}), 404

@app.route('/films', methods=['POST'])
def create_film():
    data = request.json
    new_film = database.Film(title=data['title'], year_of_creation=data['year_of_creation'])
    database.session.add(new_film)
    database.session.commit()
    return jsonify({'message': 'Film created successfully'}), 201

@app.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    film = database.Film.query.get(film_id)
    if film:
        data = request.json
        film.title = data['title']
        film.year_of_creation = data['year_of_creation']
        database.session.commit()
        return jsonify({'message': 'Film updated successfully'})
    return jsonify({'message': 'Film not found'}), 404

@app.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film = database.Film.query.get(film_id)
    if film:
        database.session.delete(film)
        database.session.commit()
        return jsonify({'message': 'Film deleted successfully'})
    return jsonify({'message': 'Film not found'}), 404

@app.route('/film_crew', methods=['POST'])
def add_film_crew():
    data = request.json
    new_crew = database.FilmCrew(film_id=data['film_id'], person_id=data['person_id'], role_id=data['role_id'])
    database.session.add(new_crew)
    database.session.commit()
    return jsonify({'message': 'Film crew member added successfully'}), 201

@app.route('/film_crew/<int:film_id>', methods=['GET'])
def get_film_crew(film_id):
    crew = database.FilmCrew.query.filter_by(film_id=film_id).all()
    if crew:
        crew_details = [
            {
                'crew_id': member.id,
                'person_id': member.person_id,
                'role_id': member.role_id
            } for member in crew
        ]
        return jsonify(crew_details)
    return jsonify({'message': 'No crew found for this film'}), 404

@app.route('/film_crew/<int:crew_id>', methods=['DELETE'])
def delete_film_crew(crew_id):
    crew = database.FilmCrew.query.get(crew_id)
    if crew:
        database.session.delete(crew)
        database.session.commit()
        return jsonify({'message': 'Crew member removed successfully'})
    return jsonify({'message': 'Crew member not found'}), 404

@app.route('/persons', methods=['GET'])
def get_persons():
    persons = database.Person.query.all()
    return jsonify([{'id': person.id, 'name': person.name, 'email': person.email} for person in persons])

@app.route('/persons', methods=['POST'])
def create_person():
    data = request.json
    new_person = database.Person(name=data['name'], email=data['email'])
    database.session.add(new_person)
    database.session.commit()
    return jsonify({'message': 'Person created successfully'}), 201

@app.route('/roles', methods=['GET'])
def get_roles():
    roles = database.Role.query.all()
    return jsonify([{'id': role.id, 'role_name': role.role_name} for role in roles])

@app.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    new_role = database.Role(role_name=data['role_name'])
    database.session.add(new_role)
    database.session.commit()
    return jsonify({'message': 'Role created successfully'}), 201
    
if __name__ == '__main__':
    app.run()