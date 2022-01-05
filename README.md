# EPAM UA Python Final Project

## Job search
“Job search” is simple web-application which allows users to find and create vacancies for their speciality in a comfortable way.


App functionality:
  - Display list of job categories;
  - Display list of vacancies by categories;
  - Filtering vacancies by special parameters;
  - Respond to the vacancy;
  - Creating account for employer;
  - Log in to your account;
  - List of created vacancies in the profile;
  - Creating your own vacancies;
  - Update and delete vacancy;

More information can be found here - SRS

----
## Basic technologies:
  - Python
  - Flask
  - MySQL
  - HTML, CSS, JS

---
## How to build this project:
### 1. Requirements
```
pip install -r requirements.txt
```
### 2. Set parameters 
```
SECRET_KEY=""
DB_USERNAME=""
DB_PASSWORD=""
DB_NAME=""
JWT_SECRET_KEY="" 
```
### 3. Run migrations
```
flask db init
flask db migrate -m ""
flask db upgrade
```
### 4. Run the project
```
python server_startup.py
```
### 5. Run tests
```
py.test
```

----
## Web application
Main page:
```
http://127.0.0.1:5000/
```
Show all categories:
```
http://127.0.0.1:5000/categories
```
Create vacancy:
```
http://127.0.0.1:5000/vacancy_create
```
Vacancies by category:
```
http://127.0.0.1:5000/<category_slug>
```
Detail vacancy:
```
http://127.0.0.1:5000/vacancy/<vacancy_slug>
```
----
Register user:
```
http://127.0.0.1:5000/signup
```
Login user:
```
http://127.0.0.1:5000/login
```
Profile user:
```
http://127.0.0.1:5000/profile
```
Logout:
```
http://127.0.0.1:5000/logout
```
Admin panel:
```
http://127.0.0.1:5000/admin
```
----
## Web service
Test:
```
http://127.0.0.1:5000/api/ping (GET)
```
Categories:
```
http://127.0.0.1:5000/api/categories (GET)
```
Vacancies:
```
http://127.0.0.1:5000/api/vacancies/<category_slug> (GET, POST, PUT, DELETE)

GET: 
{
    "filterSalary": "" (Not required)
}

POST:
{
    "name": "",
    "salary": "",
    "about": "",
    "contacts": ""
}

PUT: 
{
    "current_name": "",
    "salary": "",
    "about": "",
    "contacts": ""
}

DELETE:
{
    "name": ""
}
```
Authentication:
```
http://127.0.0.1:5000/api/auth/signup (POST)

POST: 
{
    "email": "",
    "password1": "",
    "password2": ""
}

http://127.0.0.1:5000/api/auth/login (POST)

POST:
{
    "email": "",
    "password": ""
}
```