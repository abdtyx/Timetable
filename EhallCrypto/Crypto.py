from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad

def crypates(password):
    key='0725@pwdorgopenp'
    aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
    pad_pkcs7 = pad(password.encode('utf-8'), AES.block_size, style='pkcs7')
    return base64.b64encode(aes.encrypt(pad_pkcs7))