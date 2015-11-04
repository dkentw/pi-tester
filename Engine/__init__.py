from parser import TestCaseParser
def ParseFromCSV(testCaseSuite):
    inst = TestCaseParser()
    return inst.ParseFromCSV(testCaseSuite)

import TestEngine
def GenerateTestCase(testCaseSuites, caseList, csvFileList):
    return TestEngine.GenerateTestCase(testCaseSuites, caseList, csvFileList)


def run(caseid_prefix):
    return TestEngine.run(caseid_prefix)