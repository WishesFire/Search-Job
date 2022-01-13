"""
This module works for restful api
`CategoryAPI (GET)`: show all categories
"""

from flask_restful import Resource
from app.models.model import Category
from app.rest.serializers import categories_schema


class CategoryAPI(Resource):
    """
    (GET): show all categories
    """
    @classmethod
    def get(cls):
        """
        Show all categories
        :return: json
        """
        all_categories = Category.query.all()
        categories_serialize = categories_schema.dump(all_categories)
        return categories_serialize
