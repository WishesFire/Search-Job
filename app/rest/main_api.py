"""
This module works for restful api
TestConnection - (GET)
"""

from flask_restful import Resource


class TestConnection(Resource):
    """
    Make test connection
    """
    @classmethod
    def get(cls):
        """
        Check connection
        :return: Ping: Pong
        """
        return {"Ping": "Pong"}
