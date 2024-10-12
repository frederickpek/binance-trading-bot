import aiohttp
import logging
from binance_sdk.consts import *
from binance_sdk.util.http_method import Method
from binance_sdk.util.auth_type import AuthType
from binance_sdk.util.auth_util import create_header, create_signed_url


class AsyncClient(object):

    def __init__(self, api_key: str, secret_key: str, api_url: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_url = api_url

    async def request(self, method: Method, request_path: str, params: dict={}, auth_type: AuthType=AuthType.NONE, should_log=True, log_response=False):
        if should_log:
            logging.info(f"{method.name} {self.api_url}{request_path} -- {params=}")
        header = create_header(method, auth_type, api_key=self.api_key)
        url = create_signed_url(self.api_url, request_path, auth_type, params, secret_key=self.secret_key)
        return await self.request_session(method, url, header, log_response)

    async def request_session(self, method: Method, url: str, header: dict, log_response: bool):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
            async with getattr(session, method.value.lower())(url, headers=header) as response:
                return await self.manage_response(response, log_response)

    async def manage_response(self, response, log_response):
        try:
            resp_json = await response.json()
            if log_response:
                logging.info(f"http response: {resp_json}")
            return resp_json
        except ValueError:
            resp_text = await response.text()
            err_msg = f"invalid response: {resp_text}"
            logging.exception(err_msg)
            raise ValueError(err_msg)
