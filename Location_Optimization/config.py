import base64
from Crypto.Cipher import AES
user_name = 'ALG'
server_ip = '10.42.10.202'
#password = 'nPrhkBK*7'
password = 'FwMSKXCz0BpTOf09hCe0ww=='
db_name = 'alog-wms'

query = "select SPD.ProductCode,SPD.Qty,SPD.PositionCode,O.PlanOutTime from V_t_OutOrder O "
query += "left join V_t_Stock_Pick SP on O.OutOrderNo = SP.OutOrderNo "
query += "left join V_t_Stock_Pick_Detail SPD on SP.PickNo = SPD.PickNo "
query += "left join V_t_Storage_Position SPO on SPD.PositionCode = SPO.PositionCode "
query += "where SPO.Abc_Type = 'A' and SP.StorageCode = 'ALOG-0003-03'"

queryrealdata = "select SPD.ProductCode,SPD.PositionCode,sum(SPD.Qty) AS '总数量' from V_t_OutOrder O " #根据计划出库时间
queryrealdata += "left join V_t_Stock_Pick SP on O.OutOrderNo = SP.OutOrderNo "
queryrealdata += "left join V_t_Stock_Pick_Detail SPD on SPD.DetailBoxingNo = SP.BoxingNo "
queryrealdata += "left join V_t_Storage_Position SPO on SPO.PositionCode = SPD.PositionCode "
queryrealdata += "where SPO.Abc_Type = 'A' and SPO.StorageCode = 'ALOG-0003-03' AND O.PlanOutTime >= {} "
queryrealdata += "AND O.PlanOutTime <= {} and O.CancelbyWLB = 0 group by SPD.ProductCode,SPD.PositionCode "

queryorderdata = "select SPD.ProductCode,SPD.PositionCode,sum(SPD.Qty) AS '总数量' from V_t_OutOrder O " #根据订单流入时间
queryorderdata += "left join V_t_Stock_Pick SP on O.OutOrderNo = SP.OutOrderNo "
queryorderdata += "left join V_t_Stock_Pick_Detail SPD on SPD.DetailBoxingNo = SP.BoxingNo "
queryorderdata += "left join V_t_Storage_Position SPO on SPO.PositionCode = SPD.PositionCode "
queryorderdata += "where SPO.Abc_Type = 'A' and SPO.StorageCode = 'ALOG-0003-03' AND O.OrderTime >= {} "
queryorderdata += "AND O.OrderTime <= {} AND O.PlanOutTime >= {}  AND O.PlanOutTime <= {} and O.CancelbyWLB = 0 group by SPD.ProductCode,SPD.PositionCode "

queryoptimiza = "select ARM.ProductCode,SQ.PositionCode,ARM.PlanQty from V_t_Algorithm_RMSSalesPlan ARM "
queryoptimiza += "left join V_t_Storage_Qty SQ on ARM.ProductCode = SQ.ProductCode "
queryoptimiza += "left join V_t_Storage_Position SPO on SPO.PositionCode = SQ.PositionCode "
queryoptimiza += "where SPO.Abc_Type = 'A' and SPO.StorageCode = 'ALOG-0003-03' AND SQ.Qty > 0 "
queryoptimiza += "AND ARM.PlanTime >= {} AND ARM.PlanTime <= {}"




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