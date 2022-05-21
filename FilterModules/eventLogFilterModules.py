import datetime as dt
import Evtx.Evtx as evtx
# from xml.etree import ElementTree
# from lxml import etree

import FilterModules.fileManager as fileManager

''' 初期設定 '''
settings = fileManager.getSetting()
filterName4Term ="[filterted_by_term]"
filterName4Status = "[filterted_by_StatusCode]"
filterName4Time="[filterted_by_time-taken]"
''' 初期設定 ここまで'''

schema = "http://schemas.microsoft.com/win/2004/08/events/event"


def getEventElmInfo(elm):
    event = elm.xpath("//event:EventData",namespaces={"event": schema})[0].xpath("//event:Data", namespaces={"event":schema})[0].text
    if(event is None):
        event = "There is no Detail at this event\n"
    
    provider = elm.xpath("//event:Provider",namespaces={"event":schema})[0].get("Name")
    if(provider is None): 
        provider = "There is no Provider at this event\n"

    level = elm.xpath("//event:Level", namespaces={"event":schema})[0].text
    return event,provider,level

def CheckProvider(provider):
    flag = False
    if(provider == 'Application Error' or provider == 'Windows Error Reporting'):
        flag = True
    # elif(provider == 'MsiInstaller'):
    #     print("Match Provider")
    #     flag = True
    return flag

def setFilterDateTerm():
    startTime,endTime = settings['startTime'],settings['endTime']
    timeZone = int(settings['eventLogTimeZOne'])

    startTime = dt.datetime.strptime(startTime, '%Y-%m-%d %H:%M')
    startTime = startTime + dt.timedelta(hours=timeZone)
    endTime = dt.datetime.strptime(endTime, '%Y-%m-%d %H:%M')
    endTime = endTime + dt.timedelta(hours=timeZone)

    return startTime,endTime

def filterApplicationEvents(applicationEventLogFile):
    startTime,endTime = setFilterDateTerm()
    outputText = "createdTime,level,Provider,Event\n"
    exceptionsOutputText = "createdTime,level,Provider,Event\n"

    with evtx.Evtx(applicationEventLogFile) as log:
        index = 1
        for record in log.records():
            elm = log.get_record(index).lxml()
            # root = etree.tostring(elm, pretty_print=True).decode("UTF-8")
            
            createdTime = elm.xpath("//event:TimeCreated",namespaces={"event":schema})[0].get("SystemTime")
            idx = createdTime.find(".")
            createdTime = dt.datetime.strptime(createdTime[:idx], '%Y-%m-%d %H:%M:%S')
            
            if(createdTime > endTime):
                print("Over time")
                fileManager.outputEventReport(outputText,"applicationEvetlog.log")
                fileManager.outputEventReport(exceptionsOutputText,"specificApplicationEvetlog.log")
                break

            elif(startTime <= createdTime and createdTime <= endTime):
                event,provider,level = getEventElmInfo(elm)
                outputText += createdTime.strftime('%Y-%m-%d %H:%M:%S') +","+level+","+provider+","+event

                if(int(level)<4):
                    exceptionsOutputText+= createdTime.strftime('%Y-%m-%d %H:%M:%S') +","+level+","+provider+","+event
                    print("level match")
                elif(CheckProvider(provider)==True):
                    exceptionsOutputText+= createdTime.strftime('%Y-%m-%d %H:%M:%S') +","+level+","+provider+","+event

            index += 1

def filterLogByFlag(logData,flag,inputFileName):

    fileformat = logData.split("\n")[3]
    fieldElements = fileformat.split(" ")    
    statusIndex = fieldElements.index("sc-status")-1
    subStatusIndex = fieldElements.index("sc-substatus")-1
    win32StatusIndex = fieldElements.index("sc-win32-status")-1
    timeTakenIndex = fieldElements.index("time-taken")-1
    fileformat += '\n'

    startTime,endTime,filteredLogData =filterLogByTerm(logData)
    outputFileName = filterName4Term+inputFileName

    if(flag==0):
        ''' 時間でのみフィルター '''
        fileManager.outputIISFile(fileformat + filteredLogData,outputFileName)


    elif(flag==-99):
        print("test flag")
        filteredByStatusCodeData,filteredByTimeTakenData,reportText = analyseIISLog(filteredLogData,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex,startTime,endTime)
        return str(reportText)
    
    elif(flag==100):
        fileManager.outputIISFile(fileformat + filteredLogData,outputFileName)
        LogDataFilteredByStatusCode,LogDataFilteredByTimeTaken,reportText = analyseIISLog(filteredLogData,statusIndex,subStatusIndex,win32StatusIndex,timeTakenIndex,startTime,endTime)
        
        outputFileNameByStatusCode = filterName4Status+outputFileName
        fileManager.outputIISFile(fileformat + LogDataFilteredByStatusCode+"\n",outputFileNameByStatusCode)

        outputFileNameByTimeTaken = filterName4Time+outputFileName
        fileManager.outputIISFile(fileformat + LogDataFilteredByTimeTaken+"\n",outputFileNameByTimeTaken)
        return str(reportText) 