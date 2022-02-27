import json
import pandas as pd

def readLogFile(file_name):
    f = open(file_name, 'r',encoding="utf-8")
    data = f.read()
    f.close()
    return data

def outputFile(write_text, write_file):
    ''' ファイル書き込み '''
    write_file = './output/' +write_file
    with open(write_file,'a') as file:
        file.write(write_text)
    print("Output the file : "+write_file)

def outputXlsxFile(write_text, write_file):
    ''' .xlsx ファイル書き込み '''
    '''pandas.core.frame.DataFrame という type を使うので csv にしてから変換'''
    write_file = './output/' +write_file +'.csv'
    write_text = write_text.replace(" ",",")
    with open(write_file,'a') as file:
        file.write(write_text)
    data = pd.read_csv(write_file)
    data.to_excel(write_file+'.xlsx', encoding='utf-8')
    print("Output the file : "+write_file)

def getSetting():
    ''' jsonファイルから情報取得 '''
    f = open("setting.json", 'r')
    json_body = json.load(f)
    f.close()
    return json_body