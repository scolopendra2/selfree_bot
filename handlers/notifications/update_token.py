import json
import os

import requests
import asyncio
from loader import data


def get_x_alfacrm_token():
    url = "https://selfree.s20.online/v2api/auth/login"
    response = requests.post(url, data=json.dumps(data))
    return response.json()['token']


async def update():
    os.environ['X-ALFACRM-TOKEN'] = get_x_alfacrm_token()
    print(os.environ['X-ALFACRM-TOKEN'])
    await asyncio.sleep(1)
