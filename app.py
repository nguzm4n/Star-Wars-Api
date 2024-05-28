import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import datetime
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, Character, Planet, Favorite

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
Migrate(app, db)
CORS(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    people = list(map(lambda character: character.serialize(), people))

    return jsonify(people), 200


@app.route('/register', methods=['POST'])
def registro():
    user = request.json

    username = user.get('username')
    password = user.get('password')
    email = user.get('email')
    name = user.get('name')

    if not 'username' in user:
        return jsonify({"msg": "username required"}), 400

    user = User(
        username=username,
        email=email,
        password=password,
        name=name,
        date=datetime.datetime.now()
    )

    user.save()

    return jsonify({"success": "Welcome! Your Registration was Successful"}), 201


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planets), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200


@app.route('/people/<int:id>', methods=['GET'])
def get_peopleid(id):
    people = Character.query.get(id)

    return jsonify(people), 200


@app.route('/planets/<int:id>', methods=['GET'])
def get_planetid(id):
    planet = Planet.query.get(id)

    return jsonify(planet), 200


@app.route('/user/<int:id>/favorites', methods=['GET'])
def get_userfav(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=id).all()
    favorites_data = [fav.serialize() for fav in favorites]

    return jsonify({"user": user.serialize(), "favorites": favorites_data}), 200


@app.route('/user/<int:user_id>/favorite_planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        return jsonify({"error": "Planet already in favorites"}), 400

    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"success": "Planet added to favorites"}), 201

@app.route('/user/<int:user_id>/favorite_character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    planet = Planet.query.get(character_id)
    if not planet:
        return jsonify({"error": "Character not found"}), 404

    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite:
        return jsonify({"error": "Character already in favorites"}), 400

    favorite = Favorite(user_id=user_id, character_id=character_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"success": "Character added to favorites"}), 201

@app.route('/user/<int:user_id>/favorite_planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Planet not in favorites"}), 400

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"success": "Planet deleted from favorites"}), 200



@app.route('/user/<int:user_id>/favorite_character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    planet = Planet.query.get(character_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    favorite = Favorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite:
        return jsonify({"error": "Character not in favorites"}), 400

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"success": "Character deleted from favorites"}), 200

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
