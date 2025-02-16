from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64


# AES 加密函数
def aes_encrypt(key: bytes, data: bytes) -> str:
    """
    使用 AES 加密数据。
    :param key: 加密密钥（长度必须是 16、24 或 32 字节，对应 AES-128、AES-192 或 AES-256）。
    :param data: 要加密的数据（字节类型）。
    :return: 加密后的数据（Base64 编码的字符串）。
    """
    # 生成随机的 16 字节 IV
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 使用 PKCS7 填充数据
    padded_data = pad(data, AES.block_size)
    encrypted = cipher.encrypt(padded_data)

    # 返回 IV + 加密数据（便于解密时使用相同的 IV）
    encrypted_data = iv + encrypted
    return base64.b64encode(encrypted_data).decode()


# AES 解密函数
def aes_decrypt(key: bytes, encrypted_data: str) -> bytes:
    """
    使用 AES 解密数据。
    :param key: 解密密钥（长度必须是 16、24 或 32 字节）。
    :param encrypted_data: 加密后的数据（Base64 编码的字符串）。
    :return: 解密后的原始数据（字节类型）。
    """
    # 将 Base64 编码的字符串解码为字节
    encrypted_data_bytes = base64.b64decode(encrypted_data)

    # 提取 IV（前 16 字节）
    iv = encrypted_data_bytes[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密数据并去除填充
    decrypted = cipher.decrypt(encrypted_data_bytes[16:])
    return unpad(decrypted, AES.block_size)
