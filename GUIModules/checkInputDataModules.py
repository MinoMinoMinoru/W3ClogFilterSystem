import datetime as dt

def checkDateFormats(input,kind):
    # TODO date の型にあってるかを　try-catch する
    if(len(input)==0):
        return f'- {kind} U input is empty. Please input {kind}.'+'\n'
    else:
        return ""

def checkSelectedLog(input,kind):
    if("." in input):
        # print(f"input {kind} is true")
        return ""
    else :
        return f'- {kind} is NOT selected. Please select {kind}.'+'\n'

def checkEmptyInput(inputStartDate,inputEndDate,inputIISFile,inputHttpErrorFile):
    errorMessage=""
    errorMessage+=checkDateFormats(inputStartDate,"startDate")
    errorMessage+=checkDateFormats(inputEndDate,"endDate")
    errorMessage+=checkSelectedLog(inputIISFile,"IIS Log")
    errorMessage+=checkSelectedLog(inputHttpErrorFile,"HttpError Log")
    return errorMessage

def checkInputsBoforeSubmit(logStartTime,logEndTime,startTime,endTime):
    errorMessage = ""
    try:
        logStartTime,logEndTime = dt.datetime.strptime(logStartTime, '%Y-%m-%d %H:%M:%S'),dt.datetime.strptime(logEndTime, '%Y-%m-%d %H:%M:%S')
        startTime,endTime = dt.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S'),dt.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return 'Please input date as format \'%Y-%m-%d %H:%M\'' 

    if(logStartTime>startTime):
        #TODO フィルターの開始時刻を入力のにする？でもダルイから入れなおしてもらうで良い気がする
        print(f'hogehoge')
    if(endTime<logStartTime):
        errorMessage+=f'- you input later end time than log start time as filter time.'+'\n'
    if(startTime>logEndTime):
        errorMessage+=f'- you input later start time than log end time as filter time.'+'\n'
    if(startTime>endTime):
        errorMessage+=f'- you input later start time than end time.'+'\n'
    # print('errorMessage at checkInputsBoforeSubmit:\n',errorMessage)
    return errorMessage

