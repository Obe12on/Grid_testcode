import pandas as pd

class loadCSV:
        def load(csv_path : str) -> 'pd.core.frame.DataFrame':
                df = pd.read_csv(csv_path)
                return df

if __name__ == '__main__':
    loadCSV()