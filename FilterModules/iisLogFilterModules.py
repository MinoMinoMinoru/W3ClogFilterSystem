from statistics import mean,stdev
import datetime as dt

import FilterModules.fileManager as fileManager
import AnalyseModules.iisLogAnalyseModules as iisLogAnalyseModules

''' 初期設定 '''
settings = fileManager.getSetting()
filterName4Term ="[filterted_by_term]"
filterName4Status = "[filterted_by_StatusCode]"
filterName4Time="[filterted_by_time-taken]"
minStatusCode,maxStatusCode = settings["minError"],settings["maxError"]
''' 初期設定 ここまで'''

def getTimeTakenThreshold(logData,timeTakenIndex):
    ''' time-taken の平均+標準偏差を返す(input:list,int/return:int)'''
    index =0
    timeTakens=[]

    # 最後に空行が入っているから調整
    # for log in logData:
    #     if(log!='\n'):
    #         timeTaken=int(log.split(" ")[timeTakenIndex])
    #     timeTakens.append(timeTaken)

    while(index<len(logData)-1):
        timeTaken=int(logData[index].split(" ")[timeTakenIndex])
        timeTakens.append(timeTaken)
        index=index+1

    return int(mean(timeTakens)),int(stdev(timeTakens)),int(mean(timeTakens)+stdev(timeTakens))

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

    # Remove "," for output excel files.
    if("," in logData[:idx]):
        filterdLog = logData[:idx].replace(",","")
    else:
        filterdLog = logData[:idx]
    return startTime,endTime,filterdLog

def getMatchTime(logData,targetTime,minutes):
    ''' modify the time when filter time doesn't match the log '''
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

def filterLogByStatusCode(logData,statusIndex):
    ''' FIlter by status code(input:string,int/return string)'''
    logDatasPerLine=logData.split("\n")

    outputData = ""

    for log in logDatasPerLine:
        sc_status = int(log.split(" ")[statusIndex])
        if(minStatusCode<=sc_status and sc_status<=maxStatusCode):
            outputData += log+"\n"
        # if(log == '\n'):
        #     break

    return outputData

def filterLogByTimetaken(logData,timeTakenIndex):
    '''  filter by time-taken(input:string,int/return string)'''
    logDatasPerLine=logData.split("\n")
    mean,stdev,threshold=getTimeTakenThreshold(logDatasPerLine,timeTakenIndex)
    
    print("Mean:",mean)
    print("Standard Deviation:",stdev)
    print("Threshold:",threshold)

    outputData = ""
    index =0

    # 最後に空行が入っているから調整
    while(index<len(logDatasPerLine)-1):
        timeTaken = int(logDatasPerLine[index].split(" ")[timeTakenIndex])
        if(threshold<=timeTaken):
            outputData += logDatasPerLine[index]+"\n"
        index=index+1

    return outputData

def analyseIISLog(filteredData,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex,startTime,endTime):
    logDatasPerLine=filteredData.split("\n")
    mean,stdev,threshold=getTimeTakenThreshold(logDatasPerLine,timeTakenIndex)

    requestsCount = len(logDatasPerLine)
    index,longCount,errorCount = 0,0,0
    filteredByTimeTakenData,filteredByStatusCodeData = "",""

    # 最後に空行が入っているから調整
    while(index<len(logDatasPerLine)-1):
        timeTaken = int(logDatasPerLine[index].split(" ")[timeTakenIndex])
        sc_status = int(logDatasPerLine[index].split(" ")[statusIndex])

        if(minStatusCode<=sc_status and sc_status<=maxStatusCode):
            filteredByStatusCodeData += logDatasPerLine[index]+"\n"
            errorCount += 1
        if(threshold<=timeTaken):
            filteredByTimeTakenData += logDatasPerLine[index]+"\n"
            longCount +=1
        index+=1
    
    reportText = iisLogAnalyseModules.addReferences()
    reportText += iisLogAnalyseModules.getBasicInfoReport(settings,startTime,endTime)
    reportText += iisLogAnalyseModules.analyseLogFilteredbyStatus(filteredByStatusCodeData,statusIndex,subStatusIndex,win32StatusIndex,requestsCount)
    reportText += iisLogAnalyseModules.analyseLogFilteredbyTimeTaken(filteredByTimeTakenData,requestsCount,mean,stdev,threshold)
    return filteredByStatusCodeData,filteredByTimeTakenData,reportText

def getformats(logData):
    fileformat = logData.split("\n")[3]

    fieldElements = fileformat.split(" ")    
    statusIndex = fieldElements.index("sc-status")-1
    subStatusIndex = fieldElements.index("sc-substatus")-1
    win32StatusIndex = fieldElements.index("sc-win32-status")-1
    timeTakenIndex = fieldElements.index("time-taken")-1
    fileformat += '\n'

    return fileformat,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex

def outputFilterdLogandReport(logData,inputFileName):
    fileformat,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex = getformats(logData)

    startTime,endTime,filteredLogData = filterLogByTerm(logData)
    outputFileName = filterName4Term+inputFileName
    
    fileManager.outputIISFile(fileformat + filteredLogData,outputFileName)
    LogDataFilteredByStatusCode,LogDataFilteredByTimeTaken,reportText = analyseIISLog(filteredLogData,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex,startTime,endTime)
    
    outputFileNameByStatusCode = filterName4Status+outputFileName
    fileManager.outputIISFile(fileformat + LogDataFilteredByStatusCode,outputFileNameByStatusCode)

    outputFileNameByTimeTaken = filterName4Time+outputFileName
    fileManager.outputIISFile(fileformat + LogDataFilteredByTimeTaken,outputFileNameByTimeTaken)
    return str(reportText) 

def removeFields(logData):
    ''' 既に出力済のファイルを読み込んだ時に filter 処理のために #Field を消して成型する用(return:string)'''
    idx = logData.find("#Fields:")
    logData = logData[idx:]
    # 2021 とかの Date ではじまるからそこで分割
    idx = logData.find("20")
    return logData[idx:].split("\n\n")[0]