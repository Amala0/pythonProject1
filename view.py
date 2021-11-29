import os

from controller import Controller
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import LEFT, X, CENTER, W
from tkinter.filedialog import askopenfilename
from collections import Counter


# Author: Hyun Ju Jang

class View:
    """ View class in MVC """

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1100x600")
        self.window.title("Credit Card Fraud Detection Software")
        self.strFileName = tk.StringVar()

    def buildTable(self):
        self.tableFrame = Frame(self.window, width=1000, height=500, bd=15)

        cols = ('Trans', 'Transaction_Date', "Posting_Date", "Description", "Amount")

        self.tree = ttk.Treeview(self.tableFrame, columns=cols, show='headings')
        self.tree.heading('Trans', text='Transaction')
        self.tree.heading('Transaction_Date', text='Transaction Date')
        self.tree.heading('Posting_Date', text='Posting Date')
        self.tree.heading('Description', text='Description')
        self.tree.heading('Amount', text='Amount')

        self.tableFrame.pack()
        self.tree.pack()

    def displayResult(self, dataSet, result1, result2):
        countDetected = 0

        for i in self.tree.get_children():
            self.tree.delete(i)

        i = 0

        for obj in dataSet:
            if result1[i] == -1 or result2[i] == -1:
                self.tree.insert('', 'end',
                                 values=(dataSet[i][0], dataSet[i][1], dataSet[i][2], dataSet[i][3], dataSet[i][4]))
                countDetected = countDetected + 1

            i = i + 1

        if countDetected > 0:
            self.result1.config(bg="red")
        else:
            self.result1.config(bg="#7CFC00")

        self.tree.pack()
        self.tableFrame.update()

    def displayDimensions(self, dataSet):
        dimWin = tk.Toplevel()
        dimWin.wm_title("Dimensions")
        dimWin.geometry("350x140")

        shapeInfo = dataSet.shape

        l = tk.Label(dimWin, text="Number of Rows and Columns\n\n" + str(shapeInfo))
        l.grid(row=0, column=0, padx=100, pady=20)

        b = tk.Button(dimWin, text="Close", command=dimWin.destroy)
        b.grid(row=1, column=0, padx=100, pady=10)

    def selAlgo(self):
        global alg_option
        selection = "You selected the option " + str(alg_option.get())
        print(selection)

    def getPDFFileNameFromEntry(self):
        fName = self.fileNameField.get()

        return fName;

    def getPDFFileName(self):
        fName = askopenfilename()
        self.strFileName.set(fName)

        return fName;

    def displayPeek(self, dataSet):
        peekWim = tk.Toplevel()
        peekWim.wm_title("Peek First 10 Rows")
        peekWim.geometry("480x300")

        first10Rows = dataSet.head(10)

        l = tk.Label(peekWim, text=str(first10Rows), justify=LEFT)
        l.grid(row=0, column=0, padx=20, pady=20)

        b = tk.Button(peekWim, text="Close", command=peekWim.destroy)
        b.grid(row=1, column=0, padx=20, pady=10)

    def displayHistMessage(self, mode):
        histWim = tk.Toplevel()
        histWim.wm_title("Histogram Message")
        histWim.geometry("340x100")

        if mode == 1:
            l1 = tk.Label(histWim, text='\nThe CSV file is invalid. The file does not exist.\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        elif mode == 2:
            l1 = tk.Label(histWim, text='\nno data, CSV file is empty\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        elif mode == 3:
            histWim.geometry("345x100")
            l1 = tk.Label(histWim, text='\nThe file has missing column(s).\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)

        b = tk.Button(histWim, text="Close", command=histWim.destroy)
        b.grid(row=4, column=0, padx=20, pady=10)

    def displayErrorParsing(self, option):
        errMsgWin = tk.Toplevel()
        errMsgWin.wm_title("Parsing Message")

        if option == 1:
            errMsgWin.geometry("330x100")
            l1 = tk.Label(errMsgWin, text='\nError parsing the file. Is it a PDF file?\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        elif option == 2:
            errMsgWin.geometry("280x100")
            l1 = tk.Label(errMsgWin, text='\nNo transaction is recorded.\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        elif option == 3:
            errMsgWin.geometry("400x100")
            l1 = tk.Label(errMsgWin, text='\nSelect one of BMO, Scotia, or CIBC credit card statements.\n',
                          justify=LEFT)
            l1.grid(row=0, column=0, padx=50)

        b = tk.Button(errMsgWin, text="Close", command=errMsgWin.destroy)
        b.grid(row=4, column=0, padx=20, pady=10)

    def displayErrorPredict(self, option):
        errMsgWin = tk.Toplevel()
        errMsgWin.wm_title("Predict Error Message")

        errMsgWin.geometry("230x100")
        if option == 1:
            l1 = tk.Label(errMsgWin, text='\nSave the input file.\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        elif option == 2:
            l1 = tk.Label(errMsgWin, text='\nData set is empty.\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)

        b = tk.Button(errMsgWin, text="Close", command=errMsgWin.destroy)
        b.grid(row=4, column=0, padx=20, pady=10)

    def displaySummary(self, dataSet):
        sumWim = tk.Toplevel()
        sumWim.wm_title("Summary of Data")

        # Summary of Amount column
        if os.path.isfile('dataset_customer.csv') == False:
            sumWim.geometry("340x100")
            l1 = tk.Label(sumWim, text='\nThe file does not exist.\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        elif len(dataSet) == 0:
            sumWim.geometry("340x100")
            l1 = tk.Label(sumWim, text='\nno data, CSV file is empty\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        elif len(dataSet.columns) < 5:
            sumWim.geometry("345x100")
            l1 = tk.Label(sumWim, text='\nThe file has missing column(s).\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=50)
        else:
            sumWim.geometry("340x380")
            l1 = tk.Label(sumWim, text='\nAmount (Column 4)\n', justify=LEFT)
            l1.grid(row=0, column=0, padx=5)

            summary = dataSet[4].describe()

            l2 = tk.Label(sumWim, text=str(summary), justify=LEFT)
            l2.grid(row=1, column=0, padx=30)

        b = tk.Button(sumWim, text="Close", command=sumWim.destroy)
        b.grid(row=4, column=0, padx=20, pady=10)

    def buildView(self, controller):
        alg_option = tk.IntVar(self.window)

        datasetLabelRow = tk.Frame(self.window)
        datasetFileRow = tk.Frame(self.window)

        uploadLabelRow = tk.Frame(self.window)
        selectFileRow = tk.Frame(self.window)
        accountInfoTileRow = tk.Frame(self.window)
        clientNameRow = tk.Frame(self.window)
        bankNameRow = tk.Frame(self.window)
        resultLabelRow = tk.Frame(self.window)

        result1Row = tk.Frame(self.window)

        # Row
        datasetTitle = tk.Label(datasetLabelRow, text="Data Set", anchor='w')
        datasetTitle.pack(side=LEFT)

        # Row
        datasetFileLabel = tk.Label(datasetFileRow, text="File Name:", anchor='w', width=9)
        datasetFileLabel.pack(side=LEFT)

        dsFileNameField = tk.Entry(datasetFileRow, width=30)
        dsFileNameField.pack(side=LEFT, padx=5)
        dsFileNameField.insert(0, 'dataset_customer.csv')
        dsFileNameField.configure({"background": "#E8E8E8"})

        dimensionsButton = tk.Button(datasetFileRow, command=controller.dimensionsClick, text="Dimensions")
        dimensionsButton.pack(side=LEFT, padx=3)

        peekButton = tk.Button(datasetFileRow, command=controller.peekClick, text="Peek Data")
        peekButton.pack(side=LEFT, padx=3)

        sumButton = tk.Button(datasetFileRow, command=controller.summaryOfData, text="Summary")
        sumButton.pack(side=LEFT, padx=3)

        histButton = tk.Button(datasetFileRow, command=controller.histogram, text="Histogram")
        histButton.pack(side=LEFT, padx=3)

        # Row
        uploadFileTitle = tk.Label(uploadLabelRow, text="Input File", anchor='w')
        uploadFileTitle.pack(side=LEFT)

        # Row
        selectFileLabel = tk.Label(selectFileRow, text="Select File:", anchor='w', width=9)
        selectFileLabel.pack(side=LEFT)

        self.fileNameField = tk.Entry(selectFileRow, width=30, textvariable=self.strFileName)
        self.fileNameField.bind('<Return>', controller.readPDFKeyIn)
        self.fileNameField.pack(side=LEFT, padx=5)

        browseButton = tk.Button(selectFileRow, text="Browse", command=controller.readPDF)
        browseButton.pack(side=LEFT, padx=5)

        saveButton = tk.Button(selectFileRow, text="Save", command=controller.saveToCSV)
        saveButton.pack(side=LEFT, padx=5)

        clearButton = tk.Button(selectFileRow, text="Delete", command=controller.clearCSV)
        clearButton.pack(side=LEFT, padx=5)

        # Row
        acctInfoTitle = tk.Label(accountInfoTileRow, text="Account Info", anchor='w')
        acctInfoTitle.pack(side=LEFT)

        # Row
        self.clientNameLabel = tk.Label(clientNameRow, text="Client Name:", anchor='w', width=9)
        self.clientNameLabel.pack(side=LEFT)

        self.clientNameField = tk.Entry(clientNameRow, width=30)
        self.clientNameField.pack(side=LEFT, padx=5)

        # Row
        bankNameLabel = tk.Label(bankNameRow, text="Bank Name:", anchor='w', width=9)
        bankNameLabel.pack(side=LEFT)

        self.bankNameField = tk.Entry(bankNameRow, width=30)
        self.bankNameField.pack(side=LEFT, padx=5)

        # Row
        resultTitleLabel = tk.Label(resultLabelRow, text="Prediction", anchor='w')
        resultTitleLabel.pack(side=LEFT)

        # Row
        processButton = tk.Button(result1Row, text="Process Input", width=20, command=controller.predict)
        processButton.pack(side=LEFT, padx=3)

        self.result1 = tk.Label(result1Row, text="Result (Pass or Fail)", width=20, borderwidth=2, relief="ridge",
                                bg='#7CFC00')
        self.result1.pack(side=LEFT, padx=5)

        # Support Vector Machines (SVM)

        datasetLabelRow.pack(fill=X, padx=10, pady=5)
        datasetFileRow.pack(fill=X, padx=25, pady=5)

        uploadLabelRow.pack(fill=X, padx=10, pady=5)
        selectFileRow.pack(fill=X, padx=25, pady=5)

        accountInfoTileRow.pack(fill=X, padx=10, pady=10)
        clientNameRow.pack(fill=X, padx=25, pady=5)
        bankNameRow.pack(fill=X, padx=25, pady=5)

        resultLabelRow.pack(fill=X, padx=10, pady=10)
        result1Row.pack(fill=X, padx=25, pady=5)

        self.buildTable()

        self.window.mainloop()

    def resetInputFields(self):
        self.fileNameField.delete(0, END)
        self.clientNameField.delete(0, END)
        self.bankNameField.delete(0, END)

    def setBankName(self, bkName):
        self.bankNameField.delete(0, END)
        self.bankNameField.insert(0, bkName)
