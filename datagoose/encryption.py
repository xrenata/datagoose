from orjson import dumps as jdump
from orjson import loads as jload
from base64 import b64encode, b64decode
from hashlib import sha256

from . import errors


def encrypt(data: dict) -> str:
    string_data = jdump(data)
    encoded = b64encode(string_data)
    keycode_generator = (i for i in encoded)

    encrypted = "=>".join(
        sorted(str((i + v) * 2) + f"x{i}" for i, v in enumerate(keycode_generator)))
    return sha256(string_data).hexdigest() + f"+{encrypted}"


def decrypt(data: str) -> dict:
    hash_split = data.split("+")
    splitted = hash_split[1].split("=>")

    base64 = ""

    for data in sorted(splitted, key=lambda i: int(i.split("x")[1])):
        result = data.split("x")
        key_decode = int(result[0]) // 2
        key_decode -= int(result[1])

        base64 += chr(key_decode)

    decoded = b64decode(base64).decode()
    decode_dict = jload(b64decode(base64).decode())

    if sha256(decoded.encode()).hexdigest() == hash_split[0]:
        return decode_dict
    else:
        raise errors.DecodeHashError(
            "Decrypted hash and encrypted hash is not matching.")
