import pandas as pd

class missingCheck:
    def checkMissingPerID(input_name : str, input_df : pd.DataFrame, date_start : list, date_end : list) -> None:
        missingContainer = []
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

if __name__ == '__main__':
    missingCheck()