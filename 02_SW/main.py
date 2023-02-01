import JSONloader
import CSVloader
import os
import FullerTest
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class Main:
    def __init__(self) -> None:
        self.isStationary_data = pd.DataFrame()

    def readJson(self) -> None:
        cwd = os.getcwd()
        json_path = cwd + "\\" + "config.json"
        self.config_data = JSONloader.loadJson.load(json_path)

    def readCSV(self) -> None:
        self.sales_df = CSVloader.loadCSV.load(self.config_data['Sales_data'])
        self.discount_df = CSVloader.loadCSV.load(self.config_data['Discount_data'])
        self.sales_forecast_df = CSVloader.loadCSV.load(self.config_data['Sales_forecast'])
        self.discount_forecast_df = CSVloader.loadCSV.load(self.config_data['Discount_forecast'])

    def checkNullValue(self) -> None:
        
        print('\r\n=============================================================\r\n')
        print('<INFO> Checking null values \r\n')
        data = self.sales_df
        fileName = 'Sales_data'
        self.checkNullFile(data,fileName)
        data = self.discount_df
        fileName = 'Discount_data'
        self.checkNullFile(data,fileName)
        data = self.sales_forecast_df
        fileName = 'Sales_forecast'
        self.checkNullFile(data,fileName)
        data = self.discount_forecast_df
        fileName = 'Discount_forecast'
        self.checkNullFile(data,fileName)
        
    def checkNullFile(self, data : pd.DataFrame , input_name : str) -> None:
        nullValueList = []
        if data.isnull().any().any():
            nullValueList.append(input_name)
        if nullValueList:
            print('<INFO> Null values found on {}'.format(input_name))
            print('<INFO> Necessary to implement data imputation')
            quit()
        else:
            print('<INFO> No null values found on {}'.format(input_name))

    def checkMissingEntry(self) -> None:
        data = self.sales_df.groupby('商品ID')
        self.checkMissingPerID('Sales_data', data)
        data = self.discount_df.groupby('商品ID')
        self.checkMissingPerID('Discount_data', data)
        data = self.sales_forecast_df.groupby('商品ID')
        self.checkMissingPerID('Sales_forecast', data)
        data = self.discount_forecast_df.groupby('商品ID')
        self.checkMissingPerID('Discount_forecast', data)

    def checkMissingPerID(self,input_name : str, input_df : pd.DataFrame) -> None:
        missingContainer = []
        date_start = [self.config_data['{}_start'.format(input_name)]['Year'],self.config_data['{}_start'.format(input_name)]['Month']]
        date_end = [self.config_data['{}_end'.format(input_name)]['Year'],self.config_data['{}_end'.format(input_name)]['Month']]
        date_range = pd.date_range('{}-{}'.format(date_start[0],date_start[1]),'{}-{}'.format(date_end[0],date_end[1]), freq= 'MS')
        print('\r\n=============================================================\r\n')
        print('<INFO> Checking missing entry for {}\r\n'.format(input_name))
        for ID, group in input_df:
            data = group.drop(['商品ID'], axis = 1)
            data.index = pd.to_datetime(data['日付'])
            del data['日付']
            missingDates = date_range[~date_range.isin(data.index)]
            if not missingDates.empty :
                print('<INFO> Data {} ->Missing entry on ID: {} for dates {}'.format(input_name, ID, missingDates))
                missingContainer.append(missingDates)
        if missingContainer:
            userInput = input('<USER CHECK> If missing entry is not relevant for model, press y to continue :')
            if userInput == 'y':
                pass
            else:
                quit()
        else:
            print('<INFO> No missing entry')

    def stationaryCheck(self) -> None:
        productID = self.sales_df.groupby('商品ID')
        for ID, group in productID:
            data = group.drop(['商品ID'], axis = 1)
            data['日付'] = pd.to_datetime(data['日付'], format = '%Y-%m')
            data.index = data['日付']
            del data['日付']
            isStationary = FullerTest.Dickey_Fuller.isStationary(data)
            self.isStationary_data[ID] = [ isStationary ]
        
           

    def main(self) -> None:
        self.readJson()
        self.readCSV()
        self.checkNullValue()
        self.checkMissingEntry()
        self.stationaryCheck()

        
        
    

if __name__ == '__main__':
    C = Main().main()