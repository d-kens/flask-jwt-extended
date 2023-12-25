from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, current_user, get_jwt_identity
from models import User

# create blueprint
auth_blueprint = Blueprint('auth', __name__)

# Route definition within blueprint
@auth_blueprint.post('/register') #route
def register_user(): # hander for '/register' route
    data = request.get_json()


    user = User.get_user_by_username(username = data.get('username'))

    if user is not None:
        return jsonify({
            "error": "user already exist"
        }), 409

    new_user = User(
        username = data.get('username'),
        email = data.get('email')
    )

    new_user.set_password(password=data.get('password'))

    new_user.save()

    return jsonify({
        "message": "user created"
    }), 201

@auth_blueprint.post('/login')
def login_user():
    data = request.get_json()

    user = User.get_user_by_username(username=data.get('username'))

    if user and (user.check_password(password=data.get('password'))):
        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        return jsonify({
            "message": "logged in successfully",
            "tokens": {
                "access_token": access_token,
                "refresh": refresh_token
            }
        }), 200
    

    return jsonify({
        "error": "invalid username or password"
    }), 400

# return details of a specific user with a specific jwt
@auth_blueprint.get('/whoami')
@jwt_required()
def whoami():
    return jsonify({
        "message": "message",
        "user_details": {
            "username": current_user.username, 
            "email": current_user.email
        }
    })


@auth_blueprint.get('/refresh')
@jwt_required(refresh=True)
def refresh_acesss():
    identity = get_jwt_identity()

    new_acess_token = create_access_token(identity=identity)

    return jsonify({
        "acess_token": new_acess_token
    })





"""
Blueprints are used to organize routes, views and other components in flask application.
A collection of endpoints that are responsible for a particular task
1. Create a blueprint
2. Route definition within blueprint
    - Define a route within the auth blueprint for handling POST requests to the "/register" endpoint
    - register_user() fiunction is the handler for this route.
    - When reuest is made to "/auth/register" the register user function will be executed
3. None represent the absence of value

"""