import os
import FilterModules.fileManager as fileManager
import FilterModules.iisLogFilterModules as iisLogFilterModules
import FilterModules.httpErrorLogFilterModules as httpErrorLogFilterModules

def getIISLogReport():
    inputIisLogFileName = os.listdir("./input/iislog/")[0]
    iisLogData = fileManager.readLogFile("./input/iislog/"+inputIisLogFileName)
    print("Filter next iislog:",inputIisLogFileName)
    return iisLogFilterModules.outputFilterdLogandReport(iisLogData,inputIisLogFileName)

def getHttpErrorReport():
    inputHttpErrorLogFileName = os.listdir("./input/httperrorlog/")[0]
    httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
    print("Filter next httperrorlog:",inputHttpErrorLogFileName)
    return httpErrorLogFilterModules.outputFilterdLogandReport(httpErrorLogData,inputHttpErrorLogFileName)

def main():
    issReport,httpErrorReport = "# IISLog\n There is no iislog Report\n","# HTTPErrorLog\n There is no HTTP Error Report\n"
    issReport = getIISLogReport()
    # httpErrorReport = getHttpErrorReport()
    reportText = issReport + httpErrorReport
    fileManager.outputReport(reportText,"SimpleReport.md")

main()