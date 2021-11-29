import pandas
from pandas import read_csv, Series, DataFrame
import os


# Author: Hyun Ju Jang

class Model:

    def __init__(self):
        print("Model class constructor called")

    def getDataSet(self, filename):
        dataSet = DataFrame()

        try:
            dataSet = read_csv(filename, header=None)
        except:
            print("Data Read Error")

        return dataSet

    def saveToCSV(self, fileName, dataSet):
        dataSet.to_csv(fileName, mode='a', header=None)

    def clearCSV(self, fileName):
        if os.path.exists(fileName):
            os.remove(fileName)
            print("CSV data file is deleted.")
        else:
            print("The file does not exist")
