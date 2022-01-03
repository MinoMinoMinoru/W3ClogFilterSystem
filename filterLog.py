import fileManager,filterManager
import os

def main():
    filelist=os.listdir("./input")
    print("次のファイルをフィルターします:",filelist[0])
    # input directoryの先頭ファイルを読み込む
    inputFileName = filelist[0]
    logData = fileManager.readLogFile("./input/"+inputFileName)

    descriptions = fileManager.readLogFile("description.txt")
    print(descriptions)

    while(True):
        inputString = input("次のモードで実行:")
        try:
            flag = int(inputString)
            print(flag)
            if(flag<len(descriptions.split("\n"))-1):
                filterManager.filterLogByFlag(logData,flag,inputFileName)
                break
            else:
                print(str(len(descriptions.split("\n"))-2)+"以下の整数を入力してください。")
        except ValueError:
            print("int を入力してくださいな")
    
    print("Finished")

main()