from src.systemtest.tests.Exampletest import Exampletest


class SystemTestRegistration(object):
    def __init__(self, main):
        super(SystemTestRegistration, self)
        self.main = main

    def register(self):
        self.main.register(Exampletest(self.main.getSc()))  # has to be run first
