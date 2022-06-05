import testModules.Filteriislog as Filteriislog,testModules.FilterHttpError as FilterHttpError
import FilterModules.fileManager as fileManager
import FilterModules.eventLogFilterModules as eventLogFilter

def applicationEventTest():
    eventLogFilter.filterApplicationEvents("./input/applicationlog/miito-app.evtx")


def mainTest():
    Filteriislog.main()

def reportTest():
    reportText = Filteriislog.testAnalyse()
    reportText += FilterHttpError.testAnalyse()

    fileManager.outputReport(reportText,"SimpleReport.md")

# mainTest()
# reportTest()
applicationEventTest()