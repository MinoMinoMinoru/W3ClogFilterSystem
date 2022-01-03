import json

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

def getSetting():
    ''' jsonファイルから情報取得 '''
    f = open("setting.json", 'r')
    json_body = json.load(f)
    f.close()
    return json_body