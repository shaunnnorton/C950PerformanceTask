from enum import Enum as e

class specialActions(e):
    DELAY = 0
    TRUCK = 1
    WITH = 2
    ADDRESS = 4

class Actions():
    @staticmethod
    def verifyAvalible(specialNote: tuple) -> bool:
        pass

    
    @staticmethod
    def translateAction(note: str) -> tuple:
        pass