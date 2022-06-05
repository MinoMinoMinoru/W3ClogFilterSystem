import datetime as dt

import FilterModules.fileManager as fileManager

''' 初期設定 '''
settings = fileManager.getSetting()
filterName4Term ="[filterted_by_term]"
filterName4Status = "[filterted_by_StatusCode]"
filterName4Time="[filterted_by_time-taken]"
''' 初期設定 ここまで'''

def removeFields(logData):
    ''' 既に出力済のファイルを読み込んだ時に filter 処理のために #Field を消して成型する用(return:string)'''
    idx = logData.find("#Fields:")
    logData = logData[idx:]
    # 2021 とかの Date ではじまるからそこで分割
    idx = logData.find("20")
    return logData[idx:].split("\n\n")[0]

def filterLogByTerm(logData):
    ''' 指定期間でフィルター(input/return:string)'''
    startTime,endTime = settings["startTime"],settings["endTime"]
    
    # startTime より後ろを切り取る
    startTime,idx = getMatchTime(logData,startTime,-1)
    logData = logData[idx:]
    # endTime より前を切り取る
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

    # 1 line 毎に条件を確認するため split
    logDatasPerLine=filteredData.split("\n")

    index =0
    # 最後に空行が入っているから調整
    while(index<len(logDatasPerLine)-1):
        error = logDatasPerLine[index].split(" ")[reasonIndex]
        # print(str(index)+":"+error)
        if(error not in errorTypes):
            errorTypes.append(error)
            errorCounts.append(int(1))
            errorDescriptions.append(officialErrorDescriptions[int(officialErrors.index(error))])
        else:
            errorCounts[errorTypes.index(error)]+=1
        index+=1
    return errorTypes,errorCounts,errorDescriptions

def getOfficialDescriptions():
    # memos = fileManager.readLogFile('./httpErrors.txt')
    memos = fileManager.readLogFile("./FilterModules/resources/httpErrors.txt")
    tmp = memos.split("\n")
    errorTypes =[]
    errorDescriptions =[]
    index =0
    while(index<len(tmp)-1):
        errorTypes.append(tmp[index].split(":")[0])
        errorDescriptions.append(tmp[index].split(":")[1])
        index+=1
    return errorTypes,errorDescriptions

def getHttpErrorReport(filteredLogData,reasonIndex,startTime,endTime):
    errorTypes,errorCounts,errorDescriptions = analyseHttpErrorLog(filteredLogData,reasonIndex)
    reportText = "# Http Error\n"
    reportText += f'- Term  : {startTime} - {endTime}\n'
    reportText += "## Errors\n" + str("| ErrorType | Count | description |")+"\n"
    reportText +=str("|---|---|-------|")+"\n"
    index=0
    while(index<len(errorTypes)):
        reportText +="|"+errorTypes[index] +"|"+str(errorCounts[index]) +"|"+ errorDescriptions[index]+"|\n"
        index+=1
    return reportText

def getformats(logData):
    fileformat = logData.split("\n")[3]

    fieldElements = fileformat.split(" ")    
    reasonIndex = fieldElements.index("s-reason")-1
    fileformat += '\n'

    return fileformat,reasonIndex

def outputFilterdLogandReport(logData,inputFileName):
    fileformat,reasonIndex = getformats(logData)
    startTime,endTime,filteredLogData =filterLogByTerm(logData)
    outputFileName = filterName4Term+inputFileName

    reportText = getHttpErrorReport(filteredLogData,reasonIndex,startTime,endTime)
    fileManager.outputHttpErrorFile(fileformat + filteredLogData,outputFileName)
    return str(reportText)

def filterLogByFlag(logData,flag,inputFileName):
    fileformat,reasonIndex = getformats(logData)

    startTime,endTime,filteredLogData =filterLogByTerm(logData)
    outputFileName = filterName4Term+inputFileName

    if(flag==0):
        '''Filter by Term '''
        fileManager.outputHttpErrorFile(fileformat + filteredLogData,outputFileName)
        
    if(flag==1):
        ''' Simple Report Test '''
        reportText = getHttpErrorReport(filteredLogData,reasonIndex,startTime,endTime)
        # fileManager.outputReport(reportText,"HttpErrorReport.md")
        return str(reportText)

    if(flag==100):
        reportText = getHttpErrorReport(filteredLogData,reasonIndex,startTime,endTime)
        fileManager.outputHttpErrorFile(fileformat + filteredLogData,outputFileName)
        return str(reportText)