import os
import FilterModules.fileManager as fileManager
import FilterModules.iisLogFilterModules as iisLogFilterModules
import FilterModules.httpErrorLogFilterModules as httpErrorLogFilterModules


flag = 100
iisFileList=os.listdir("./input/iislog/")
httpErrorFileList=os.listdir("./input/httperrorlog/")

inputIisLogFileName = iisFileList[0]
iisLogData = fileManager.readLogFile("./input/iislog/"+inputIisLogFileName)
print("Filter next iislog:",inputIisLogFileName)

inputHttpErrorLogFileName = httpErrorFileList[0]
httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
print("Filter next httperrorlog:",inputHttpErrorLogFileName)

def main():
    issReport = iisLogFilterModules.filterLogByFlag(iisLogData,flag,inputIisLogFileName)
    httpErrorReport = httpErrorLogFilterModules.filterLogByFlag(httpErrorLogData,flag,inputHttpErrorLogFileName)
    reportText = issReport + httpErrorReport
    fileManager.outputReport(reportText,"SimpleReport.md")

main()