"""module for registering system tests"""
from src.systemtest.tests.badass_bastard_test import BadassBastardTest
from src.systemtest.tests.berserk_test import BerserkTest1
from src.systemtest.tests.berserk_test import BerserkTest2
from src.systemtest.tests.berserk_test import BerserkTest3
from src.systemtest.tests.crash_test import CrashTest
from src.systemtest.tests.cupid_test import CupidTest
from src.systemtest.tests.example_test import Exampletest
from src.systemtest.tests.fast_death_test import FastDeath
from src.systemtest.tests.love_win_test import LoveWinTest
from src.systemtest.tests.patt_test import DoublePattTest
from src.systemtest.tests.patt_test import PattTest
from src.systemtest.tests.psychopath_test import PsychopathTest
from src.systemtest.tests.psychopath_test_2 import PsychopathTest2
from src.systemtest.tests.redhat_test import RedhatTest
from src.systemtest.tests.scallywag_test import ScallywagTest
from src.systemtest.tests.seherin_test import SeherinTest
from src.systemtest.tests.terrorwolf_test import TerrorwolfTest
from src.systemtest.tests.whitewolf_test import WhiteWolfTest


class SystemTestRegistration:
    """class for registering system tests"""
    def __init__(self, main):
        super()
        self.main = main

    def register(self):
        """register system tests here"""
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
        self.main.register(BerserkTest1)
        self.main.register(BerserkTest2)
        self.main.register(BerserkTest3)
        self.main.register(PsychopathTest)
        self.main.register(PsychopathTest2)
        self.main.register(ScallywagTest)

    def get_main(self):
        """dummy method to fill publics"""
        return self.main
