

class TestBaseConfig(object):
    SECRET_KEY = "osdjgposdfjfpo234po23jkpofsdj"
    DEBUG = True


class ProductionBaseConfig(TestBaseConfig):
    DEBUG = False
