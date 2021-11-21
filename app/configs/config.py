

class TestBaseConfig(object):
    SECRET_KEY = "osdjgposdfjfpo234po23jkpofsdj"
    TESTING = True
    DEBUG = True


class ProductionBaseConfig(TestBaseConfig):
    DEBUG = False
