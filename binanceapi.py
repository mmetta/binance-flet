import requests
from settings import read_pars


def data_objs():
    data = consulta()
    pars = read_pars()
    objs = []
    for name in pars:
        for par in data:
            if par["symbol"] == str(name):
                amplitude = float(par["highPrice"]) / float(par["lowPrice"])
                perc = float(par["openPrice"]) / float(par["bidPrice"])
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
