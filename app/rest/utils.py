"""
Special tools used in rest / api.
"""

from sqlalchemy import exc


def vacancy_check(func):
    """
    Check the rest function for errors
    :param func: any rest func
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except exc.ArgumentError:
            return {"msg": "Invalid or conflicting function argument is supplied"}, 404
        except exc.SQLAlchemyError:
            return {"msg": "Execution of a database operation fails"}, 404
        except Exception as error:
            return {"msg": str(error)}, 404
    return wrapper
