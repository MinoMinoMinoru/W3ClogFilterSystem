from statistics import mean,stdev
import fileManager

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

def getTimeTakenThreshold(logData,timeTakenIndex):
    ''' time-taken の平均+標準偏差を返す(input:list,int/return:int)'''
    index =0
    timeTakens=[]

    # 最後に空行が入っているから調整
    while(index<len(logData)-1):
        timeTaken=int(logData[index].split(" ")[timeTakenIndex])
        timeTakens.append(timeTaken)
        index=index+1
    
    print("Mean:",mean(timeTakens))
    print("StDev:",stdev(timeTakens))
    print("Threshold:",int(mean(timeTakens)+stdev(timeTakens)))
    return int(mean(timeTakens)+stdev(timeTakens))

def filterLogByTerm(logData):
    ''' 指定期間でフィルター(input/return:string)'''
    startTime = settings["startTime"]
    endTime = settings["endTime"]
    
    # startTime より後ろを切り取る
    # print(startTime)
    while(True):
        idx = logData.find(startTime)
        if(idx!= -1):
            print("Fitler from " + startTime)
            break
        date_value = dt.datetime.strptime(startTime, '%Y-%m-%d %H:%M')
        date_value = date_value + dt.timedelta(minutes=-1)
        startTime  = date_value.strftime('%Y-%m-%d %H:%M')
        continue

    logData = logData[idx:]

    # endTime より前を切り取る
    # print(endTime)
    while(True):
        idx = logData.find(endTime)
        if(idx!= -1):
            print("Fitler to " + endTime)
            break
        date_value = dt.datetime.strptime(endTime, '%Y-%m-%d %H:%M')
        date_value = date_value + dt.timedelta(minutes=1)
        endTime  = date_value.strftime('%Y-%m-%d %H:%M')
        continue
    # idx = logData.find(settings["endTime"])
    return logData[:idx]

def filterLogByStatusCode(logData,statusIndex):
    ''' ステータス コードでフィルター(input:string,int/return string)'''
    # 1 line 毎に条件を確認するため split
    logDatasPerLine=logData.split("\n")

    minStatusCode = settings["minError"]
    maxStatusCode = settings["maxError"]

    outputData = ""

    index =0
    # 最後に空行が入っているから調整
    while(index<len(logDatasPerLine)-1):
        sc_status = int(logDatasPerLine[index].split(" ")[statusIndex])
        if(minStatusCode<=sc_status and sc_status<=maxStatusCode):
            outputData += logDatasPerLine[index]+"\r"
        index=index+1

    return outputData

def filterLogByTimetaken(logData,timeTakenIndex):
    '''  time-taken でフィルター(input:string,int/return string)'''
    # 1 line 毎に条件を確認するため split
    logDatasPerLine=logData.split("\n")

    threshold=getTimeTakenThreshold(logDatasPerLine,timeTakenIndex)

    outputData = ""

    index =0
    # 最後に空行が入っているから調整
    while(index<len(logDatasPerLine)-1):
        timeTaken = int(logDatasPerLine[index].split(" ")[timeTakenIndex])
        if(threshold<=timeTaken):
            outputData += logDatasPerLine[index]+"\r"
        index=index+1

    return outputData

def filterLogByFlag(logData,flag,inputFileName):

    fileformat = logData.split("\n")[3]
    fieldElements = fileformat.split(" ")    
    
    timeTakenIndex = fieldElements.index("time-taken")-1
    statusIndex = fieldElements.index("sc-status")-1
    fileformat += '\r'

    if(flag==0):
        ''' 時間でのみフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName

        fileManager.outputIISFile(fileformat + filteredLogData,outputFileName)
        # fileManager.outputXlsxFile(fileformat + filteredLogData,outputFileName)

    elif(flag==1):
        ''' 時間でフィルターしたものを Status Code と time-taken それぞれでフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName
        fileManager.outputIISFile(fileformat + filteredLogData+"\r",outputFileName)

        LogDataFilteredByStatusCode = filterLogByStatusCode(filteredLogData,statusIndex)
        outputFileNameByStatusCode = filterName4Status+outputFileName
        fileManager.outputIISFile(fileformat + LogDataFilteredByStatusCode+"\r",outputFileNameByStatusCode)
        
        LogDataFilteredByTimeTaken = filterLogByTimetaken(filteredLogData,timeTakenIndex)
        outputFileNameByTimeTaken = filterName4Time+outputFileName
        fileManager.outputIISFile(fileformat + LogDataFilteredByTimeTaken+"\r",outputFileNameByTimeTaken)

    elif(flag==2):
        ''' 時間と Status Code でフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName
        fileManager.outputIISFile(fileformat + filteredLogData+"\r",outputFileName)

        filteredLogData = filterLogByStatusCode(filteredLogData,statusIndex)
        outputFileName = filterName4Status+outputFileName
        fileManager.outputIISFile(fileformat + filteredLogData+"\r",outputFileName)

    elif(flag==3):
        ''' 時間と time-taken でフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName
        fileManager.outputIISFile(fileformat + filteredLogData+"\r",outputFileName)

        filteredLogData = filterLogByTimetaken(filteredLogData,timeTakenIndex)
        outputFileName = filterName4Time+outputFileName
        fileManager.outputIISFile(fileformat + filteredLogData+"\r",outputFileName)

    elif(flag==4):
        ''' Status Code だけでフィルター '''
        filteredLogData =removeFields(logData)

        filteredLogData = filterLogByStatusCode(filteredLogData,statusIndex)
        outputFileName = filterName4Status+inputFileName
        fileManager.outputIISFile(fileformat + filteredLogData+"\r",outputFileName)
    
    elif(flag==5):
        ''' time-taken だけでフィルター '''
        filteredLogData =removeFields(logData)

        filteredLogData = filterLogByTimetaken(filteredLogData,timeTakenIndex)
        outputFileName = filterName4Time+inputFileName
        fileManager.outputIISFile(fileformat + filteredLogData+"\r",outputFileName)

    elif(flag==-99):
        print("test")
        filteredLogData =filterLogByTerm(logData)
        print(filteredLogData[0])