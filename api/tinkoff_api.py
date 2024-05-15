import requests

from typing import Union, Dict, Any

from config.api import api_settings

from dto.result import InstrumentID

class TinkoffAPI:

    @classmethod
    async def get_price_from_json(cls, json: Dict[str, Any]) -> Union[int, None]:
        try:
            price = json.get("closePrices")[0].get("price").get("units")
            return int(price)

        except AttributeError as e:
            print(f"Не удается получить цену инструмента из json: {e}")
            return None
        

    @classmethod
    async def make_price_request(cls, figi: InstrumentID) -> Union[Dict[str, Any], None]:
        url = api_settings.BASE_URL + "/tinkoff.public.invest.api.contract.v1.MarketDataService/GetClosePrices"

        json = {
            "instruments": [
                {
                "instrumentId": f"{figi}"
                }
            ]
        }

        headers = {
            "Authorization": api_settings.TOKEN
        }

        post = requests.post(
            url=url,
            json=json,
            headers=headers
        )

        if isinstance(post.json(), dict):
            return post.json()