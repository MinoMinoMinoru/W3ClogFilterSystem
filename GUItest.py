import tkinter
import os
import FilterModules.fileManager as fileManager
import FilterModules.iisLogFilterModules as iisLogFilterModules
import FilterModules.eventLogFilterModules as eventLogFilter
import FilterModules.httpErrorLogFilterModules as httpErrorLogFilterModules


class Application(tkinter.Frame):
    def __init__(self,root=None):
        super().__init__(root,width=840,height=640,borderwidth=1,relief='groove')

        self.root=root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        quit_btn = tkinter.Button(self)
        quit_btn['text']="close"
        quit_btn['command']=self.root.destroy
        quit_btn.pack(side="bottom")

        self.ShowTermChoice()
        self.IISLogTerm()
        self.httpErrorLogTerm()
        self.showChosen()

        submit_btn = tkinter.Button(self)
        submit_btn['text']='submit'
        submit_btn['command']=self.submit
        submit_btn.pack()

    def showChosen(self):
        self.chosenIIS = tkinter.Message(self,width=350)
        self.chosenIIS['text'] = 'IIS log is NOT selected'
        self.chosenIIS.pack()

        self.chosenHttpError = tkinter.Message(self,width=350)
        self.chosenHttpError['text'] = 'HTTP ERROR log is NOT selected'
        self.chosenHttpError.pack()

    def ShowTermChoice(self):
        self.TermMessage = tkinter.Message(self,width=350)
        self.TermMessage['text'] = 'Input fiter UTC tems ex)2022-12-07 06:00 - 2022-12-07 07:00'
        self.TermMessage.pack()

        self.startDateBox = tkinter.Entry(self)
        self.startDateBox['width'] =100
        self.startDateBox.pack()

        self.endDateBox = tkinter.Entry(self)
        self.endDateBox['width'] =100
        self.endDateBox.pack()

    def IISLogTerm(self):
        self.iisFiles=[]
        inputIISLogFiles= os.listdir("./input/iislog/")

        self.iisChoseMessage=tkinter.Message(self,width=300)
        self.iisChoseMessage['text'] = "Choose iis Log"
        self.iisChoseMessage.pack()

        for inputIISLogFileName in inputIISLogFiles:
            iisLogData = fileManager.readLogFile("./input/iislog/"+inputIISLogFileName)
            logFileTerm = fileManager.getLogTime(iisLogData)
            print(f'{inputIISLogFileName}|{logFileTerm}')
            self.iisFiles.append(f'{inputIISLogFileName}|{logFileTerm}')

        self.list_iis_items =tkinter.StringVar(value=self.iisFiles)
        self.list_iis_box = tkinter.Listbox(self,listvariable=self.list_iis_items,width=100)
        self.list_iis_box.bind('<<ListboxSelect>>', lambda e:self.checkIISFilesList())
        self.list_iis_box.pack()

    def httpErrorLogTerm(self):
        self.httpErrorLogFiles=[]
        inputHttpErrorLogFiles= os.listdir("./input/httperrorlog/")

        # HttpErrorLog Fiiles
        self.HttpErrorChoseMessage=tkinter.Message(self,width=300)
        self.HttpErrorChoseMessage['text'] = "Choose HttpError Log"
        self.HttpErrorChoseMessage.pack()

        for inputHttpErrorLogFileName in inputHttpErrorLogFiles:
            httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
            logFileTerm = httpErrorLogFilterModules.getLogTime(httpErrorLogData)
            # print(f'{inputHttpErrorLogFileName}|{logFileTerm}')
            self.httpErrorLogFiles.append(f'{inputHttpErrorLogFileName}|{logFileTerm}')

        self.list_httperror_items =tkinter.StringVar(value=self.httpErrorLogFiles)
        self.list_httpError_box = tkinter.Listbox(self,listvariable=self.list_httperror_items,width=100)
        self.list_httpError_box.bind('<<ListboxSelect>>', lambda e:self.checkHttpErrorFilesList())
        self.list_httpError_box.pack()

    def input_handler(self):
        text = self.text_box.get()
        self.message['text'] = text

    def checkIISFilesList(self):
        self.selected_iis_index = self.list_iis_box.curselection()[0]
        self.chosenIIS['text']=self.iisFiles[self.selected_iis_index].split("|")[0]
        self.chosenIIS.pack()
    
    def checkHttpErrorFilesList(self):
        self.selected_httperror_index = self.list_httpError_box.curselection()[0]
        self.chosenHttpError['text'] = self.httpErrorLogFiles[self.selected_httperror_index].split("|")[0]
        self.chosenHttpError.pack()

    def submit(self):
        inputIisLogFileName = self.chosenIIS['text']
        inputHttpErrorLogFileName = self.chosenHttpError['text']
        startTime = self.startDateBox.get()
        endTime = self.endDateBox.get()

        print("inputIisLogFileName",inputIisLogFileName)
        print("startTime",startTime)
        print("endTime",endTime)

        issReport = getIISLogReport(inputIisLogFileName,startTime,endTime)
        httpErrorReport = getHttpErrorReport(inputHttpErrorLogFileName,startTime,endTime)
        
        reportText = issReport + httpErrorReport
        fileManager.outputReport(reportText,"SimpleReport.md")

def getIISLogReport(file,startTime,endTime):
    inputIisLogFileName =file
    iisLogData = fileManager.readLogFile("./input/iislog/"+inputIisLogFileName)
    print("Filter next iislog:",inputIisLogFileName)
    return iisLogFilterModules.outputFilterdLogandReport(iisLogData,inputIisLogFileName,startTime,endTime)

def getHttpErrorReport(file,startTime,endTime):
    # inputHttpErrorLogFileName = os.listdir("./input/httperrorlog/")[0]
    inputHttpErrorLogFileName = file
    httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
    print("Filter next httperrorlog:",inputHttpErrorLogFileName)
    return httpErrorLogFilterModules.outputFilterdLogandReport(httpErrorLogData,inputHttpErrorLogFileName,startTime,endTime)
        

root = tkinter.Tk()
root.title('test App')
root.geometry('1200x900')

app = Application(root=root)
app.mainloop()

# root.mainloop()