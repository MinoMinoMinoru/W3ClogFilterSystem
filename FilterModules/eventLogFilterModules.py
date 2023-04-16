import datetime
import pandas as pd
from lxml import etree
import Evtx.Evtx as evtx

schema = "http://schemas.microsoft.com/win/2004/08/events/event"

# 
def outputEventFile(writeText,writeFile):
    writeFile ='./output/' + writeFile
    with open(writeFile,'w',encoding='UTF-8') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)
    data = pd.read_csv(writeFile)
    data.to_excel(writeFile+'.xlsx')
    print("Output the file : "+writeFile+'.xlsx')


def getFilteredAppEventlog(inputFilename,startTime,endTime,outputFile):
    
    starttime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
    endtime = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    print("startTime : ",startTime)
    print("endTime : ",endtime)

    outputText = "Level,createdTime,Provider,EventID,Event"+'\n'

    with evtx.Evtx(inputFilename) as log:

        for record in log.records():

            elm = record.lxml()
            event,createdTime,provider,level,eventID = getAppEventInfo(elm)

            eventDateTime = datetime.datetime.strptime(createdTime.split(".")[0], '%Y-%m-%d %H:%M:%S')

            if(eventDateTime>starttime):
                if(provider.find('ASP.NET')!=-1):
                    print(f'{level},{createdTime},{provider},{event}'+'\n')

                if(eventDateTime>endtime):
                    print("Break by timestamp")
                    # print(f'{level},{createdTime},{provider},{event}')
                    break
                
                if(level<4):
                    ''' If warning or errror'''
                    outputText += f'{convetEventLevel(level)},{createdTime},{provider},{eventID},{cleanEvent(event)}'+'\n'
    
        outputEventFile(outputText,outputFile)
    

def getAppEventInfo(elm):
    # event = elm.xpath("//event:EventData",namespaces={"event": schema})[0].xpath("//event:Data", namespaces={"event":schema})[0].text
    event = elm.xpath("//event:Data",namespaces={"event": schema})
    if(len(event) == 0):
        event ="Null event"
    elif(type(event) is list):
        event = str(event[0].text).replace(",","|").replace("\n","|")
    else:
        print(type(event))
        event=event
    createdTime = elm.xpath("//event:TimeCreated",namespaces={"event":schema})[0].get("SystemTime")
    provider = elm.xpath("//event:Provider",namespaces={"event":schema})[0].get("Name")
    level = int(elm.xpath("//event:Level", namespaces={"event":schema})[0].text)
    eventID = int(elm.xpath("//event:EventID", namespaces={"event":schema})[0].text)
    return event,createdTime,provider,level,eventID

def convetEventLevel(rawLevel):
    if(rawLevel==4):
        return 'Information'
    elif(rawLevel==3):
        return 'Warning'
    elif(rawLevel==2):
        return 'Error'
    else:
        return 'Critical'

def cleanEvent(event):
    event = event.replace('<string>','')
    event = event.replace('</string>','')
    return event