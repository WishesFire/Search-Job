from flask_restful import Resource


class TestConnection(Resource):
    """
    Make test connection
    """
    @classmethod
    def get(cls):
        return {"Ping": "Pong"}
