import tkinter,os
import FilterModules.fileManager as fileManager
import FilterModules.getReports as getReports
import GUIModules.checkInputDataModules as checkInputDataModules

class Application(tkinter.Frame):
    def __init__(self,root=None):
        super().__init__(root,width=840,height=640,borderwidth=1,relief='groove')

        self.root=root
        self.pack()
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        self.ShowTermChoice()
        self.IISLogTerm()
        self.httpErrorLogTerm()
        self.showBUttons()

        self.testTextBoxs()

    def showBUttons(self):
        quit_btn = tkinter.Button(self,text="close Window")
        quit_btn['command']=self.root.destroy
        quit_btn.pack(side="bottom")

        submit_btn = tkinter.Button(self,text='Start Filtering')
        submit_btn['command']=self.submit
        submit_btn.pack()

    def ShowTermChoice(self):
        self.TermMessage = tkinter.Message(self,width=350,text='Input fiter UTC terms : ex)2022-12-07 06:00 - 2022-12-07 07:00')
        self.TermMessage.pack()

        self.startDateBox = tkinter.Entry(self,width=100)
        self.startDateBox.pack()

        self.endDateBox = tkinter.Entry(self,width=100)
        self.endDateBox.pack()

    def IISLogTerm(self):
        self.iisFiles=[]
        inputIISLogFiles= os.listdir("./input/iislog/")

        self.iisSelectMessage=tkinter.Message(self,width=300,text="Select IIS Log")
        self.iisSelectMessage.pack()
        self.SelectedIIS = tkinter.Message(self,width=350,text='IIS log is NOT selected',background="red")
        self.SelectedIIS.pack()

        # get file lists
        for inputIISLogFileName in inputIISLogFiles:
            iisLogData = fileManager.readLogFile("./input/iislog/"+inputIISLogFileName)
            logFileTerm = fileManager.getLogTime(iisLogData)
            self.iisFiles.append(f'{inputIISLogFileName}|{logFileTerm}')

        self.list_iis_items =tkinter.StringVar(value=self.iisFiles)
        self.list_iis_box = tkinter.Listbox(self,listvariable=self.list_iis_items,width=100)
        self.list_iis_box.bind('<<ListboxSelect>>', lambda e:self.checkIISFilesList())
        self.list_iis_box.pack()

    def httpErrorLogTerm(self):
        self.httpErrorLogFiles=[]
        inputHttpErrorLogFiles= os.listdir("./input/httperrorlog/")

        self.HttpErrorSelectMessage=tkinter.Message(self,width=300,text="Select HttpError Log")
        self.HttpErrorSelectMessage.pack()
        self.SelectedHttpError = tkinter.Message(self,width=350,text='HTTP ERROR log is NOT selected',background="red")
        self.SelectedHttpError.pack()

        # get file lists
        for inputHttpErrorLogFileName in inputHttpErrorLogFiles:
            httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
            logFileTerm = fileManager.getLogTime(httpErrorLogData)
            self.httpErrorLogFiles.append(f'{inputHttpErrorLogFileName}|{logFileTerm}')

        self.list_httperror_items =tkinter.StringVar(value=self.httpErrorLogFiles)
        self.list_httpError_box = tkinter.Listbox(self,listvariable=self.list_httperror_items,width=100)
        self.list_httpError_box.bind('<<ListboxSelect>>', lambda e:self.checkHttpErrorFilesList())
        self.list_httpError_box.pack()

    def checkIISFilesList(self):
        self.selected_iis_index = self.list_iis_box.curselection()[0]
        self.SelectedIIS['text']=self.iisFiles[self.selected_iis_index].split("|")[0]
        self.SelectedIIS['background'] = "lightgreen"
        self.SelectedIIS.pack()
    
    def checkHttpErrorFilesList(self):
        self.selected_httperror_index = self.list_httpError_box.curselection()[0]
        self.SelectedHttpError['text'] = self.httpErrorLogFiles[self.selected_httperror_index].split("|")[0]
        self.SelectedHttpError['background'] = "lightgreen"
        self.SelectedHttpError.pack()

    def submit(self):
        # TODO 確認ダイアログを作る(別メソッドのが良さそう)
        inputIISLogFileName = self.SelectedIIS['text']
        inputHttpErrorLogFileName = self.SelectedHttpError['text']
        startTime,endTime = self.startDateBox.get(),self.endDateBox.get()

        self.submitMessage = tkinter.Message(self,width=350,text='Now Filtering')
        self.submitMessage.pack()

        getReports.getReports(inputIISLogFileName,inputHttpErrorLogFileName,startTime,endTime)

        self.submitMessage['text']='Completed!'
        self.submitMessage['background']='lightgreen'
        self.submitMessage.pack()

    def testTextBoxs(self):
        test_btn = tkinter.Button(self,text='Test output textbox')
        test_btn['command']= self.checkInputs
        test_btn.pack()
        
    def checkInputs(self):
        # len(errorMessage) が 0 だとエラーなし
        errorMessage=""
        
        errorMessage +=checkInputDataModules.checkEmptyInput(self.startDateBox.get(),self.endDateBox.get(),self.SelectedIIS['text'],self.SelectedHttpError['text'])

        # errorMessage +=self.getLogTerms()
        if(len(errorMessage)==0):
            errorMessage +=self.getLogTerms()
        else :
            print(errorMessage)
        if(len(errorMessage)==0):
            print("There is no error")
        else :
            print(errorMessage)
            
        # return warningMessage

    def getLogTerms(self):
        term = self.iisFiles[self.selected_iis_index].split("|")[1].split(" ~ ")
        logStart,logEnd = term[0],term[1]
        startTime,endTime = self.startDateBox.get()+":00",self.endDateBox.get()+":00"
        return checkInputDataModules.checkInputsBoforeSubmit(logStart,logEnd,startTime,endTime)

root = tkinter.Tk()
root.title('Filter Log App')
root.geometry('1200x900')

app = Application(root=root)
app.mainloop()