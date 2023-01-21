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
    ''' Return Average and Stdev of time-taken (input:list,int/return:int)'''
    timeTakens=[]

    for log in logData:
        timeTaken=int(log.split(" ")[timeTakenIndex])
        timeTakens.append(timeTaken)

    return int(mean(timeTakens)),int(stdev(timeTakens)),int(mean(timeTakens)+stdev(timeTakens))

def filterLogByTerm(logData,startTime,endTime):
    ''' 指定期間でフィルター(input/return:string)'''
    # Cut after startTime
    startTime,idx = getMatchTime(logData,startTime,-1)
    logData = logData[idx:]
    # Cut before endTime
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

def analyseIISLog(filteredData,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex,startTime,endTime):
    logDatasPerLine=filteredData.split("\n")
    logDatasPerLine.pop()
    mean,stdev,threshold=getTimeTakenThreshold(logDatasPerLine,timeTakenIndex)

    requestsCount = len(logDatasPerLine)
    slowCount,errorCount = 0,0
    filteredByTimeTakenData,filteredByStatusCodeData = "",""

    for log in logDatasPerLine:
        timeTaken = int(log.split(" ")[timeTakenIndex])
        sc_status = int(log.split(" ")[statusIndex])

        if(minStatusCode<=sc_status and sc_status<=maxStatusCode):
            filteredByStatusCodeData += log+"\n"
            errorCount += 1
        if(threshold<=timeTaken):
            filteredByTimeTakenData += log+"\n"
            slowCount +=1

    reportText = iisLogAnalyseModules.addReferences()
    reportText += iisLogAnalyseModules.getBasicInfoReport(settings,startTime,endTime)
    reportText += iisLogAnalyseModules.analyseLogFilteredbyStatus(filteredByStatusCodeData,statusIndex,subStatusIndex,win32StatusIndex,requestsCount)
    reportText += iisLogAnalyseModules.analyseLogFilteredbyTimeTaken(filteredByTimeTakenData,requestsCount,mean,stdev,threshold)
    return filteredByStatusCodeData,filteredByTimeTakenData,reportText

def getformats(logData):
    ''' get Log format(Fields) '''
    fileformat = logData.split("\n")[3]

    fieldElements = fileformat.split(" ")    
    statusIndex = fieldElements.index("sc-status")-1
    subStatusIndex = fieldElements.index("sc-substatus")-1
    win32StatusIndex = fieldElements.index("sc-win32-status")-1
    timeTakenIndex = fieldElements.index("time-taken")-1
    fileformat += '\n'

    return fileformat,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex

def outputFilterdLogandReport(logData,inputFileName,startTime,endTime):
    ''' filter term/status/time-takens and output report file'''
    fileformat,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex = getformats(logData)
    startTime,endTime,filteredLogData = filterLogByTerm(logData,startTime,endTime)

    outputFileName = filterName4Term+inputFileName
    outputFileNameByStatusCode,outputFileNameByTimeTaken = filterName4Status+outputFileName,filterName4Time+outputFileName
    
    fileManager.outputIISFile(fileformat + filteredLogData,outputFileName)
    LogDataFilteredByStatusCode,LogDataFilteredByTimeTaken,reportText = analyseIISLog(filteredLogData,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex,startTime,endTime)
    
    fileManager.outputIISFile(fileformat + LogDataFilteredByStatusCode,outputFileNameByStatusCode) 
    fileManager.outputIISFile(fileformat + LogDataFilteredByTimeTaken,outputFileNameByTimeTaken)
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
    logDatasPerLine.pop()
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