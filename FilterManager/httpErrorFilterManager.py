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

def filterLogByTerm(logData):
    ''' 指定期間でフィルター(input/return:string)'''
    # startTime より後ろを切り取る
    idx = logData.find(settings["startTime"])
    logData = logData[idx:]
    # endTime より前を切り取る
    idx = logData.find(settings["endTime"])
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

def filterLogByFlag(logData,flag,inputFileName):
    # #Fields: date time c-ip c-port s-ip s-port cs-version cs-method cs-uri streamid sc-status s-siteid s-reason s-queuename 
    fileformat = logData.split("\n")[3]
    # fieldElements = fileformat.split(" ")    
    
    # reasonIndex = fieldElements.index("s-reason")-1
    fileformat += '\r'

    if(flag==0):
        ''' 時間でのみフィルター '''
        filteredLogData =filterLogByTerm(logData)
        outputFileName = filterName4Term+inputFileName

        fileManager.outputFile(fileformat + filteredLogData,outputFileName)
