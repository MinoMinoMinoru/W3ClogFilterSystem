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
    if(elm.xpath("//event:EventData",namespaces={"event": schema})[0].xpath("//event:Data", namespaces={"event":schema})[0].text):
        event = elm.xpath("//event:EventData",namespaces={"event": schema})[0].xpath("//event:Data", namespaces={"event":schema})[0].text
    else:
        event = "There is no Detail at this event\n"

    if(elm.xpath("//event:Provider",namespaces={"event":schema})[0].get("Name")):    
        provider = elm.xpath("//event:Provider",namespaces={"event":schema})[0].get("Name")
    else: 
        provider = "There is no Provider at this event\n"
    # if(elm.xpath("//event:Level", namespaces={"event":schema})[0].text):
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
    timeZone = int(settings['eventLogTimeZone'])

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
        index = len(list(log.records()))
        
        for record in log.records():
            elm = log.get_record(index).lxml()

            createdTime = elm.xpath("//event:TimeCreated",namespaces={"event":schema})[0].get("SystemTime")
            idx = createdTime.find(".")
            createdTime = dt.datetime.strptime(createdTime[:idx], '%Y-%m-%d %H:%M:%S')
            
            if(createdTime < startTime):
                print("Over time")
                fileManager.outputEventReport(outputText,"applicationEvetlog.log")
                fileManager.outputEventReport(exceptionsOutputText,"/specificApplicationEvetlog.log")
                break

            elif(startTime <= createdTime and createdTime <= endTime):
                print(createdTime)
                print(elm.xpath("//event:EventData",namespaces={"event": schema})[0])
                event,provider,level = getEventElmInfo(elm)
                outputText += createdTime.strftime('%Y-%m-%d %H:%M:%S') +","+level+","+provider+","+event
                
                if(int(level)<4):
                    exceptionsOutputText+= createdTime.strftime('%Y-%m-%d %H:%M:%S') +","+level+","+provider+","+event
                    print("level match")
                elif(CheckProvider(provider)):
                    exceptionsOutputText+= createdTime.strftime('%Y-%m-%d %H:%M:%S') +","+level+","+provider+","+event
            
            index -= 1