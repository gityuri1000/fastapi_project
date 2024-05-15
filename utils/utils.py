import hashlib
import requests

from typing import Dict, Any, Union

from config.api import api_settings

class UtilsRepository:

    @classmethod
    async def get_hash_password(cls, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    @classmethod
    async def complain_passwords(cls, plain_password: str, password: str) -> bool:
        return plain_password == password
    
    @classmethod
    async def get_price_from_json(cls, json: Dict[str, Any]) -> Union[int, None]:
        try:
            price = json.get("closePrices")[0].get("price").get("units")
            return int(price)

        except AttributeError as e:
            print(f"Не удается получить цену инструмента из json: {e}")
            return None
        

    @classmethod
    async def make_price_request(cls, figi: str) -> Union[Dict[str, Any], None]:
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
    
