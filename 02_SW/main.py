import JSONloader
import CSVloader
import os

class Main:
    def readJson(self) -> None:
        cwd = os.getcwd()
        json_path = cwd + "\\" + "config.json"
        self.config_data = JSONloader.loadJson.load(json_path)

    def readCSV(self) -> None:
        self.sales_df = CSVloader.loadCSV.load(self.config_data['Sales_data'])
        self.discount_df = CSVloader.loadCSV.load(self.config_data['Discount_data'])
        self.sales_forecast_df = CSVloader.loadCSV.load(self.config_data['Sales_forecast'])
        self.discount_forecast_df = CSVloader.loadCSV.load(self.config_data['Discount_forecast'])
    def main(self) -> None:
        self.readJson()
        self.readCSV()
        print(type(self.sales_df))
        
    

if __name__ == '__main__':
    C = Main().main()