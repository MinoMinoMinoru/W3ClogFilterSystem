import datetime as dt
import FilterModules.fileManager as fileManager
import FilterModules.resources.httpErrorReference as httpErrorReference

settings = fileManager.getSetting()
filterName4Term ="[filterted_by_term]"
filterName4Status = "[filterted_by_StatusCode]"
filterName4Time="[filterted_by_time-taken]"

def filterLogByTerm(logData,startTime,endTime):
    # Get after #Fields 
    idx = logData.find('#Fields')
    logData = logData[idx:]
    # Get after startTime 
    startTime,idx = getMatchTime(logData,startTime,-1)
    logData = logData[idx:]
    # Get before endTime
    endTime,idx = getMatchTime(logData,endTime,1)
    print("Fitler from " + startTime)
    print("Fitler to " + endTime)

    return startTime,endTime,logData[:idx]

def getMatchTime(logData,targetTime,minutes):
    while(True):
        idx = logData.find(targetTime)
        if(idx!= -1):
            matchTime = targetTime
            break
        dateValue = dt.datetime.strptime(targetTime, '%Y-%m-%d %H:%M')
        dateValue = dateValue + dt.timedelta(minutes=minutes)
        targetTime  = dateValue.strftime('%Y-%m-%d %H:%M')
        continue
    return matchTime,idx

def analyseHttpErrorLog(filteredData,reasonIndex):
    errorTypes,errorCounts,errorDescriptions = [],[],[]
    officialErrors,officialErrorDescriptions = getOfficialDescriptions()

    logDatasPerLine=filteredData.split("\n")
    logDatasPerLine.pop()

    for log in logDatasPerLine:
        error = log.split(" ")[reasonIndex]
        if(error not in errorTypes):
            errorTypes.append(error)
            errorCounts.append(int(1))
            errorDescriptions.append(officialErrorDescriptions[int(officialErrors.index(error))])
        else:
            errorCounts[errorTypes.index(error)]+=1

    return errorTypes,errorCounts,errorDescriptions

def getOfficialDescriptions():
    # memos = fileManager.readLogFile("./FilterModules/resources/httpErrors.txt")
    # tmp = memos.split("\n")
    errors = httpErrorReference.Erors
    errorTypes,errorDescriptions =[],[]

    for error in errors:
        errorTypes.append(error.split(":")[0])
        errorDescriptions.append(error.split(":")[1])

    return errorTypes,errorDescriptions

def getHttpErrorReport(filteredLogData,reasonIndex,startTime,endTime):
    errorTypes,errorCounts,errorDescriptions = analyseHttpErrorLog(filteredLogData,reasonIndex)
    reportText = "# Http Error\n"
    reportText += f'- Term  : {startTime} - {endTime}\n'
    reportText += "## Errors\n" + str("| ErrorType | Count | description |")+"\n"
    reportText +=str("|---|---|-------|")+"\n"

    for index,error in enumerate(errorTypes):
        reportText += f'|{errorTypes[index]} |{errorCounts[index]} |{errorDescriptions[index]}|\n'

    return reportText

def getformats(logData):
    fileformat = logData.split("\n")[3]

    fieldElements = fileformat.split(" ")    
    reasonIndex = fieldElements.index("s-reason")-1
    fileformat += '\n'

    return fileformat,reasonIndex

def getLogTime(logData):
    ''' get first & end Date of httpError log file '''
    firstTime = logData.split("\n")[4].split(" ")
    endTime = logData.split("\n")[-2].split(" ")
    logFileTerm = f'{firstTime[0]} {firstTime[1]}  ~ {endTime[0]} {endTime[1]}'
    return logFileTerm
    
def outputFilterdLogandReport(logData,inputFileName,startTime,endTime):
    fileformat,reasonIndex = getformats(logData)
    startTime,endTime,filteredLogData =filterLogByTerm(logData,startTime,endTime)
    outputFileName = filterName4Term+inputFileName

    reportText = getHttpErrorReport(filteredLogData,reasonIndex,startTime,endTime)
    fileManager.outputHttpErrorFile(fileformat + filteredLogData,outputFileName)
    return str(reportText)

# ######
# Don't use now
# ######
def removeFields(logData):
    ''' 既に出力済のファイルを読み込んだ時に filter 処理のために #Field を消して成型する用(return:string)'''
    idx = logData.find("#Fields:")
    logData = logData[idx:]
    # 2021 とかの Date ではじまるからそこで分割
    idx = logData.find("20")
    return logData[idx:].split("\n\n")[0]