import numpy
import pandas as pd
from pandas import read_csv, Series, DataFrame
from matplotlib import pyplot
from sklearn.ensemble import IsolationForest

import pdfplumber
from collections import namedtuple
from tkinter import *

import re

import os
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import LocalOutlierFactor

Trans = namedtuple('Trans', 'Transaction_Date Posting_Date Description Amount')


# Author: Hyun Ju Jang

class Controller:
    """ Controller class in MVC """

    def __init__(self, model, view):
        """
            Initialized with model and view
        :param model:
        :param view:
        """
        self.model = model
        self.view = view

        self.data = DataFrame()

        print("Controller Constructor is called")

    def dimensionsClick(self):
        self.loadData()

        self.view.displayDimensions(self.dataSet)

    def peekClick(self):
        self.loadData()

        self.view.displayPeek(self.dataSet)

    def summaryOfData(self):
        self.loadData()

        self.view.displaySummary(self.dataSet)

    def histogram(self):
        self.loadData()

        if os.path.isfile('dataset_customer.csv') == False:
            self.view.displayHistMessage(1)
        elif len(self.dataSet) == 0:
            self.view.displayHistMessage(2)
        elif len(self.dataSet.columns) < 5:
            self.view.displayHistMessage(3)
        else:
            self.dataSet.hist()
            pyplot.show()

    def startWindow(self):
        self.view.buildView(self)

    def loadData(self):
        self.dataSet = self.model.getDataSet('dataset_customer.csv')

    def getOutlierFactor(self):
        defaultValue = 0.02

        avg = 0

        array = self.dataSet.values
        amounts = array[:, 4]

        # if the amount is more than 98 quantile of the amounts, then add to the outlier list

        count = 0

        quantile = numpy.quantile(amounts, 0.98)

        for amount in amounts:
            if amount > quantile:
                count = count + 1

        ol_factor = count / amounts.size

        if ol_factor > 0.5:
            ol_factor = 0.5

        if ol_factor == 0:
            ol_factor = defaultValue

        print("Outlier Factor: " + str(ol_factor))

        return ol_factor

    def predict(self):
        self.loadData()

        if self.dataSet.empty:

            strBankName = self.view.bankNameField.get()

            if strBankName:
                # Click on save button
                self.view.displayErrorPredict(1)
            else:
                # Data Set is empty
                self.view.displayErrorPredict(2)

            return

        random_state = numpy.random.RandomState(42)
        array = self.dataSet.values

        dateArray = array[:, 1]
        descArray = array[:, 3]
        amtArray = array[:, 4]

        labelencoder_X = LabelEncoder()
        encodedDateArray = labelencoder_X.fit_transform(dateArray)
        encodedDescArray = labelencoder_X.fit_transform(descArray)

        samples = []

        i = 0

        for x in amtArray:
            row = []
            row.append(encodedDateArray[i])
            row.append(encodedDescArray[i])
            row.append(x)
            samples.append(row)
            i = i + 1

        random_state = numpy.random.RandomState(42)
        result1 = IsolationForest(contamination=float(self.getOutlierFactor()), random_state=random_state).fit_predict(
            samples)

        clf = LocalOutlierFactor(n_neighbors=18, contamination=self.getOutlierFactor())
        result2 = clf.fit_predict(samples)

        self.view.displayResult(array, result1, result2)

    def parseCIBC(self, text):
        print("CIBC Bank Statement detected")

        # For testing, we do not reveal customer's real name
        customerName = "Joe Smith"

        self.view.clientNameField.delete(0, END)
        self.view.clientNameField.insert(0, customerName)

        purchase_items = list()

        purchase_line = re.compile(r'^([a-zA-Z]{3}\ \d{1,2}) ([a-zA-Z]{3}\ \d{1,2}) ([\w\W]*) ([0-9,]+\.\d{2})$')
        for line in text.split("\n"):
            ln = purchase_line.match(line)
            if ln:
                trans_date = ln.group(1)
                posting_date = ln.group(2)
                description = ln.group(3)
                amount = ln.group(4)
                amount = amount.replace(",", "")

                purchase_items.append(Trans(trans_date, posting_date, description, amount))

        if len(purchase_items) == 0:
            self.view.displayErrorParsing(2)
        else:
            self.view.setBankName("CIBC Bank");
            self.data = DataFrame(purchase_items)

    def parseScotia(self, text):
        print("Scotia Bank Statement detected")

        # For testing, we do not reveal customer's real name
        customerName = "Joe Smith"

        self.view.clientNameField.delete(0, END)
        self.view.clientNameField.insert(0, customerName)

        purchase_items = list()

        purchase_line = re.compile(r'^\d{3} ([a-zA-Z]{3} \d{1,2}) ([a-zA-Z]{3} \d{1,2}) ([\w\W]*) ([0-9,]+\.\d{2})')
        for line in text.split("\n"):
            ln = purchase_line.match(line)
            if ln:
                trans_date = ln.group(1)
                posting_date = ln.group(2)
                description = ln.group(3)
                amount = ln.group(4)
                amount = amount.replace(",", "")
                purchase_items.append(Trans(trans_date, posting_date, description, amount))

        if len(purchase_items) == 0:
            self.view.displayErrorParsing(2)
        else:
            self.view.setBankName("Scotia Bank");
            self.data = DataFrame(purchase_items)

    def parseBMO(self, text):
        print("Bank of Montreal Statement detected")

        for line in text.split("\n"):
            if line.startswith("Customer Name"):
                idx = line.find("Purchases and other charges")

                if idx != -1:
                    customerName = line[14:idx]
                else:
                    customerName = line[14:]

                # For testing, we do not reveal customer's real name
                customerName = "Joe Smith"

                self.view.clientNameField.delete(0, END)
                self.view.clientNameField.insert(0, customerName)

                break

        purchase_items = list()

        purchase_line = re.compile(r'^([a-zA-Z]{3}\. \d{1,2}) ([a-zA-Z]{3}\. \d{1,2}) ([\w\W]*) ([0-9,]+\.\d{2})$')
        for line in text.split("\n"):
            ln = purchase_line.match(line)
            if ln:
                trans_date = ln.group(1)
                posting_date = ln.group(2)
                description = ln.group(3)
                amount = ln.group(4)
                amount = amount.replace(",", "")

                purchase_items.append(Trans(trans_date, posting_date, description, amount))

        print("\n")

        #        deposit_line = re.compile(r'^([a-zA-Z]{3}\. \d{1,2}) ([a-zA-Z]{3}\. \d{1,2}) ([\w\W]*) ([0-9,]+\.\d{2}) CR$')
        #        for line in text.split("\n"):
        #            ln = deposit_line.match(line)
        #            if ln:
        #                print(line)

        if len(purchase_items) == 0:
            self.view.displayErrorParsing(2)
        else:
            self.view.setBankName("Bank of Montreal");
            self.data = DataFrame(purchase_items)

    def saveToCSV(self):
        if self.data.empty == False:
            self.model.saveToCSV('dataset_customer.csv', self.data)
            print("Data is appended to dataset_customer.csv")

    def clearCSV(self):
        self.model.clearCSV('dataset_customer.csv', )
        self.view.resetInputFields()
        self.dataSet = DataFrame()
        self.view.displayResult(self.dataSet, list(), list())

    def readPDFKeyIn(self, event):
        strFileName = self.view.getPDFFileNameFromEntry()

        self.readPDFDetails(strFileName)

    def readPDF(self):
        strFileName = self.view.getPDFFileName()

        self.readPDFDetails(strFileName)

    def readPDFDetails(self, strFileName):
        whole_text = ""

        errorOccurred = False

        try:
            with pdfplumber.open(strFileName) as pdf:
                for page in pdf.pages:
                    text = page.extract_text(x_tolerance=1)
                    if isinstance(text, str):
                        whole_text = whole_text + text

            print("PDF File: " + strFileName)

            #        print(whole_text)
            # detect bank
            # 1. BMO
            # 2. Scotia Bank

            bmoDetected = False
            scotiaDetected = False
            cibcDetected = False

            for line in whole_text.split("\n"):
                linelower = line.lower()
                if 'bank of montreal' in linelower:
                    bmoDetected = True
                elif 'scotiabank' in linelower:
                    scotiaDetected = True
                elif 'cibc' in linelower:
                    cibcDetected = True

            if bmoDetected:
                self.parseBMO(whole_text)
            elif scotiaDetected:
                self.parseScotia(whole_text)
            elif cibcDetected:
                self.parseCIBC(whole_text)
            else:
                self.view.displayErrorParsing(3)

        except:
            errorOccurred = True

        if errorOccurred:
            self.view.displayErrorParsing(1)
