import requests
from settings import read_pars
import json
import os


app_path = os.path.abspath(os.getcwd())
path = os.path.join(app_path, './')


def write_dolar_now(usdt):
    json_path = os.path.normpath(os.path.join(path, 'dolar_now.txt'))
    try:
        with open(json_path, 'w', encoding='utf8') as f:
            f.write(usdt)
        return 'Dolar salvo com sucesso!!'
    except Exception as e:
        return e
    

def read_dolar_now():
    try:
        dolar_path = os.path.normpath(os.path.join(path, 'dolar_now.txt'))
        with open(dolar_path, "r") as arquivo:
            usdt = arquivo.read()
            return float(usdt)
    except Exception as e:
        print(e)
        return 0


def write_obj_list(objs):
    json_path = os.path.normpath(os.path.join(path, 'obj_list.json'))
    try:
        with open(json_path, 'w', encoding='utf8') as f:
            json.dump(objs, f)
        return 'Objetos salvos com sucesso!!'
    except Exception as e:
        return e
    

def read_obj_list():
    try:
        json_path = os.path.normpath(os.path.join(path, 'obj_list.json'))
        with open(json_path, 'r', encoding='utf8') as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return []


def read_wallet():
    try:
        json_path = os.path.normpath(os.path.join(path, 'wallet.json'))
        with open(json_path, 'r', encoding='utf8') as f:
            return json.load(f)
    except Exception as e:
        print(e)
        return []


# def data_objs():
#     pars = read_pars()
#     objs = []
#     for name in pars:
#         par = consulta_par(name)
#         amplitude = float(par["highPrice"]) / float(par["lowPrice"])
#         perc = float(par["priceChangePercent"])
#         obj = {
#             "symbol": par["symbol"],
#             "open": f"{float(par["openPrice"]):.3f}",
#             "hi": f"{float(par["highPrice"]):.3f}",
#             "low": f"{float(par["lowPrice"]):.3f}",
#             "amplitude": f"{amplitude:.2f}%",
#             "bid": f"{float(par["lastPrice"]):.3f}",
#             "perc": f"{perc:.2f}"
#         }
#         objs.append(obj)
#         USDT = consulta_dolar()
#         write_dolar_now(USDT["price"])
#     write_obj_list(objs)
#     return objs


def data_objs():
    data = consulta()
    pars = read_pars()
    objs = []
    for name in pars:
        for par in data:
            if par["symbol"] == str(name):
                amplitude = float(par["highPrice"]) / float(par["lowPrice"])
                perc = float(par["priceChangePercent"])
                obj = {
                    "symbol": par["symbol"],
                    "open": f"{float(par["openPrice"]):.3f}",
                    "hi": f"{float(par["highPrice"]):.3f}",
                    "low": f"{float(par["lowPrice"]):.3f}",
                    "amplitude": f"{amplitude:.2f}%",
                    "bid": f"{float(par["bidPrice"]):.3f}",
                    "perc": f"{perc:.2f}"
                }
                objs.append(obj)
            if par["symbol"] == "USDTBRL":
                write_dolar_now(par["bidPrice"])
    write_obj_list(objs)
    return objs


def consulta():
    link = 'https://api2.binance.com/api/v3/ticker/24hr'
    try:
        req = requests.get(link)
        res = req.json()
        return res
    except Exception as e:
        print(e)
        return {}


def consulta_par(par):
    link = f"https://api2.binance.com/api/v3/ticker?symbol={par}"
    try:
        req = requests.get(link)
        res = req.json()
        return res
    except Exception as e:
        print(e)
        return {}
    
    
def consulta_dolar():
    link = "https://api2.binance.com/api/v3/ticker/price?symbol=USDTBRL"
    try:
        req = requests.get(link)
        res = req.json()
        return res
    except Exception as e:
        print(e)
        return {}
