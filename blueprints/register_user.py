from flask import Blueprint, request, jsonify
import db_tools.pw_management as pw_management
from db_tools.db_models import User
from app import db

register_user = Blueprint('register_user', __name__)

@register_user.route('/register', methods=['POST'])
def register():
    #test if user email already exists
    if request.is_json:
        email = request.json['email']
    else:
        email = request.form['email']
    email = email.strip()
    test = User.query.filter_by(email=email).first()

    if test: 
        return jsonify(message="That email already exists"), 409
    else:
        # handle both html forms and json requests
        if request.is_json:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            password = request.json['password']
        else:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            password = request.form['password']
        password = pw_management.hash_password(password)
        user = User(first_name=first_name, last_name=last_name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201