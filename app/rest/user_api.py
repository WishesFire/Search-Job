"""
This module works for restful api
LoginUserAPI - (POST)
RegistrationUserAPI - (POST)
"""

import datetime
from flask_restful import Resource
from app.service.auth import util_signup, util_login
from flask_jwt_extended import create_access_token
from .handlers import login_user_post_args, registration_user_post_args


class LoginUserAPI(Resource):
    """
    Log in to an existing user's account and create token
    """

    @classmethod
    def post(cls):
        args = login_user_post_args.parse_args()
        email = args.get("email")
        password = args.get("password")

        user_status, user_error_msg, user = util_login(email, password)
        if user_status:
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {"token": access_token}, 200

        return {"msg": f"Something wrong - {user_error_msg}"}, 401


class RegistrationUserAPI(Resource):
    """
    Create a new user in the system
    """

    @classmethod
    def post(cls):
        args = registration_user_post_args.parse_args()
        email = args.get("email")
        password1 = args.get("password1")
        password2 = args.get("password2")

        user = util_signup(email, password1, password2)
        if user:
            user_id = user.id
            return {"msg": "User successfully created", "id": str(user_id)}, 200
        return {"msg": "Failed with registration new user"}, 401
