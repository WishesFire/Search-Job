"""
This module works for restful api
LoginUserAPI - (POST)
RegistrationUserAPI - (POST)
"""

import datetime
from flask_restful import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity,
                                create_access_token, create_refresh_token)
from app.rest.serializers import vacancies_schema
from app.service.auth_service import util_signup, util_login
from app.service.vacancy_service import VacancyService
from .handlers import login_user_post_args, registration_user_post_args


class LoginUserAPI(Resource):
    """
    Log in to an existing user's account and create token
    """

    @classmethod
    def post(cls):
        """
        Log into the user's account
        :return: msg or token
        """
        args = login_user_post_args.parse_args()
        email = args.get("email")
        password = args.get("password")

        user_status, user_error_msg, user = util_login(email, password)
        if user_status:
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"user_id": user.id, "access_token": access_token, "refresh_token": refresh_token}, 200

        return {"msg": f"Something wrong - {user_error_msg}"}, 401


class RegistrationUserAPI(Resource):
    """
    Create a new user in the system
    """

    @classmethod
    def post(cls):
        """
        Creating a new account
        :return: msg
        """
        args = registration_user_post_args.parse_args()
        email = args.get("email")
        password1 = args.get("password1")
        password2 = args.get("password2")

        user = util_signup(email, password1, password2)
        if user:
            user_id = user.id
            return {"msg": "User successfully created", "id": str(user_id)}, 200
        return {"msg": "Failed with registration new user"}, 401


class ProfileUserAPI(Resource):
    """
    Show user-created vacancies
    """

    @classmethod
    @jwt_required()
    def get(cls):
        """
        Show user's vacancies
        :return: user's vacancies or msg
        """
        user_id = get_jwt_identity()
        all_vacancies = VacancyService.find_vacancies_current_user(user_id)
        if all_vacancies:
            vacancies_serialize = vacancies_schema.dump(all_vacancies)
            return vacancies_serialize, 200
        return {"msg": "No vacancies"}, 200
