import json
import pandas as pd

def readLogFile(file_name):
    f = open(file_name, 'r',encoding="utf-8")
    data = f.read()
    f.close()
    return data

def outputReport(writeText, writeFile):
    writeFile = './output/' + writeFile
    with open(writeFile,'w') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)

def outputEventReport(writeText, writeFile):
    writeFile = './output/' + writeFile
    with open(writeFile,'w',encoding='UTF-8') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)

def outputHttpErrorFile(writeText, writeFile):
    writeFile = './output/httperrorlog/' + writeFile
    with open(writeFile,'w') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)

def outputIISFile(writeText, writeFile):
    xlsxFlag = getSetting()["Output2Excel"]
    if xlsxFlag==True:
        print("Output .xlsx")
        outputPlaneLogFile(writeText, writeFile)
        outputXlsxFile(writeText, writeFile)
    else:
        print("Output plane log")
        outputPlaneLogFile(writeText, writeFile)

def outputPlaneLogFile(writeText, writeFile):
    writeFile = './output/iislog/' + writeFile
    with open(writeFile,'w',encoding='UTF-8') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)

def outputXlsxFile(writeText, writeFile):
    ''' .xlsx ファイル書き込み '''
    '''pandas.core.frame.DataFrame という type を使うので csv にしてから変換'''
    writeFile = './output/iislog/'+writeFile +'.csv'
    writeText = writeText.replace(" ",",")
    with open(writeFile,'w',encoding='UTF-8') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)
    data = pd.read_csv(writeFile)
    data.to_excel(writeFile+'.xlsx')
    print("Output the file : "+writeFile+'.xlsx')

def getSetting():
    ''' jsonファイルから情報取得 '''
    f = open("./setting.json", 'r')
    json_body = json.load(f)
    f.close()
    return json_body

def getLogTime(logData):
    ''' get first & end Date of httpError log file '''
    firstTime = logData.split("\n")[4].split(" ")
    endTime = logData.split("\n")[-2].split(" ")
    logFileTerm = f'{firstTime[0]} {firstTime[1]} ~ {endTime[0]} {endTime[1]}'
    return logFileTerm