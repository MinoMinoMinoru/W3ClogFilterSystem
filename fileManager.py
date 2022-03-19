import json
import pandas as pd

def readLogFile(file_name):
    f = open(file_name, 'r',encoding="utf-8")
    data = f.read()
    f.close()
    return data

def outputHttpErrorFile(writeText, writeFile):
    ''' ファイル書き込み '''
    writeFile = './output/httperrorlog/' + writeFile
    with open(writeFile,'a') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)

def outputIISFile(writeText, writeFile):
    xlsxFlag = getSetting()["Output2Excel"]
    if xlsxFlag==True:
        print("Output .xlsx")
        outputLogFile(writeText, writeFile)
        outputXlsxFile(writeText, writeFile)
    else:
        print("Output plane log")
        outputLogFile(writeText, writeFile)

def outputLogFile(writeText, writeFile):
    ''' ファイル書き込み '''
    writeFile = './output/iislog/' + writeFile
    with open(writeFile,'a') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)

def outputXlsxFile(writeText, writeFile):
    ''' .xlsx ファイル書き込み '''
    '''pandas.core.frame.DataFrame という type を使うので csv にしてから変換'''
    writeFile = './output/iislog/'+writeFile +'.csv'
    writeText = writeText.replace(" ",",")
    with open(writeFile,'a') as file:
        file.write(writeText)
    print("Output the file : "+writeFile)
    data = pd.read_csv(writeFile)
    data.to_excel(writeFile+'.xlsx', encoding='utf-8')
    print("Output the file : "+writeFile+'.xlsx')

def getSetting():
    ''' jsonファイルから情報取得 '''
    f = open("setting.json", 'r')
    json_body = json.load(f)
    f.close()
    return json_body