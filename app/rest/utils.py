"""
Special tools used in rest api.
"""

# pylint: disable=broad-except

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
            if str(error) == "400 Bad Request: The browser (or proxy)" \
                             " sent a request that this server could not understand.":
                return {"msg": "Data entered incorrect"}
            return {"msg": str(error)}, 404
    return wrapper
