import JSONloader
import CSVloader
import os
import FullerTest
import pandas as pd
import nullCheck as nc
import missingCheck as mc
import organizeData as od
import trainArima as ta
from threading import Thread

class Main:
    def __init__(self) -> None:
        self.isStationary_data = pd.DataFrame()
        self.resultDict = {}

    def readJson(self) -> None:
        cwd = os.getcwd()
        json_path = cwd + "\\" + "config.json"
        self.config_data = JSONloader.loadJson.load(json_path)

    def readCSV(self) -> None:
        self.dataDict = {}
        self.dataDict['Sales_data'] = CSVloader.loadCSV.load(self.config_data['Sales_data'])
        self.dataDict['Discount_data'] = CSVloader.loadCSV.load(self.config_data['Discount_data'])
        self.dataDict['Sales_forecast'] = CSVloader.loadCSV.load(self.config_data['Sales_forecast'])
        self.dataDict['Discount_forecast'] = CSVloader.loadCSV.load(self.config_data['Discount_forecast'])

    def checkNullValue(self) -> None:
        print('\r\n=============================================================\r\n')
        print('<INFO> Checking null values \r\n')
        for key, value in self.dataDict.items():
            nc.nullCheck.checkNullFile(value,key)

    def checkMissingEntry(self) -> None:
        for key, value in self.dataDict.items():
            date_start = [self.config_data['{}_start'.format(key)]['Year'],self.config_data['{}_start'.format(key)]['Month']]
            date_end = [self.config_data['{}_end'.format(key)]['Year'],self.config_data['{}_end'.format(key)]['Month']]
            data = value.groupby('商品ID')
            mc.missingCheck.checkMissingPerID(key, data, date_start, date_end)

    def stationaryCheck(self) -> None:
        data = self.dataDict['Sales_data']
        productID = data.groupby('商品ID')
        for ID, group in productID:
            data = group.drop(['商品ID'], axis = 1)
            data['日付'] = pd.to_datetime(data['日付'], format = '%Y-%m')
            data.index = data['日付']
            del data['日付']
            isStationary = FullerTest.Dickey_Fuller.isStationary(data)
            self.isStationary_data[ID] = [ isStationary ]
    
    def organizeDataByID(self) -> None:
        self.dataByID = {}
        self.dataByID = od.organizeData.ByID(self.dataDict, self.isStationary_data)
        
    def createModelThread(self) -> None:
        self.threadDict = {}
        totalTask = len(self.dataByID)
        self.numberOfThread = self.config_data['Number_of_processing_thread']
        for threadsTask in range(self.numberOfThread):
            startVal = (threadsTask ) * (totalTask//self.numberOfThread) + 1
            endVal = (threadsTask + 1 ) * (totalTask//self.numberOfThread)
            if endVal > totalTask :
                endVal = totalTask
            self.threadDict[threadsTask] = Thread(target = self.trainModelThread, args = (startVal, endVal))
            self.threadDict[threadsTask].start()
            

    def trainModelThread(self, startVal : int , endVal : int) -> None:
        for ID in range(startVal, endVal + 1):
            self.trainModel(ID)
            print('<INFO> Result for product ID {} completed'.format(ID))

    def trainModel(self, ID : int) -> None:
        self.resultDict[ID] = ta.callArima.train(self.dataByID[ID])
        
    def outputResultCSV(self) -> None:
        for threadsTask in range(self.numberOfThread):
            self.threadDict[threadsTask].join()
        result = self.resultDict[1].astype('int')
        for ID in range(2 , len(self.resultDict) + 1):
            result = pd.concat([result, self.resultDict[ID].astype('int')], axis= 1)
        result.to_csv('my_submission.csv', encoding = 'utf-8_sig', date_format = '%Y-%m', header = False)

    
    def main(self) -> None:
        self.readJson()
        self.readCSV()
        self.checkNullValue()
        self.checkMissingEntry()
        self.stationaryCheck()
        self.organizeDataByID()
        self.createModelThread()
        self.outputResultCSV()

        

        
        
    

if __name__ == '__main__':
    C = Main().main()