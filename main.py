import os
import FilterModules.fileManager as fileManager
import FilterModules.iisLogFilterModules as iisLogFilterModules
import FilterModules.httpErrorLogFilterModules as httpErrorLogFilterModules

def getIISLogReport(file,startTime,endTime):
    inputIisLogFileName =file
    iisLogData = fileManager.readLogFile("./input/iislog/"+inputIisLogFileName)
    print("Filter next iislog:",inputIisLogFileName)
    return iisLogFilterModules.outputFilterdLogandReport(iisLogData,inputIisLogFileName,startTime,endTime)

def getHttpErrorReport(file,startTime,endTime):
    # inputHttpErrorLogFileName = os.listdir("./input/httperrorlog/")[0]
    inputHttpErrorLogFileName = file
    httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
    print("Filter next httperrorlog:",inputHttpErrorLogFileName)
    return httpErrorLogFilterModules.outputFilterdLogandReport(httpErrorLogData,inputHttpErrorLogFileName,startTime,endTime)

def main():
    settings = fileManager.getSetting()
    startTime,endTime = settings["startTime"],settings["endTime"]
    
    issReport,httpErrorReport = "# IISLog\n There is no iislog Report\n","# HTTPErrorLog\n There is no HTTP Error Report\n"
    
    if(settings['useIISLog']):
        inputIisLogFileName = os.listdir("./input/iislog/")[0]
        issReport = getIISLogReport(inputIisLogFileName,startTime,endTime)
    else:
        print("You set 'useIISLog' flse")
        
    if(settings['useHttpErrorLog']):
        inputHttpErrorLogFileName = os.listdir("./input/httperrorlog/")[0]
        httpErrorReport = getHttpErrorReport(inputHttpErrorLogFileName,startTime,endTime)
    else:
        print("You set 'useHttpErrorLog' flse")
    reportText = issReport + httpErrorReport
    fileManager.outputReport(reportText,"SimpleReport.md")

main()