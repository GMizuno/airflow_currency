import requests
from datetime import datetime
import logging

def available_symbols(headers):
    url = "https://fixer-fixer-currency-v1.p.rapidapi.com/symbols"
    symbols = requests.get(url=url, headers=headers).json().get('symbols').keys()
    for symbol in symbols:
        yield symbol


def remove_wrong_symbols(symbols, all_symbols):
    s1 = set(symbols)
    s2 = set(all_symbols)
    s_result = s1 & s2

    if len(s1 - s_result):
        print(f'Remove {s1 - s_result}, does not exists')

    return s_result


def request(base: str, symbols: list, headers: dict) -> dict:
    logger = logging.getLogger(__name__)

    url = "https://fixer-fixer-currency-v1.p.rapidapi.com/latest"

    availables = list(available_symbols(headers))
    symbols = ','.join(remove_wrong_symbols(symbols, availables))
    if base not in availables:
        raise ValueError(f'base {base} does not exists, replace by {availables}')

    logger.info(f"Fetching curreny of {symbols} use {base} as base")
    querystring = {"base": base, "symbols": symbols}
    return requests.get(url=url, headers=headers, params=querystring).json()


def clean_resquest(dict) -> dict:
    if dict.get('success') == True and dict.get('success') is not None:
        return {"timestamp": datetime.utcfromtimestamp(dict.get('timestamp')).strftime('%Y-%m-%d %H:%M:%S'),
                "base": dict.get('base'),
                "rates": dict.get('rates')
                }
    else:
        raise ValueError(f'Wrong dict {dict}')


def execute(base: str, symbols: list, headers: dict) -> dict:
    result = request(base, symbols, headers)
    return clean_resquest(result)