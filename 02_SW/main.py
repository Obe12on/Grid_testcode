import JSONloader
import CSVloader
import os
import FullerTest
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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
        self.stationaryCheck()
        print(self.isStationary_data)

        
        
    

if __name__ == '__main__':
    C = Main().main()