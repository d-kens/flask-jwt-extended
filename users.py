from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import User
from schemas import UserSchema

users_blueprint = Blueprint(
    'users',
    __name__
)


@users_blueprint.get('/all')
@jwt_required()
def get_all_users():
    claims = get_jwt()

    if claims.get('isAdmin') == True:
        # retrieve query parameters page and per page from the request
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)


        # perform a database query using SQLAlchemy paginate method on the User model
        # retrieve a subset of users based on the specified page and per page values
        users = User.query.paginate(
            page = page,
            per_page = per_page
        )

        result = UserSchema().dump(users, many=True)
        return jsonify({
            "users": result,
        }), 200

    return jsonify({
        "error": "you are not authorized to access this"
    }), 401