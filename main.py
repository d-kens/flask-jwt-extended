from flask import Flask, jsonify
from extensions import db, jwt
from auth import auth_blueprint
from users import users_blueprint
from models import User

def create_app():
    app = Flask(__name__)

    ## config params to be set via env vaariales with a specifis prefix
    app.config.from_prefixed_env()

    # initalize extensions
    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    # all routes defined in the auth blueprint will have
    # the "/auth" prefix
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(users_blueprint, url_prefix='/users')


    # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(__jwt_header, jwt_data):
        identity = jwt_data['sub']

        return User.query.filter_by(username = identity).one_or_none()




    # jwt error handlers
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
        if identity == "onyango dickens":
            return {
                "isAdmin": True
            }
        
        return {
            "isAdmin": False
        }

    """
        - Error handlers for different scenarios when using FLASK JWT Extended
    """
    # Expired token handler
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({
            "message": "token has expired",
            "error": "token expired"
        }), 401

    
    # Invalid token handler
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "message": "signature verification failed",
            "error": "invalid token"
        }), 401

    
    # Unauthorized (Missing Token) Handler
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "message": "request does not contain a valid token",
            "error": "authorization required"
        }), 401


    return app
