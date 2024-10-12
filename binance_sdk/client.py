import requests
import logging
import urllib.parse
import time
from typing import Dict, Any

from binance_sdk.util.auth_util import create_header, create_signed_url
from binance_sdk.util.http_method import Method
from binance_sdk.util.auth_type import AuthType
from binance_sdk.consts import *


class Client(object):

    def __init__(self, api_key: str, secret_key: str, api_url: str):
        self._api_key: str = api_key
        self._secret_key: str = secret_key
        self._api_url: str = api_url
        self.session = requests.Session()

    def _request(self, method: Method, request_path: str, params: Dict[str, str], auth_type: AuthType):
        logging.info("binance http url: %s" % self._api_url + f"{request_path}?{self.build_url(params)}")
        header = create_header(method, auth_type, api_key=self._api_key)
        url = create_signed_url(self._api_url, request_path, auth_type, params, secret_key=self._secret_key)

        # send request
        response = None
        if method == Method.GET:
            response = requests.get(url, headers=header, timeout=10)
        elif method == Method.POST:
            response = self.session.post(url, headers=header, timeout=10)
        elif method == Method.DELETE:
            response = requests.delete(url, headers=header, timeout=10)

        # exception handle
        if not str(response.status_code).startswith('2'):
            logging.info("http response: %s" % response.content)
            raise ValueError(f"{response.content}")
        # logging.info("http response: %s" % response.content)
        return response.json()

    def _request_without_params(self, method: Method, request_path: str, auth_type: AuthType):
        return self._request(method, request_path, {}, auth_type)

    def _request_with_params(self, method, request_path, params, auth_type: AuthType):
        return self._request(method, request_path, params, auth_type)

    def request(self, method, request_path, params={}, auth_type=AuthType.NONE):
        return self._request(method, request_path, params, auth_type)

    @staticmethod
    def build_url(param_map):
        if len(param_map) == 0:
            return ""
        encoded_param = urllib.parse.urlencode(param_map)
        return encoded_param

    @staticmethod
    def _get_timestamp():
        return int(time.time() * 1000)

