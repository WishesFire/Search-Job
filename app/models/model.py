from app import db
from slugify import slugify


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100))
    vacancies = db.relationship("Vacancy")

    def __init__(self, *args, **kwargs):
        if "slug" not in kwargs:
            kwargs["slug"] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "Category"


class Vacancy(db.Model):
    __tablename__ = "vacancies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100))
    salary = db.Column(db.FLOAT, nullable=False)
    info = db.Column(db.String, nullable=False)
    contacts = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "Vacancy"


def init_categories():
    db.create_all()
    db.session.add()
    db.session.commit()


class User:
    pass
