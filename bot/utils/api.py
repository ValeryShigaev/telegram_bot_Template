import os
from base64 import decode, encode

import aiohttp
import json

from redis import asyncio as aioredis
from typing import Union, List, Dict
from fastapi.security import OAuth2PasswordRequestForm


storage = aioredis.from_url("redis://redis:6379")


async def login() -> Union[str, None]:
    """
    This function allows to get local api token and writes it to storage

    :rtype: Union[str, None]
    """

    url = 'http://api:5000/token/'
    form = OAuth2PasswordRequestForm(
        grant_type='password',
        username=os.getenv('ADMIN_EMAIL'),
        password=os.getenv('ADMIN_PASSWORD'),
    )
    form_data = aiohttp.FormData()
    for key, val in form.__dict__.items():
        form_data.add_field(key, val)
    try:
        async with aiohttp.ClientSession() as session:
            result = await session.post(url, data=form_data, ssl=False)
            result_text = await result.json()
            token = 'Bearer ' + result_text['access_token']
            await storage.set('api_token', token)
            return token
    except Exception as e: # can log here later
        return None

async def users_list() -> List[Dict]:
    """
    This function allows to get users list fom <users> test endpoint

    :rtype: List[str, Dict]
    """

    token = await storage.get('api_token')
    token = token.decode('utf-8') if token else await login() # can decorate here later
    url = 'http://api:5000/users/'
    async with aiohttp.ClientSession() as session:
        result = await session.get(url,
                                   headers={'Authorization': token},
                                   ssl=False)
        result_text = await result.text()
        return json.loads(result_text)['data']
