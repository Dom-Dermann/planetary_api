from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from db_tools.db_models import db, Planet, User
from flask_marshmallow import Marshmallow
import db_tools.pw_management as pw_management
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message
from blueprints.register_user import register_user

# Instantiate app
app = Flask(__name__)
# register blueprints
app.register_blueprint(register_user)
# set up SQLAlchemy db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' # change this for production

# Instanciations
db.init_app(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# database models
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields=('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

# flask commands for db testing
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("database created")

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped.")

@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name = 'Mercury', planet_type = 'Class D', home_star='Sol', mass=3.256e23, radius=1516, distance=35.98e6)
    venus = Planet(planet_name = 'Venus', planet_type = 'Class K', home_star='Sol', mass=4.867e24, radius=3760, distance=67.24e6)
    earth = Planet(planet_name = 'Earth', planet_type = 'Class M', home_star='Sol', mass=5.972e24, radius=3959, distance=92.96e6)
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='William', last_name='Herschel', email='test@test.com', password='P@ssword')
    db.session.add(test_user)
    db.session.commit()
    print("Database seeded.")


# defining API routes
# actual application endpoints
# user management
@app.route('/plantes', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(data=result)

## CRUD operations
@app.route('/planet_details/<int:planet_id>', methods=["GET"])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else: 
        return jsonify(Message="that plant does not exist."), 404


@app.route('/add_planet', methods=["POST"])
@jwt_required
def add_planet():
    planet_name = request.json['planet_name']
    test = Planet.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify(Message="there is already a planet by that name."), 409
    else:
        planet_type = request.json['planet_type']
        home_star = request.json['home_star']
        mass = float(request.json['mass'])
        radius = float(request.json['radius'])
        distance = request.json['distance']

        new_planet = Planet(planet_name=planet_name, planet_type=planet_type, home_star=home_star, mass=mass, radius=radius, distance=distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(Message="you added a planet."), 201


@app.route('/update_planet', methods=["PUT"])
@jwt_required
def update_planet():
    planet_id = int(request.json['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet: 
        planet.planet_name = request.json['planet_name']
        planet.planet_type = request.json['planet_type']
        planet.home_star = request.json['home_start']
        planet.mass = float(request.json['mass'])
        planet.radius = float(request.json['radius'])
        planet.distance = float(request.json['distance'])
        db.session.commit()
        return jsonify(Message="you updated a planet."), 202
    else:
        return jsonify(Message="that planet does not exist."), 404


@app.route('/delete_planet/<int:planet_id>', methods=["DELETE"])
@jwt_required
def delete_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(Message="You deleted a planet."), 202
    return jsonify(Message="Planet not found."), 404

if __name__ == "__main__":
    app.run()