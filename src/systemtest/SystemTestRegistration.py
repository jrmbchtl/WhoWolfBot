from src.systemtest.tests.Exampletest import Exampletest
from src.systemtest.tests.FastDeath import FastDeath


class SystemTestRegistration(object):
    def __init__(self, main):
        super(SystemTestRegistration, self)
        self.main = main

    def register(self):
        self.main.register(Exampletest(self.main.getSc()))  # has to be run first
        self.main.register(FastDeath(self.main.getSc()))
