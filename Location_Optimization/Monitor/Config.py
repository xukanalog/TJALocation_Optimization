import base64
from Crypto.Cipher import AES

user_name = 'ALG'
server_ip = '10.42.10.202'
#password = 'nPrhkBK*7'
password = 'FwMSKXCz0BpTOf09hCe0ww=='
db_name = 'alog-wms'

query = "select P.BarCode,PositionCode from V_t_Storage_Qty SQ "
query += "left join V_t_Product P on SQ.ProductCode = P.ProductCode "
query += "where Qty > 0 and StorageCode = 'Alog-0003-03' "
query += "and left(PositionCode,2) <> '41' and left(PositionCode,3) <> '42R' and PositionCode = {} group by P.BarCode,PositionCode  "

# str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes

#解密方法
def decrypt_oralce(password):
    # 秘钥
    key = '123456'
    # 密文
    text = password
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','')
    return decrypted_text

password = decrypt_oralce(password)