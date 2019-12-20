from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from db_tools.db_models import db, Planet, User
import db_tools.pw_management as pw_management
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message

# Instantiate app
app = Flask(__name__)

from blueprints.register_user import register_user
from blueprints.login import login_action
from blueprints.crud import create_planet, read_planet, update_planet, delete_planet

# Instantiate app
app = Flask(__name__)
# register blueprints
app.register_blueprint(register_user)
app.register_blueprint(login_action)
app.register_blueprint(create_planet)
app.register_blueprint(read_planet)
app.register_blueprint(update_planet)
app.register_blueprint(delete_planet)

# set up SQLAlchemy db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' # change this for production

# Instanciations
db.init_app(app)
jwt = JWTManager(app)

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
@app.route('/plantes', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(data=result)

if __name__ == "__main__":
    app.run()