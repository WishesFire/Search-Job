from app import create_app, db
from app.models.model import Category

app = create_app()


def test_add_category():
    """
    Check add element category in database
    """
    category_example = "Testing"

    with app.app_context():
        db.create_all()

        check_exists = Category.query.filter_by(name=category_example).first()
        if check_exists:
            Category.query.filter_by(name=category_example).delete()

        new_category = Category(name=category_example)
        db.session.add(new_category)
        db.session.commit()

        result = Category.query.filter_by(name=category_example).first()
        assert result.name == "Testing"

        Category.query.filter_by(name=category_example).delete()


def test_category_slug():
    """
    Check slug element category in database
    """
    category_example = "Testing"

    with app.app_context():
        db.create_all()

        check_exists = Category.query.filter_by(name=category_example).first()
        if not check_exists:
            new_category = Category(name=category_example)
            db.session.add(new_category)
            db.session.commit()

        result = Category.query.filter_by(name=category_example).first()
        assert result.slug

        Category.query.filter_by(name=category_example).delete()
