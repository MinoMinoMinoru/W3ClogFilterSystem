import tkinter,os
from tkinter import messagebox
import FilterModules.fileManager as fileManager
import AnalyseModules.getReports as getReports
import GUIModules.checkInputDataModules as checkInputDataModules

class Application(tkinter.Frame):
    def __init__(self,root=None):
        super().__init__(root,width=840,height=640,borderwidth=1,relief='groove')

        self.root=root
        self.pack(anchor=tkinter.W)
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        self.ShowTermChoice()
        self.ShowIISLogList()
        self.ShowHttpErrorLogList()
        self.showBUttons()

    def showBUttons(self):
        # quit_btn = tkinter.Button(self,text="close Window")
        # quit_btn['command']=self.root.destroy
        # quit_btn.pack(anchor=tkinter.W)

        submit_btn = tkinter.Button(self,text='Start Filtering')
        submit_btn['command']=self.submit
        submit_btn.pack(anchor=tkinter.W)

    def ShowTermChoice(self):
        self.TermMessage = tkinter.Message(self,width=350,text='Input fiter UTC terms : ex)2022-12-07 06:00 - 2022-12-07 07:00')
        self.TermMessage.pack(anchor=tkinter.W)

        self.startDateBox = tkinter.Entry(self,width=100)
        self.startDateBox.insert(0,'2022-12-07 06:00')
        self.startDateBox.pack(anchor=tkinter.W)

        self.endDateBox = tkinter.Entry(self,width=100)
        self.endDateBox.insert(0,'2022-12-07 07:00')
        self.endDateBox.pack(anchor=tkinter.W)

    def ShowIISLogList(self):
        self.iisFiles=['None']
        
        inputIISLogFiles= os.listdir("./input/iislog/")
        self.iisSelectMessage=tkinter.Message(self,width=300,text="Select IIS Log from the following list.")
        self.iisSelectMessage.pack(anchor=tkinter.W)
        self.SelectedIIS = tkinter.Message(self,width=350,text='IIS log is NOT selected',background="red")
        self.SelectedIIS.pack(anchor=tkinter.W)

        # get file lists
        for inputIISLogFileName in inputIISLogFiles:
            iisLogData = fileManager.readLogFile("./input/iislog/"+inputIISLogFileName)
            logFileTerm = fileManager.getLogTime(iisLogData)
            self.iisFiles.append(f'{inputIISLogFileName}|{logFileTerm}')

        self.list_iis_items =tkinter.StringVar(value=self.iisFiles)
        self.list_iis_box = tkinter.Listbox(self,listvariable=self.list_iis_items,width=100)
        self.list_iis_box.bind('<<ListboxSelect>>', lambda e:self.checkIISFilesList())
        self.list_iis_box.pack(anchor=tkinter.W)

    def ShowHttpErrorLogList(self):
        self.httpErrorLogFiles=['None']
        
        inputHttpErrorLogFiles= os.listdir("./input/httperrorlog/")
        self.HttpErrorSelectMessage=tkinter.Message(self,width=300,text="Select HttpError Log from the following list.")
        self.HttpErrorSelectMessage.pack(anchor=tkinter.W)
        self.SelectedHttpError = tkinter.Message(self,width=350,text='HTTP ERROR log is NOT selected',background="red")
        self.SelectedHttpError.pack(anchor=tkinter.W)

        # get file lists
        for inputHttpErrorLogFileName in inputHttpErrorLogFiles:
            httpErrorLogData = fileManager.readLogFile("./input/httperrorlog/"+inputHttpErrorLogFileName)
            logFileTerm = fileManager.getLogTime(httpErrorLogData)
            self.httpErrorLogFiles.append(f'{inputHttpErrorLogFileName}|{logFileTerm}')

        self.list_httperror_items =tkinter.StringVar(value=self.httpErrorLogFiles)
        self.list_httpError_box = tkinter.Listbox(self,listvariable=self.list_httperror_items,width=100)
        self.list_httpError_box.bind('<<ListboxSelect>>', lambda e:self.checkHttpErrorFilesList())
        self.list_httpError_box.pack(anchor=tkinter.W)

    def checkIISFilesList(self):
        self.selected_iis_index = self.list_iis_box.curselection()[0]
        self.SelectedIIS['text']=self.iisFiles[self.selected_iis_index].split("|")[0]
        self.SelectedIIS['background'] = "lightgreen"
        self.SelectedIIS.pack(anchor=tkinter.W)
    
    def checkHttpErrorFilesList(self):
        self.selected_httperror_index = self.list_httpError_box.curselection()[0]
        self.SelectedHttpError['text'] = self.httpErrorLogFiles[self.selected_httperror_index].split("|")[0]
        self.SelectedHttpError['background'] = "lightgreen"
        self.SelectedHttpError.pack(anchor=tkinter.W)

    def submit(self):
        ''' called when submit_btn is clicked'''
        inputIISLogFileName = self.SelectedIIS['text']
        inputHttpErrorLogFileName = self.SelectedHttpError['text']

        if(inputIISLogFileName=='None' and inputHttpErrorLogFileName =='None'):
            messagebox.showinfo('There is error','Plese choice at least ONE log.')
            return 0

        startTime,endTime = self.startDateBox.get(),self.endDateBox.get()

        flag = self.checkInputs()
        if(flag==True):
            #TODO:show windows message that filer start and do process at background
            getReports.getReports(inputIISLogFileName,inputHttpErrorLogFileName,startTime,endTime)
            messagebox.showinfo('Complete Filtering!','Let\'s check your output directory.')

    def checkInputs(self):
        errorMessage=""
        
        errorMessage +=checkInputDataModules.checkEmptyInput(self.startDateBox.get(),self.endDateBox.get(),self.SelectedIIS['text'],self.SelectedHttpError['text'])
        if(len(errorMessage)==0):
            errorMessage +=self.checkLogTerm()
            if(len(errorMessage)==0):
                return True
            else :
                messagebox.showinfo('There is error',errorMessage)
                return False
        else :
            messagebox.showinfo('There is error',errorMessage)
            return False

    def checkLogTerm(self):
        ''' caleed when '''
        errorMessage=""
        startTime,endTime = self.startDateBox.get()+":00",self.endDateBox.get()+":00"

        if(self.iisFiles[self.selected_iis_index]!='None'):
            iisTerm = self.iisFiles[self.selected_iis_index].split("|")[1].split(" ~ ")
            iislogStart,iislogEnd = iisTerm[0],iisTerm[1]
            errorMessage += checkInputDataModules.checkInputsBoforeSubmit(iislogStart,iislogEnd,startTime,endTime,'IISLog')

        if(self.httpErrorLogFiles[self.selected_httperror_index]!='None'):
            httpErrorTerm = self.httpErrorLogFiles[self.selected_httperror_index].split("|")[1].split(" ~ ")
            httpErrorlogStart,httpErrorlogEnd = httpErrorTerm[0],httpErrorTerm[1]
            errorMessage += checkInputDataModules.checkInputsBoforeSubmit(httpErrorlogStart,httpErrorlogEnd,startTime,endTime,'HttpErrorLog')
        return errorMessage

root = tkinter.Tk()
root.title('Filter Log App')
root.geometry('1200x900')

app = Application(root=root)
app.mainloop()