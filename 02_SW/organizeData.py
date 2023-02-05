import pandas as pd

class organizeData:
    def ByID(dataDict : dict , isStationary : pd.DataFrame) -> dict:
        newDictData = {}
        for key, value in dataDict.items():
            data = value
            dataID = data.groupby('商品ID')
            for ID, group in dataID:
                if ID not in newDictData:
                    newDictData[ID] = {}
                dataNew = group.drop(['商品ID'], axis = 1)
                dataNew['日付'] = pd.to_datetime(dataNew['日付'], format = '%Y-%m')
                dataNew.index = dataNew['日付']
                del dataNew['日付']
                newDictData[ID][key] = dataNew
        columns = list(isStationary)
        for index in columns:
            newDictData[index]['isStationary'] = isStationary[index]

        return newDictData

if __name__ == '__main__':
    organizeData()