from src.systemtest.tests.BadassBastardTest import BadassBastardTest
from src.systemtest.tests.CrashTest import CrashTest
from src.systemtest.tests.CupidTest import CupidTest
from src.systemtest.tests.DoublePattTest import DoublePattTest
from src.systemtest.tests.Exampletest import Exampletest
from src.systemtest.tests.FastDeath import FastDeath
from src.systemtest.tests.LoveWin import LoveWinTest
from src.systemtest.tests.PattTest import PattTest
from src.systemtest.tests.RedhatTest import RedhatTest
from src.systemtest.tests.SeherinTest import SeherinTest
from src.systemtest.tests.TerrorwolfTest import TerrorwolfTest
from src.systemtest.tests.WhiteWolfTest import WhiteWolfTest


class SystemTestRegistration(object):
    def __init__(self, main):
        super(SystemTestRegistration, self)
        self.main = main

    def register(self):
        self.main.register(Exampletest)  # has to be run first
        self.main.register(CrashTest)
        self.main.register(BadassBastardTest)
        self.main.register(FastDeath)
        self.main.register(PattTest)
        self.main.register(DoublePattTest)
        self.main.register(SeherinTest)
        self.main.register(RedhatTest)
        self.main.register(TerrorwolfTest)
        self.main.register(WhiteWolfTest)
        self.main.register(CupidTest)
        self.main.register(LoveWinTest)
