import pandas as pd

class nullCheck:
    def checkNullFile(data : pd.DataFrame , input_name : str) -> None:
        nullValueList = []
        if data.isnull().any().any():
            nullValueList.append(input_name)
        if nullValueList:
            print('<INFO> Null values found on {}'.format(input_name))
            print('<INFO> Necessary to implement data imputation')
            quit()
        else:
            print('<INFO> No null values found on {}'.format(input_name))

if __name__ == '__main__':
    nullCheck()