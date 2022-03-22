def getBasicInfoReport(settings,startTime,endTime):
    reportText ="# IISLog\n"
    reportText += "- Term : "+str(startTime) +" - " + str(endTime) +"\n"
    reportText += "- StatusCode: "+ str(settings["minError"]) +" - " + str(settings["maxError"])+"\n"
    return reportText

def getSortedErrors(logDatasPerLine,statusIndex,subStatusIndex,win32StatusIndex):
    errors,statusCounts,results = [],[],[]

    index = 0
    while(index<len(logDatasPerLine)-1):
        sc_status = int(logDatasPerLine[index].split(" ")[statusIndex])
        subStatus = int(logDatasPerLine[index].split(" ")[subStatusIndex])
        win32Status = int(logDatasPerLine[index].split(" ")[win32StatusIndex])
        #TODO sc_status と subStatus から先に IIS ログの該当する情報を引き抜く
        error= str(sc_status)+"."+str(subStatus)+"."+str(win32Status)
        if(error not in errors):
            errors.append(error)
            statusCounts.append(1)
        else:
            statusCounts[errors.index(error)] +=1
        index+=1
    
    index = 0
    while(index<len(errors)):
        results.append([errors[index],statusCounts[index]])
        index+=1
    results.sort()
    return results

def analyseLogFilteredbyStatus(filteredData,statusIndex,subStatusIndex,win32StatusIndex,requestsCount):
    logDatasPerLine=filteredData.split("\n")
    
    results = getSortedErrors(logDatasPerLine,statusIndex,subStatusIndex,win32StatusIndex)
    
    # ReportText = "## Errors\n" + str("| ErrorType | Count | description |")+"\n"
    # ReportText +=str("|---|---|-------|")+"\n"
    ReportText = "## Error Status Codes\n" 
    ReportText += "Error Counts/All Counts : " +str(len(logDatasPerLine)-1) +"/" +str(requestsCount)+"\n"
    ReportText += str("| Status Code | Count | ")+"\n"
    ReportText +=str("|---|-------|")+"\n"
    
    index = 0
    while(index<len(results)):
        ReportText +="|"+str(results[index][0]) +"|"+str(results[index][1]) +"|\n"
        index+=1
    
    return ReportText

def analyseLogFilteredbyTimeTaken(logDatasPerLine,requestsCount,mean,stdev,threshold):
    reportText = "## Slow Responses\n"
    reportText += "Error Counts/All Counts :" +str(len(logDatasPerLine)-1) +"/" +str(requestsCount)+"\n"
    reportText += "- Mean : " + str(mean) +"\n" +"- Standard Deviation : " + str(stdev) +"\n"+"- Threshold : " + str(threshold) +"\n"
    return reportText

def addReferences():
    reportText = "# References\n"
    reportText += "- [Status/SubStatus](https://docs.microsoft.com/en-us/troubleshoot/developer/webapps/iis/www-administration-management/http-status-code)\n"
    reportText += "- [Win32Status](https://docs.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-?redirectedfrom=MSDN#ERROR_BAD_COMMAND)\n"
    reportText += "- [HTTPErrorLog](https://docs.microsoft.com/en-us/troubleshoot/developer/webapps/aspnet/site-behavior-performance/error-logging-http-apis)\n"
    return reportText