def getBasicInfoReport(requestsCount,errorCount,longCount,mean,stdev,threshold):
    ''' Return Report String '''
    reportText ="# IISLog\n"
    reportText += "## StatusCode\n"
    reportText += "errorCount/allRequests : "+str(errorCount)+"/"+str(requestsCount)+"\n"

    reportText += "## Time-Taken\n"
    reportText += "Mean : " + str(mean) +"\n" +"Standard Deviation : " + str(stdev) +"\n"+"Threshold : " + str(threshold) +"\n"
    reportText += "longCount/allRequests : "+str(longCount)+"/"+str(requestsCount)+"\n"
    return reportText

def analyseLogFilteredbyTimeTaken(filteredData):
    print()

def getSortedErrors(logDatasPerLine,statusIndex,subStatusIndex,win32StatusIndex):
    errors,statusCounts,results = [],[],[]

    index = 0
    while(index<len(logDatasPerLine)-1):
        sc_status = int(logDatasPerLine[index].split(" ")[statusIndex])
        subStatus = int(logDatasPerLine[index].split(" ")[subStatusIndex])
        win32Status = int(logDatasPerLine[index].split(" ")[win32StatusIndex])
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

def analyseLogFilteredbyStatus(filteredData,statusIndex,subStatusIndex,win32StatusIndex):
    logDatasPerLine=filteredData.split("\n")
    
    results = getSortedErrors(logDatasPerLine,statusIndex,subStatusIndex,win32StatusIndex)
    
    # ReportText = "## Errors\n" + str("| ErrorType | Count | description |")+"\n"
    # ReportText +=str("|---|---|-------|")+"\n"
    ReportText = "## Error Status Codes\n" 
    ReportText += "Error Counts :" +str(len(logDatasPerLine)-1) +" \n"+ str("| Status Code | Count | ")+"\n"
    ReportText +=str("|---|-------|")+"\n"
    
    index = 0
    while(index<len(results)):
        ReportText +="|"+str(results[index][0]) +"|"+str(results[index][1]) +"|\n"
        index+=1
    return ReportText
    # print(ReportText)
