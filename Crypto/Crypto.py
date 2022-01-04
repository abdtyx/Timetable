import requests
import json
def crypates(password):
    url = "http://tool.chacuo.net/cryptaes"
    data = {
        "data" : password,
        "type" : "aes",
        "arg" : "m=ecb_pad=pkcs7_block=128_p=0725@pwdorgopenp_o=0_s=utf-8_t=0"
    }
    headers = {
        "Cookie": "__yjs_duid=1_8951386ced567837690521334496dde71635310863455; __gads=ID=c2b1567921e87b81-221f52c7e4cc007c:T=1635310867:RT=1635310867:S=ALNI_Mae_OdF9ItTZIKNzHG-fmqLcPXz-g; bdshare_firstime=1635310864973; yjs_js_security_passport=b530c1e922208d6279a792dcb07cdb9f3803f314_1641272681_js; Hm_lvt_ef483ae9c0f4f800aefdf407e35a21b3=1641272682; Hm_lpvt_ef483ae9c0f4f800aefdf407e35a21b3=1641272682",
        "Host": "tool.chacuo.net",
        "Origin": "http://tool.chacuo.net",
        "Referer": "http://tool.chacuo.net/cryptaes",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62",
    }
    r = requests.post(url=url, data=data, headers=headers, allow_redirects=False)
    return json.loads(r.text)['data'][0]