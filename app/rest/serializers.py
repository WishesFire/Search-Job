"""
This module used for serializing data

CategorySchema - data from Category model
VacancySchema - data from Vacancy model
"""

from app import ma
from app.models.model import Category, Vacancy


class CategorySchema(ma.SQLAlchemyAutoSchema):
    """
    Used for serialize Category data
    """
    class Meta:
        model = Category
        fields = ("name", "slug")


class VacancySchema(ma.SQLAlchemyAutoSchema):
    """
    Used for serialize Vacancy data
    """
    class Meta:
        model = Vacancy
        fields = ("name", "salary", "info", "contacts")


categories_schema = CategorySchema(many=True)
vacancies_schema = VacancySchema(many=True)
