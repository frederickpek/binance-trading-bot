import time
import hmac
import hashlib
import datetime
import urllib.parse
from binance_sdk.consts import *
from binance_sdk.util.auth_type import AuthType
from binance_sdk.util.http_method import Method


def create_signature(secret_key: str, builder):
    query_string = builder.build_url()
    signature = hmac.new(secret_key.encode(), msg=query_string.encode(), digestmod=hashlib.sha256).hexdigest()
    builder.put_url("signature", signature)


def create_signature_with_query(secret_key: str, query: str):
    signature = hmac.new(secret_key.encode(), msg=query.encode(), digestmod=hashlib.sha256).hexdigest()
    return signature


def utc_now():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]

def create_header(method: Method, auth_type: AuthType, api_key=None):
    header = dict()
    if auth_type != AuthType.NONE:
        header[X_MBX_APIKEY] = api_key
    if method in [Method.POST, Method.PUT, Method.DELETE]:
        header[CONTENT_TYPE_NAME] = CONTENT_TYPE_VALUE
    return header

def create_signed_url(api_url: str, request_path: str, auth_type: AuthType, params: dict, secret_key=None):
    sign_param = {**params}
    if auth_type in [AuthType.TRADE, AuthType.USER_DATA]:
        sign_param[RECV_WINDOW_KEY] = RECV_WINDOW
        sign_param[TIMESTAMP_KEY] = int(time.time() * 1000)
        query_string: str = urllib.parse.urlencode(sign_param)
        sign_param["signature"] = create_signature_with_query(secret_key, query_string)
    request_path = f"{request_path}?{urllib.parse.urlencode(sign_param)}"
    return api_url + request_path

