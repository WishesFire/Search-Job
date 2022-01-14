"""
This module has all the necessary functions to interact with the Category model
"""

from app.models.model import Category


class CategoryService:
    """
    CRUD operations on Category model
    """

    @staticmethod
    def get_all_categories() -> Category:
        """
        Takes all fields from the Category model
        :return: List categories
        """
        return Category.query.all()

    @staticmethod
    def find_category_by_name(vacancy_category: str) -> Category:
        """
        Takes a category according to a certain parameter
        :param vacancy_category: the category to which the vacancy belongs
        :return: A certain category
        """
        return Category.query.filter_by(name=vacancy_category).first()

    @staticmethod
    def find_category_by_slug(category_slug: str) -> Category:
        """
        Takes a category according to a certain parameter
        :param category_slug:
        :return: A certain category
        """
        return Category.query.filter_by(slug=category_slug).first()
