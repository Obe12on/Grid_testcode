
import json

class loadJson:
    def load(json_path : str) -> list:
        with open(json_path, 'r', encoding = 'utf-8') as file:

            data = json.loads(file.read())
            return(data)

if __name__ == '__main__':
    loadJson()