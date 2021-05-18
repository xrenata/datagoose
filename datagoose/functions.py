from gc import collect as gccollect
from hashlib import sha256
from random import sample, randint
from re import findall
from string import digits, ascii_lowercase
from time import time

from orjson import dumps as jdump

from . import errors


def find_item_algorithm(data, obj, regex):
    return len([item for item in data.items() if
                item[0] in obj and (item[1] == obj[item[0]] or (regex and
                                                                (type(item[1]), type(obj[item[0]])) == (
                                                                    str, str,) and findall(item[1],
                                                                                           obj[item[
                                                                                               0]])))]) == len(
        data)


def auto_save(option: bool, location: str, memory: list, events: dict):
    if option:
        events["before_save"]()
        with open(location, "w+", encoding="utf-8") as f:
            f.write(jdump({"database": memory}).decode())

        events["after_save"]()
        gccollect()


def garbage_check(data: dict):
    if not bool(data):
        raise errors.GarbageDataError(
            "You can't insert garbage data to database. Try use older version of datagoose.")


def hash_keys(keys: list, data: dict):
    for key in data.keys():
        if key in keys:
            data[key] = sha256(str(data[key]).encode()).hexdigest()

    return data


def raise_error(value, argument_name: str, check):
    if isinstance(check, tuple):
        if not type(value) in check:
            raise TypeError(
                f"Argument '{argument_name}' type must be {' / '.join([i.__name__ if i != None else 'None' for i in check])}, not {type(value).__name__}.")
    else:
        if not isinstance(value, check):
            raise TypeError(
                f"Argument '{argument_name}' type must be {check.__name__ if check != None else 'None'}, not {type(value).__name__}.")


def create_dict_id(data: dict) -> str:
    if not isinstance(data, dict):
        raise TypeError(
            "Data argument only can be dict, not {0}.".format(
                type(data).__name__))

    return sha256(
        f'{time()}_{"".join(sample(digits, 10))}_{sha256(jdump(data)).hexdigest()}_{"".join(sample(ascii_lowercase, randint(10, 25)))}'.encode()
    ).hexdigest()
