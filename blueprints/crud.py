from flask import Blueprint, request, jsonify
from db_tools.db_models import Planet, db
from db_tools.db_schemas import planet_schema
from flask_jwt_extended import jwt_required

create_planet = Blueprint('create_planet', __name__)
read_planet = Blueprint('read_planet', __name__)
update_planet = Blueprint('update_planet', __name__)
delete_planet = Blueprint('delete_planet', __name__)

@create_planet.route('/add_planet', methods=["POST"])
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

@read_planet.route('/planet_details/<int:planet_id>', methods=["GET"])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else: 
        return jsonify(Message="that plant does not exist."), 404

@update_planet.route('/update_planet', methods=["PUT"])
@jwt_required
def update():
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

@delete_planet.route('/delete_planet/<int:planet_id>', methods=["DELETE"])
@jwt_required
def delete(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(Message="You deleted a planet."), 202
    return jsonify(Message="Planet not found."), 404