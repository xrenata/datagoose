from datetime import datetime
from gc import collect as gccollect
from hashlib import sha256
from os import mkdir
from os import path as opath
from re import findall
from threading import Thread
from time import sleep
from json import dump as slowjdump

from orjson import dumps as jdump
from orjson import loads as jload

from . import errors, functions


class Datagoose:
    def __init__(self, name: str, options: dict = {}):
        if not isinstance(name, str):
            raise TypeError("Name argument only can be string, not {0}.".format(type(name).__name__))

        if not isinstance(options, dict):
            raise TypeError("Options argument only can be dict, not {0}.".format(type(options).__name__))

        self.__path = options['PATH'] if 'PATH' in options and type(options['PATH']) == str else "datagoose_files"
        self.__autosave = options['AUTO_SAVE'] if 'AUTO_SAVE' in options and type(
            options['AUTO_SAVE']) == bool else False
        self.__leakgarbage = options['LEAK_GARBAGE'] if 'LEAK_GARBAGE' in options and type(
            options['LEAK_GARBAGE']) == bool else False
        self.__hashing = [i for i in options['HASHING'] if type(i) == str] if 'HASHING' in options and type(
            options['HASHING']) == list else []
        self.__safemode = options['SAFE_MODE'] if 'SAFE_MODE' in options and type(
            options['SAFE_MODE']) == bool else True

        self.__name = name
        self.__location = f"./{self.__path}/{self.__name}.json"

        self.__backup = False
        self.__backup_time = 60
        self.__backup_path = "datagoose_backups"

        path_prefix = "./"
        for path in self.__path.split("/"):
            if not opath.exists(f"{path_prefix}{path}"):
                mkdir(f"{path_prefix}{path}")
            path_prefix += f"{path}/"

        del path_prefix

        if not opath.isfile(self.__location):
            with open(self.__location, "w+", encoding="utf-8") as f:
                f.write(jdump({"database": []}).decode())

        with open(self.__location, "r", encoding="utf-8") as f:
            self.__memory = jload(f.read())["database"]

    def read(self) -> list:
        """Returns database memory."""

        return self.__memory

    @property
    def length(self) -> int:
        """Returns database total length."""

        return len(self.__memory)

    def save(self) -> bool:
        """Saves database to JSON file."""

        with open(self.__location, "w+", encoding="utf-8") as f:
            f.write(jdump({"database": self.__memory}).decode())

        gccollect()

        return True

    def save_with_indent(self, indent: int = None) -> bool:
        """Saves database to JSON file with indent (slow!)."""

        functions.raise_error(indent, "indent", (int, type(None)))

        with open(self.__location, "w+", encoding="utf-8") as f:
            slowjdump({"database": self.__memory}, f, indent=indent)

        gccollect()

        return True

    def insert_one(self, data: dict) -> dict:
        """Inserts one data (dict) to database."""

        functions.raise_error(data, "data", dict)
        functions.garbage_check(self.__leakgarbage, data)

        hashed = functions.hash_keys(self.__hashing, {
            "_id": functions.create_dict_id(data),
            **data
        })

        self.__memory.append(hashed)
        functions.auto_save(self.__autosave, self.__location, self.__memory)

        return hashed

    def insert_many(self, *args) -> bool:
        """Insert many data (dict args) to database."""

        def __insert_data(data):
            functions.garbage_check(self.__leakgarbage, data)
            return functions.hash_keys(self.__hashing, {
                "_id": functions.create_dict_id(data),
                **data
            })

        self.__memory.__iadd__(__insert_data(item) for item in args if isinstance(item, dict))
        functions.auto_save(self.__autosave, self.__location, self.__memory)

        return True

    def find(self, data: dict) -> dict:
        """Find data (dict) from database."""

        functions.raise_error(data, "data", dict)

        for objects in self.__memory:
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                    (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                       objects[item[0]])))]) == len(
                data):
                yield objects

    def find_and_sort(self, data: dict, key: str, reverse: bool = False) -> list:
        """Find and sort data (dict) from database."""

        functions.raise_error(data, "data", dict)
        functions.raise_error(key, "key", str)
        functions.raise_error(reverse, "reverse", bool)

        founds = (objects for objects in self.__memory
                  if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                   objects[item[0]])))]) == len(
            data))

        return sorted(founds, key=lambda v: v[key],
                      reverse=reverse)

    def find_one(self, data: dict) -> dict:
        """Find one (first) data (dict) from database."""

        functions.raise_error(data, "data", dict)

        for objects in self.__memory:
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                    (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                       objects[item[0]])))]) == len(
                data):
                return objects

        return {}

    def update(self, data: dict, new_data: dict) -> list:
        """Update data (dict) from database."""

        functions.raise_error(data, "data", dict)
        functions.raise_error(new_data, "new_data", dict)

        def __update_value(index, n_data):
            for values in n_data.items():
                self.__memory[index][values[0]] = values[1]

            return self.__memory[index]

        result = [__update_value(index, new_data) for index, objects in enumerate(self.__memory) if len(
            [item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                    (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                       objects[item[0]])))]) == len(
            data)]
        functions.auto_save(self.__autosave, self.__location, self.__memory)
        return result

    def update_one(self, data: dict, new_data: dict) -> dict:
        """Update one data (dict) from database."""

        functions.raise_error(data, "data", dict)

        functions.raise_error(new_data, "new_data", dict)

        for index, objects in enumerate(self.__memory):
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                    (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                       objects[item[0]])))]) == len(
                data):
                for values in new_data.items():
                    self.__memory[index][values[0]] = values[1]

                functions.auto_save(self.__autosave, self.__location, self.__memory)
                return self.__memory[index]

        return {}

    def delete(self, data: dict) -> list:
        """Delete data (dict) from database."""

        functions.raise_error(data, "data", dict)

        shift, deleted = 0, []
        for index, objects in enumerate(self.__memory[:]):
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                    (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                       objects[item[0]])))]) == len(
                data):

                del self.__memory[index - shift]
                deleted.append(objects)
                shift += 1

        functions.auto_save(self.__autosave, self.__location, self.__memory)
        return deleted

    def delete_one(self, data: dict) -> dict:
        """Delete one data (dict) from database."""

        functions.raise_error(data, "data", dict)

        for index, objects in enumerate(self.__memory[:]):
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                    (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                       objects[item[0]])))]) == len(
                data):
                del self.__memory[index]

                functions.auto_save(self.__autosave, self.__location, self.__memory)
                return objects

        return {}

    def count(self, data: dict) -> int:
        """Count data (dict) from database."""

        functions.raise_error(data, "data", dict)

        return len([objects for objects in self.__memory if len([item for item in data.items() if
                                                                 item[0] in objects and (
                                                                         item[1] == objects[item[0]] or ((type(
                                                                     item[1]), type(objects[item[0]])) == (str,
                                                                                                           str,) and findall(
                                                                     item[1], objects[item[0]])))]) == len(data)])

    def exists(self, data: dict) -> bool:
        """Checks a data (dict) is in database."""

        functions.raise_error(data, "data", dict)

        return bool([objects for objects in self.__memory if len([item for item in data.items() if
                                                                  item[0] in objects and (
                                                                          item[1] == objects[item[0]] or ((type(
                                                                      item[1]), type(objects[item[0]])) == (str,
                                                                                                            str,) and findall(
                                                                      item[1], objects[item[0]])))]) == len(data)])

    has = exists

    def dump(self, location: str, encoding: str = "utf-8", indent=None) -> bool:
        """Dumps all the data to a file."""

        functions.raise_error(location, "location", str)
        functions.raise_error(encoding, "encoding", str)
        functions.raise_error(indent, "indent", (int, type(None)))

        with open(location, "w+", encoding=encoding) as f:
            f.write(jdump({"database": self.__memory}).decode())

        gccollect()

        return True

    export = dump

    def load(self, location: str, encoding: str = "utf-8", overwrite: bool = True) -> bool:
        """Loads a json file to the database."""

        functions.raise_error(location, "location", str)
        functions.raise_error(encoding, "encoding", str)
        functions.raise_error(overwrite, "overwrite", bool)

        with open(location, "r", encoding=encoding) as f:
            loaded = jload(f.read())

        if not "database" in loaded:
            raise KeyError("Can't find 'database' array in the json.")
        elif not isinstance(loaded["database"], list):
            raise TypeError("'database' Value must be a list.")

        dicts = ({"_id": functions.create_dict_id(i), **i} for i in loaded["database"] if isinstance(i, dict))

        if overwrite:
            self.__memory = list(dicts)
        else:
            self.__memory.extend(dicts)

        functions.auto_save(self.__autosave, self.__location, self.__memory)
        return True

    @property
    def info(self) -> dict:
        """Returns database info."""

        return {
            "hash": sha256(str(self.__memory).encode()).hexdigest(),
            "length": len(self.__memory),
            "location": self.__location,
            "name": self.__name
        }

    def clear(self) -> bool:
        """Clears the entire database."""

        self.__memory = []

        functions.auto_save(self.__autosave, self.__location, self.__memory)
        return True

    def collect_garbage(self) -> list:
        """Returns all the garbage data in database."""

        for item in self.__memory:
            if list(item.keys()) == ['_id']:
                yield item

    def clear_garbage(self) -> bool:
        """Remove all the garbage data in database."""

        for item in self.__memory.copy():
            if list(item.keys()) == ['_id']:
                self.__memory.remove(item)

        functions.auto_save(self.__autosave, self.__location, self.__memory)
        return True

    def copy(self, data: dict, repeat: int = 1) -> bool:
        """Copy the found data(s) to the database."""

        functions.raise_error(data, "data", dict)
        functions.raise_error(repeat, "repeat", int)

        if self.__safemode:
            if repeat < 1:
                raise errors.ValueTooSmall(
                    "The minimum repeat value can be 1. if you don't want limitation, "
                    "make 'SAFE_MODE' option False. (not recommended.)"
                )
            if repeat > 100_000:
                raise errors.ValueTooBig(
                    "The maximum repeat value can be 100,000. if you don't want limitation, "
                    "make 'SAFE_MODE' option False. (not recommended.)"
                )

        def __give_id_to_data(obj):
            return {
                **obj,
                "_id": functions.create_dict_id(obj)
            }

        while repeat > 0:
            self.__memory.extend(
                __give_id_to_data(objects) for objects in self.__memory.copy() if len([item for item in data.items() if
                                                                                       item[0] in objects and (
                                                                                               item[1] == objects[
                                                                                           item[0]] or ((type(
                                                                                           item[1]), type(
                                                                                           objects[item[0]])) == (
                                                                                                            str,
                                                                                                            str,) and findall(
                                                                                           item[1], objects[
                                                                                               item[0]])))]) == len(
                    data)
            )

            repeat -= 1

        functions.auto_save(self.__autosave, self.__location, self.__memory)
        return True

    def copy_one(self, data: dict) -> dict:
        """Copy the found data(s) to the database."""

        functions.raise_error(data, "data", dict)

        for objects in self.__memory.copy():
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or (
                    (type(item[1]), type(objects[item[0]])) == (str, str,) and findall(item[1],
                                                                                       objects[item[0]])))]) == len(
                data):
                data = {
                    **objects,
                    "_id": functions.create_dict_id(objects)
                }

                self.__memory.append(data)
                functions.auto_save(self.__autosave, self.__location, self.__memory)
                return data

    def sort_for_key(self, key: str, reverse: bool = False) -> list:
        """Sort database for key. (not saves, just returns sorted version of database.)"""

        functions.raise_error(key, "key", str)
        functions.raise_error(reverse, "reverse", bool)

        return sorted((i for i in self.__memory if type(i) == dict and key in i.keys()), key=lambda v: v[key],
                      reverse=reverse)

    def start_backup(self, options: dict = {}) -> None:
        """Opens backup for database. if backup is already open, it will raise error."""

        functions.raise_error(options, "options", dict)
        if self.__safemode:
            if self.__backup:
                raise errors.BackupAlreadyStarted(
                    "Backup is already started. if you wan't to ignore this error,"
                    " make 'SAFE_MODE' option False. (not recommended.)"
                )

            if 'TIME' in options and type(options['TIME']) in (float, int,):
                if options['TIME'] < 30:
                    raise errors.ValueTooSmall(
                        "Backup time value is too small. The minimum time can be 30 second. "
                        "if you wan't to ignore this error, make 'SAFE_MODE' option False. (not recommended.)"
                    )
                elif options['TIME'] > 31_557_600:
                    raise errors.ValueTooBig(
                        "Backup time value is too big. The maximum time can be 1 year. "
                        "if you wan't to ignore this error, make 'SAFE_MODE' option False. (not recommended.)"
                    )
            else:
                options['TIME'] = 60

        self.__backup = True
        self.__backup_time = options['TIME']
        self.__backup_path = options['PATH'] if 'PATH' in options and type(
            options['PATH']) == str else "datagoose_backups"

        def __wrapper():
            while self.__backup:
                last_path = "./"
                for path in self.__backup_path.split("/"):
                    if not opath.exists(f"{last_path}{path}"):
                        mkdir(f"{last_path}{path}")
                    last_path += f"{path}/"

                with open(f"./{self.__backup_path}/backup_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json", "w+",
                          encoding="utf-8") as f:
                    f.write(jdump({"database": self.__memory}).decode())

                gccollect()
                sleep(self.__backup_time)

        Thread(target=__wrapper, daemon=True).start()

    def stop_backup(self) -> bool:
        """Stops backup for database. if backup is closed, it will not effect."""

        self.__backup = False
        return True

    @property
    def is_backup_open(self) -> bool:
        """Returns auto-backup status."""

        return self.__backup
