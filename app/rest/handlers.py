"""
Request parser (analyzes the query for the required fields)

- login_user_post_args (post) - [email, password]
- registration_user_post_args (post) - [email, password1, password2]
- create_vacancy_post_args (post) - [name, salary, about, contacts]
- delete_vacancy_post_args (delete) - [name]
"""

from flask_restful import reqparse


# LoginUserAPI (POST)
login_user_post_args = reqparse.RequestParser()
login_user_post_args.add_argument("email", type=str, help="User email", required=True)
login_user_post_args.add_argument("password", type=str, help="User password", required=True)

# RegistrationUserAPI (POST)
registration_user_post_args = reqparse.RequestParser()
registration_user_post_args.add_argument("email", type=str, help="User email", required=True)
registration_user_post_args.add_argument("password1", type=str, help="First user password", required=True)
registration_user_post_args.add_argument("password2", type=str, help="Similar user password", required=True)

# VacancyAPI (POST)
create_vacancy_post_args = reqparse.RequestParser()
create_vacancy_post_args.add_argument("name", type=str, help="The main name of the vacancy", required=True)
create_vacancy_post_args.add_argument("salary", type=float, help="Salary vacancies", required=True)
create_vacancy_post_args.add_argument("about", type=str, help="Vacancy information", required=True)
create_vacancy_post_args.add_argument("contacts", type=str, help="Vacancy contacts", required=True)

# VacancyAPI (DELETE)
delete_vacancy_post_args = reqparse.RequestParser()
delete_vacancy_post_args.add_argument("name", type=str, help="The main name of the vacancy", required=True)
