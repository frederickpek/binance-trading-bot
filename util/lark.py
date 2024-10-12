import requests
from secret import LARK_KEY


def send_lark_msg(msg: str, lark_key: str=LARK_KEY):
    try:
        resp = requests.post(
            url=f"https://open.larksuite.com/open-apis/bot/v2/hook/{lark_key}",
            json={"msg_type": "text", "content": {"text": msg}}
        )
        return resp.status_code
    except:
        pass
