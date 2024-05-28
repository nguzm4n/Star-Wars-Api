from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    Tabla correspondiente a los usuarios
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime())
    favorites = db.relationship('Favorite', backref='user')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "favorites": self.favorites,
        }


    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(120))
    birth_year = db.Column(db.String(120))
    eye_color = db.Column(db.String(120))
    skin_color = db.Column(db.String(120))
    hair_color = db.Column(db.String(120))
    mass = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "mass": self.mass,
            "height": self.height
        }



class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    surface = db.Column(db.String(120))
    terrain = db.Column(db.String(120))
    climate = db.Column(db.String(120))
    population = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    diameter = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "surface": self.surface,
            "terrain": self.terrain,
            "climate": self.climate,
            "population": self.population,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "diameter": self.diameter
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey(
        'character.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey(
        'planet.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
        }
