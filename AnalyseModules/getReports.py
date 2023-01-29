import FilterModules.fileManager as fileManager
import FilterModules.iisLogFilterModules as iisLogFilterModules
import FilterModules.httpErrorLogFilterModules as httpErrorLogFilterModules

def getReports(inputIisLogFileName,inputHttpErrorLogFileName,startTime,endTime):
    ''' call this method to get Repots and filterrd log'''
    issReport = getIISLogReport(inputIisLogFileName,startTime,endTime)
    httpErrorReport = getHttpErrorReport(inputHttpErrorLogFileName,startTime,endTime)
        
    reportText = issReport + httpErrorReport
    fileManager.outputReport(reportText,"SimpleReport.md")

def getIISLogReport(file,startTime,endTime):
    inputIisLogFileName =file
    iisLogData = fileManager.readLogFile("./input/iislog/"+inputIisLogFileName)
    print("Filter next iislog:",inputIisLogFileName)
    return iisLogFilterModules.outputFilterdLogandReport(iisLogData,inputIisLogFileName,startTime,endTime)

def getHttpErrorReport(file,startTime,endTime):
    inputHttpErrorLogFileName = file
    httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
    print("Filter next httperrorlog:",inputHttpErrorLogFileName)
    return httpErrorLogFilterModules.outputFilterdLogandReport(httpErrorLogData,inputHttpErrorLogFileName,startTime,endTime)