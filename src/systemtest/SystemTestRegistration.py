from src.systemtest.tests.DoublePattTest import DoublePattTest
from src.systemtest.tests.Exampletest import Exampletest
from src.systemtest.tests.FastDeath import FastDeath
from src.systemtest.tests.PattTest import PattTest
from src.systemtest.tests.SeherinTest import SeherinTest


class SystemTestRegistration(object):
    def __init__(self, main):
        super(SystemTestRegistration, self)
        self.main = main

    def register(self):
        self.main.register(Exampletest(self.main.getSc()))  # has to be run first
        self.main.register(FastDeath(self.main.getSc()))
        self.main.register(PattTest(self.main.getSc()))
        self.main.register(DoublePattTest(self.main.getSc()))
        self.main.register(SeherinTest(self.main.getSc()))
