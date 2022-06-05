import os
import FilterModules.fileManager as fileManager
import FilterModules.iisLogFilterModules as iisLogFilterModules
import FilterModules.httpErrorLogFilterModules as httpErrorLogFilterModules

# iisFileList=os.listdir("./input/iislog/")
# httpErrorFileList=os.listdir("./input/httperrorlog/")

inputIisLogFileName = os.listdir("./input/iislog/")[0]
iisLogData = fileManager.readLogFile("./input/iislog/"+inputIisLogFileName)
print("Filter next iislog:",inputIisLogFileName)

def getHttpErrorReport():
    inputHttpErrorLogFileName = os.listdir("./input/httperrorlog/")[0]
    httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
    print("Filter next httperrorlog:",inputHttpErrorLogFileName)
    return httpErrorLogFilterModules.outputFilterdLogandReport(httpErrorLogData,inputHttpErrorLogFileName)

def main():
    issReport = iisLogFilterModules.outputFilterdLogandReport(iisLogData,inputIisLogFileName)
    httpErrorReport = getHttpErrorReport()
    reportText = issReport + httpErrorReport
    fileManager.outputReport(reportText,"SimpleReport.md")

main()