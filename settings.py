import json
import os


app_path = os.path.abspath(os.getcwd())
path = os.path.join(app_path, './')


def read_themes():
    try:
        json_path = os.path.normpath(os.path.join(path, 'themes.json'))
        with open(json_path, 'r', encoding='utf8') as f:
            j = json.load(f)
            return j
    except Exception as e:
        print(e)
        return []


def write_themes(temas):
    json_path = os.path.normpath(os.path.join(path, 'themes.json'))
    try:
        with open(json_path, 'w', encoding='utf8') as f:
            json.dump(temas, f)
        return 'Temas salvos com sucesso!!'
    except Exception as e:
        return e
