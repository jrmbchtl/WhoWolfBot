"""common util module"""
import random


class Utils:
    """common util class"""

    def __init__(self, seed):
        super().__init__()
        self.seed = seed
        random.seed(seed)

    @staticmethod
    def randrange(start, stop, step=1):
        """randrange using seed"""
        return random.randrange(start, stop, step)

    @staticmethod
    def random():
        """random using seed"""
        return random.random()

    @staticmethod
    def shuffle(lis):
        """shuffle using seed"""
        random.shuffle(lis)

    @staticmethod
    def get_decision(dic):
        """calculates vote decision"""
        choice_to_amount = {}
        for key in dic:
            if dic[key] not in choice_to_amount:
                choice_to_amount[dic[key]] = 1
            else:
                choice_to_amount[dic[key]] += 1

        maximum = 0
        unique = True
        for key in choice_to_amount:
            if choice_to_amount[key] > maximum:
                maximum = choice_to_amount[key]
                unique = True
            elif choice_to_amount[key] == maximum:
                unique = False

        if not unique:
            return None

        for key in choice_to_amount:
            if choice_to_amount[key] == maximum:
                return key
        return None

    @staticmethod
    def unique_decision(dic):
        """checks if a decision is unique"""
        if Utils.get_decision(dic) is None:
            return False
        return True
