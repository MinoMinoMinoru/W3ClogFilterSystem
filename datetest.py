import fileManager,FilterManager.httpErrorLogFilterManager as httpErrorLogFilterManager
import datetime as dt

def main():
    # input directoryの先頭ファイルを読み込む
    settings = fileManager.getSetting()
    print("Now Settings")
    print("--------")
    starttime = settings["startTime"]
    
    date_value = dt.datetime.strptime(starttime, '%Y-%m-%d %H:%M')
    print(date_value)
    date_value = date_value + dt.timedelta(minutes=-10)
    print("-10 min",date_value)
    print(type(date_value))

    date_value = date_value.strftime('%Y-%m-%d %H:%M')
    print(type(date_value))



main()