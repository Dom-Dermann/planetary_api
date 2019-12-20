from flask import Blueprint, request, jsonify
from db_tools.db_models import User
from app import users_schema
from flask_jwt_extended import create_access_token
from db_tools.pw_management import verify_password

login_action = Blueprint('login_action', __name__)

@login_action.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    
    user = User.query.filter_by(email=email)
    user = users_schema.dump(user)
    user = user[0]
    stored_pw = user['password']

    verification = verify_password(stored_password=stored_pw, provided_password=password)
    if verification: 
        jwt = create_access_token(identity=email)
        return jsonify(message="you logged in successfully", jwt=jwt)
    else:
        return jsonify(message="permission denied"), 403