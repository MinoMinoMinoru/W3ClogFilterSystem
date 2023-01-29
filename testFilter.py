# import testModules.Filteriislog as Filteriislog,testModules.FilterHttpError as FilterHttpError
import FilterModules.fileManager as fileManager
import FilterModules.httpErrorLogFilterModules as httpErrorLogFilterModules
import os


def reportTest():
    reportText = Filteriislog.testAnalyse()
    reportText += FilterHttpError.testAnalyse()

    fileManager.outputReport(reportText,"SimpleReport.md")

def settingTest():
    settings = fileManager.getSetting()
    print(settings['useIISLog'])
    if(settings['useIISLog']):
        print("True")
    else:
        print("False")

def httpErrorLogTerm():
    # inputHttpErrorLogFileName = os.listdir("./input/httperrorlog/")[0]
    # httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
    # httpErrorLogFilterModules.getLogTime(httpErrorLogData)
    inputHttpErrorLogFiles= os.listdir("./input/httperrorlog/")
    for inputHttpErrorLogFileName in inputHttpErrorLogFiles:
        # print(inputHttpErrorLogFileName)
        httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
        logFileTerm = httpErrorLogFilterModules.getLogTime(httpErrorLogData)
        print(f'{inputHttpErrorLogFileName} {logFileTerm}')

# mainTest()
# reportTest()
# applicationEventTest()

# httpErrorLogTerm()

settingTest()