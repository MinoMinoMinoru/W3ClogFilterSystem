import FilterModules.fileManager as fileManager,FilterModules.iisLogFilterModules as iisLogFilterModules
import os

def main():
    filelist=os.listdir("./input/iislog/")
    print("Filter next log:",filelist[0])

    # input directoryの先頭ファイルを読み込む
    inputFileName = filelist[0]
    logData = fileManager.readLogFile("./input/iislog/"+inputFileName)

    settings = fileManager.getSetting()
    print("Now Settings")
    print("--------")
    print("Term: ",settings["startTime"] +"～" + settings["endTime"])
    print("StatusCode: ",str(settings["minError"]) +"～" + str(settings["maxError"]))
    print("OutPut Excel(.xlsx) File: ", settings["Output2Excel"] )
    print("--------")
    descriptions = fileManager.readLogFile("./FilterModules/resources/description.txt")
    print(descriptions)

    while(True):
        inputString = input("次のモードで実行:")
        try:
            flag = int(inputString)
            print(flag)
            if(flag<len(descriptions.split("\n"))-1):
                iisLogFilterModules.filterLogByFlag(logData,flag,inputFileName)
                break
            else:
                print(str(len(descriptions.split("\n"))-2)+"以下の整数を入力してください。")
        except ValueError:
            print("int を入力してくださいな")
            print(ValueError)
    
    print("Finished")

main()