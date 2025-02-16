import aes
import base64
import hashlib

from fastapi import FastAPI, Request
from starlette.responses import PlainTextResponse
from typing import List

import melina_client

token = 'dK2cRNE322kDvTR9NA'
encoding_aes_key = 'vZrUvHQ1sf2SGxpuT3KlDsXpBRk2e4f3AcWWTlXIPJI'

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/fs")
async def fs(request: Request) -> PlainTextResponse:
    request_body_bytes = await request.body()
    request_body = request_body_bytes.decode('utf-8')
    print(request_body)
    melina_client.handle(request_body)
    return PlainTextResponse("hello world.")


@app.get("/work-wx/check")
def check(msg_signature: str, timestamp: str, nonce: str, echostr: str) -> PlainTextResponse:
    print(echostr)

    # 拼接并排序
    sorted_list: List[str] = sorted([token, timestamp, nonce, echostr])
    sorted_string = ''.join(sorted_list)

    # 计算 SHA1 签名
    actual_signature = hashlib.sha1(sorted_string.encode('utf-8')).hexdigest()

    if msg_signature != actual_signature:
        raise ValueError("Signature verification failed")

    # 解密
    aes_key = base64.b64decode(encoding_aes_key + "=")
    decrypted = aes.aes_decrypt(aes_key, echostr)

    # 提取消息内容
    length_bytes = decrypted[0:4]
    print('length_bytes: ', length_bytes)
    length_big = int.from_bytes(length_bytes, byteorder='big')
    print('length_big: ', length_big)
    content_big = decrypted[4:4 + length_big].decode('utf-8')
    print(content_big)
    print(decrypted.decode('utf-8'))
    return PlainTextResponse(content_big)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8110)
