from src.systemtest.Exampletest import Exampletest


class SystemTestRegistration(object):
    def __init__(self, main):
        super(SystemTestRegistration, self)
        self.main = main

    def register(self):
        self.main.register(Exampletest())
