import requests


def consulta(name):
    link = 'https://api2.binance.com/api/v3/ticker/24hr'
    try:
        req = requests.get(link)
        res = req.json()
        for par in res:
            if par["symbol"] == str(name):
                print(par["symbol"])
                amplitude = float(par["highPrice"]) / float(par["lowPrice"])
                perc = float(par["openPrice"]) / float(par["bidPrice"])
                obj = {
                    "open": f"{float(par["openPrice"]):.3f}",
                    "hi": f"{float(par["highPrice"]):.3f}",
                    "low": f"{float(par["lowPrice"]):.3f}",
                    "amplitude": f"{amplitude:.2f}%",
                    "bid": f"{float(par["bidPrice"]):.3f}",
                    "perc": f"{perc:.2f}%"
                }
        return obj
    except Exception as e:
        print(e)
        return {}
