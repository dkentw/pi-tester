from Engine.parser import TestCaseParser
from Engine import TestEngine


def GenerateTestCase(testCaseSuites):
    return TestEngine.GenerateTestCase(testCaseSuites)


def run(caseid_prefix):
    return TestEngine.Runner().run(caseid_prefix)
