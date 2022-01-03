from statistics import mean,stdev
import fileManager

''' 初期設定 '''
settings = fileManager.getSetting()
filterName4Term ="[filterted_by_term]"
filterName4Status = "[filterted_by_StatusCode]"
filterName4Time="[filterted_by_time-taken]"
fileformat = "#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port cs-username c-ip cs(User-Agent) cs(Referrer) sc-status sc-substatus sc-win32-status time-taken\r"
''' 初期設定 ここまで'''

def removeFields(logData):
    ''' 既に出力済のファイルを読み込んだ時に filter 処理のために成型する用(return:string)'''
    idx = logData.find("#Fields:")
    logData = logData[idx:]
    # 2021 とかの Date ではじまるからそこで分割
    idx = logData.find("20")
    return logData[idx:].split("\n\n")[0]

def calcTimeTakenThreshold(logData):
    ''' time-taken の平均+標準偏差を返す(input:list/return:int)'''
    index =0
    timeTakens=[]
    # time-taken が後ろから 1 番目の項目
    timeTakenIndex = len(logData[0].split(" "))-1
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
    # startTime より後ろを切り取る
    idx = logData.find(settings["startTime"])
    logData = logData[idx:]
    # endTime より前を切り取る
    idx = logData.find(settings["endTime"])
    return logData[:idx]

def filterLogByStatusCode(logData):
    ''' ステータス コードでフィルター(input/return:string)'''
    # 1 line 毎に条件を確認するため split
    logDatasPerLine=logData.split("\n")

    minStatusCode = settings["minError"]
    maxStatusCode = settings["maxError"]

    # sc-status が後ろから 4 番目の項目
    statusIndex = len(logDatasPerLine[0].split(" "))-4
    outputData = ""

    index =0
    # 最後に空行が入っているから調整
    while(index<len(logDatasPerLine)-1):
        sc_status = int(logDatasPerLine[index].split(" ")[statusIndex])
        if(minStatusCode<=sc_status and sc_status<=maxStatusCode):
            outputData += logDatasPerLine[index]+"\r"
        index=index+1

    return outputData

def filterLogByTimetaken(logData):
    '''  time-taken でフィルター(input/return:string)'''
    # 1 line 毎に条件を確認するため split
    logDatasPerLine=logData.split("\n")

    # threshold = settings["time-taken-threshold"]
    threshold=calcTimeTakenThreshold(logDatasPerLine)

    # time-taken が後ろから 1 番目の項目
    timeTakenIndex = len(logDatasPerLine[0].split(" "))-1
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
    if(flag==0):
        ''' 時間でのみフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName
        fileManager.outputFile(fileformat + filteredLogData,outputFileName)
        print(filteredLogData)
    
    elif(flag==1):
        ''' 時間でフィルターしたものを Status Code と time-taken それぞれでフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName
        fileManager.outputFile(fileformat + filteredLogData+"\r",outputFileName)

        LogDataFilteredByStatusCode = filterLogByStatusCode(filteredLogData)
        outputFileNameByStatusCode = filterName4Status+outputFileName
        fileManager.outputFile(fileformat + LogDataFilteredByStatusCode+"\r",outputFileNameByStatusCode)
        
        LogDataFilteredByTimeTaken = filterLogByTimetaken(filteredLogData)
        outputFileNameByTimeTaken = filterName4Time+outputFileName
        fileManager.outputFile(fileformat + LogDataFilteredByTimeTaken+"\r",outputFileNameByTimeTaken)

    elif(flag==2):
        ''' 時間と Status Code でフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName
        fileManager.outputFile(fileformat + filteredLogData+"\r",outputFileName)

        filteredLogData = filterLogByStatusCode(filteredLogData)
        outputFileName = filterName4Status+outputFileName
        fileManager.outputFile(fileformat + filteredLogData+"\r",outputFileName)

    elif(flag==3):
        ''' 時間と time-taken でフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName
        fileManager.outputFile(fileformat + filteredLogData+"\r",outputFileName)

        filteredLogData = filterLogByTimetaken(filteredLogData)
        outputFileName = filterName4Time+outputFileName
        fileManager.outputFile(fileformat + filteredLogData+"\r",outputFileName)

    elif(flag==4):
        ''' Status Code だけでフィルター '''
        filteredLogData =removeFields(logData)

        filteredLogData = filterLogByStatusCode(filteredLogData)
        outputFileName = filterName4Status+inputFileName
        fileManager.outputFile(fileformat + filteredLogData+"\r",outputFileName)
    
    elif(flag==5):
        ''' time-taken だけでフィルター '''
        filteredLogData =removeFields(logData)

        filteredLogData = filterLogByTimetaken(filteredLogData)
        outputFileName = filterName4Time+inputFileName
        fileManager.outputFile(fileformat + filteredLogData+"\r",outputFileName)