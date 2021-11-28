from app import db
from slugify import slugify
from flask_login import UserMixin


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100))
    vacancies = db.relationship("Vacancy", backref="category")

    def __init__(self, *args, **kwargs):
        if "slug" not in kwargs:
            kwargs["slug"] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "Category"


class Vacancy(db.Model):
    __tablename__ = "vacancy"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100))
    salary = db.Column(db.FLOAT, nullable=False)
    info = db.Column(db.String(400), nullable=False)
    contacts = db.Column(db.String(100), nullable=False)
    user = db.Column(db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __repr__(self):
        return "Vacancy"


def init_categories():
    db.create_all()
    db.session.add()
    db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Users {self.id}'


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vacancies = db.relationship("Vacancy")

