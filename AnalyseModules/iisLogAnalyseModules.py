def getBasicInfoReport(settings,startTime,endTime):
    reportText ='# IISLog\n'
    reportText += f'- Term : {startTime} - {endTime}\n'
    reportText += f'- StatusCode:{settings["minError"]}  - {settings["maxError"]}\n'
    return reportText

def getSortedErrors(logDatasPerLine,statusIndex,subStatusIndex,win32StatusIndex):
    errors,statusCounts,results = [],[],[]

    for log in logDatasPerLine:
        scStatus = int(log.split(" ")[statusIndex])
        subStatus = int(log.split(" ")[subStatusIndex])
        win32Status = int(log.split(" ")[win32StatusIndex])
        error= f'{scStatus}.{subStatus}.{win32Status}'
        #TODO sc_status と subStatus から先に IIS ログの該当する情報を引き抜く
        # ex 500.10 はこういうエラーみたいな情報を。
        if(error not in errors):
            errors.append(error)
            statusCounts.append(1)
        else:
            statusCounts[errors.index(error)] +=1

    for index,error in enumerate(errors):
        results.append([error,statusCounts[index]])

    results.sort()
    return results

def analyseLogFilteredbyStatus(filteredData,statusIndex,subStatusIndex,win32StatusIndex,requestsCount):
    logDatasPerLine=filteredData.split("\n")
    logDatasPerLine.pop()
    
    results = getSortedErrors(logDatasPerLine,statusIndex,subStatusIndex,win32StatusIndex)
    
    ReportText = "## Error Status Codes\n" 
    ReportText += "Error Counts/All Counts : " +str(len(logDatasPerLine)-1) +"/" +str(requestsCount)+"\n"
    ReportText += str("| Status Code | Count | ")+"\n"
    ReportText +=str("|---|-------|")+"\n"

    for result in results:
        ReportText += f'|{result[0]}|{result[1]}|\n'
    
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


# def getReport(settings,startTime,endTime,filteredByStatusCodeData,statusIndex,subStatusIndex,win32StatusIndex,requestsCount):
#     reportText = addReferences()
#     reportText += getBasicInfoReport(settings,startTime,endTime)
#     reportText += iisLogAnalyseModules.analyseLogFilteredbyStatus(filteredByStatusCodeData,statusIndex,subStatusIndex,win32StatusIndex,requestsCount)
#     reportText += iisLogAnalyseModules.analyseLogFilteredbyTimeTaken(filteredByTimeTakenData,requestsCount,mean,stdev,threshold)
#     return reportText