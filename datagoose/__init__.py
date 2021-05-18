# Hash: bc86c078738529555989c12dfc7afb35fa9908c3fd4bf29bbf9041312ee64fc6

from datetime import datetime
from gc import collect as gccollect
from hashlib import sha256
from json import dump as slowjdump
from os import mkdir
from os import path as opath
from threading import Thread
from time import sleep
from typing import Union, Callable

from orjson import dumps as jdump
from orjson import loads as jload

from . import errors, functions


class Datagoose:
    def __init__(self, name: str, options: dict = {}) -> None:
        if not isinstance(name, str):
            raise TypeError(
                "Name argument only can be string, not {0}.".format(
                    type(name).__name__))

        if not isinstance(options, dict):
            raise TypeError(
                "Options argument only can be dict, not {0}.".format(
                    type(options).__name__))

        self.__path = options['PATH'] if 'PATH' in options and isinstance(
            options['PATH'], str) else "datagoose_files"
        self.__autosave = options['AUTO_SAVE'] if 'AUTO_SAVE' in options and isinstance(
            options['AUTO_SAVE'], bool) else False
        self.__hashing = [
            i for i in options['HASHING'] if isinstance(
                i, str)] if 'HASHING' in options and isinstance(
            options['HASHING'], list) else []
        self.__safemode = options['SAFE_MODE'] if 'SAFE_MODE' in options and isinstance(
            options['SAFE_MODE'], bool) else True
        self.__useregex = options['USE_REGEX'] if 'USE_REGEX' in options and isinstance(
            options['USE_REGEX'], bool) else False

        self.__name = name
        self.__location = f"./{self.__path}/{self.__name}.json"

        self.__backup = False
        self.__backup_time = 60
        self.__backup_path = "datagoose_backups"

        self.__events = {
            "before_insert": lambda value: None,
            "should_insert": lambda value: True,
            "after_insert": lambda value: None,

            "before_update": lambda now, changes: None,
            "should_update": lambda now, changes: True,
            "after_update": lambda now, old: None,

            "before_delete": lambda value: None,
            "should_delete": lambda value: True,
            "after_delete": lambda value: None,

            "before_copy": lambda value: None,
            "should_copy": lambda value: True,
            "after_copy": lambda value: None,

            "before_save": lambda: None,
            "after_save": lambda: None,

            "before_export": lambda: None,
            "after_export": lambda: None,

            "before_import": lambda: None,
            "after_import": lambda: None,

            "backup_start": lambda: None,
            "backup": lambda: None,
            "backup_finish": lambda: None,

            "before_garbage_clear": lambda: None,
            "after_garbage_clear": lambda: None
        }

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

    def on(self, key: str, event: Callable) -> dict:
        """Creates event for database."""

        functions.raise_error(key, "key", str)
        functions.raise_error(event, "event", type(lambda: True))

        if key not in self.__events.keys():
            raise KeyError(
                "Event not found. Please check the documentation for all events!")

        self.__events[key] = event

        return {key: event}

    def read(self) -> list:
        """Returns database memory."""

        return self.__memory

    @property
    def length(self) -> int:
        """Returns database total length."""

        return len(self.__memory)

    def save(self) -> bool:
        """Saves database to JSON file."""

        self.__events["before_save"]()
        with open(self.__location, "w+", encoding="utf-8") as f:
            f.write(jdump({"database": self.__memory}).decode())

        self.__events["after_save"]()
        gccollect()

        return True

    def save_with_indent(self, indent: int = None) -> bool:
        """Saves database to JSON file with indent (slow!)."""

        functions.raise_error(indent, "indent", (int, type(None)))

        self.__events["before_save"]()
        with open(self.__location, "w+", encoding="utf-8") as f:
            slowjdump({"database": self.__memory}, f, indent=indent)

        self.__events["after_save"]()
        gccollect()

        return True

    def insert_one(self, data: dict) -> Union[dict, None]:
        """Inserts one data (dict) to database."""

        functions.raise_error(data, "data", dict)
        functions.garbage_check(data)

        self.__events["before_insert"](data)

        if self.__events["should_insert"](data):
            hashed = functions.hash_keys(self.__hashing, {
                "_id": functions.create_dict_id(data),
                **data
            })

            self.__memory.append(hashed)
            self.__events["after_insert"](data)

            functions.auto_save(
                self.__autosave,
                self.__location,
                self.__memory,
                self.__events)

            return hashed

    def insert_many(self, *args) -> bool:
        """Insert many data (dict args) to database."""

        def __insert_data(data):
            functions.garbage_check(data)
            self.__events["before_insert"](data)

            if self.__events["should_insert"](data):
                item = functions.hash_keys(self.__hashing, {
                    "_id": functions.create_dict_id(data),
                    **data
                })
                self.__events["after_insert"](item)
                return item
            else:
                return {}

        self.__memory.__iadd__(__insert_data(item)
                               for item in args if isinstance(item, dict))
        self.clear_garbage()
        functions.auto_save(
            self.__autosave,
            self.__location,
            self.__memory,
            self.__events)

        return True

    def find(self, data: dict) -> dict:
        """Find data (dict) from database."""

        functions.raise_error(data, "data", dict)

        for objects in self.__memory:
            if functions.find_item_algorithm(data, objects, self.__useregex):
                yield objects

    def find_and_sort(
            self,
            data: dict,
            key: str,
            reverse: bool = False) -> list:
        """Find and sort data (dict) from database."""

        functions.raise_error(data, "data", dict)
        functions.raise_error(key, "key", str)
        functions.raise_error(reverse, "reverse", bool)

        founds = (
            objects for objects in self.__memory if functions.find_item_algorithm(
                data, objects, self.__useregex))

        return sorted(founds, key=lambda v: v[key],
                      reverse=reverse)

    def find_one(self, data: dict) -> dict:
        """Find one (first) data (dict) from database."""

        functions.raise_error(data, "data", dict)

        for objects in self.__memory:
            if functions.find_item_algorithm(data, objects, self.__useregex):
                return objects

        return {}

    def update(self, data: dict, new_data: dict) -> list:
        """Update data (dict) from database."""

        functions.raise_error(data, "data", dict)
        functions.raise_error(new_data, "new_data", dict)

        def __update_value(index, n_data):
            now = self.__memory[index]
            self.__events["before_update"](now, n_data)
            if self.__events["should_update"](now, n_data):
                for values in n_data.items():
                    self.__memory[index][values[0]] = values[1]

                self.__events["after_update"](self.__memory[index], now)

            return self.__memory[index]

        result = [
            __update_value(
                index, new_data) for index, objects in enumerate(
                self.__memory) if functions.find_item_algorithm(
                data, objects, self.__useregex)]
        functions.auto_save(
            self.__autosave,
            self.__location,
            self.__memory,
            self.__events)
        self.clear_garbage()
        return result

    def update_one(self, data: dict, new_data: dict) -> dict:
        """Update one data (dict) from database."""

        functions.raise_error(data, "data", dict)
        functions.raise_error(new_data, "new_data", dict)

        for index, objects in enumerate(self.__memory):
            if functions.find_item_algorithm(data, objects, self.__useregex):
                self.__events["before_update"](objects, new_data)
                if self.__events["should_update"](objects, new_data):
                    for values in new_data.items():
                        self.__memory[index][values[0]] = values[1]

                    self.__events["after_update"](
                        self.__memory[index], objects)

                functions.auto_save(
                    self.__autosave,
                    self.__location,
                    self.__memory,
                    self.__events)
                return self.__memory[index]

        return {}

    def delete(self, data: dict) -> list:
        """Delete data (dict) from database."""

        functions.raise_error(data, "data", dict)

        shift, deleted = 0, []
        for index, objects in enumerate(self.__memory[:]):
            if functions.find_item_algorithm(data, objects, self.__useregex):
                self.__events["before_delete"](self.__memory[index - shift])
                if self.__events["should_delete"](
                        self.__memory[index - shift]):
                    save = self.__memory[index - shift]
                    del self.__memory[index - shift]

                    self.__events["after_delete"](save)
                    deleted.append(objects)
                    shift += 1

        functions.auto_save(
            self.__autosave,
            self.__location,
            self.__memory,
            self.__events)
        return deleted

    def delete_one(self, data: dict) -> dict:
        """Delete one data (dict) from database."""

        functions.raise_error(data, "data", dict)

        for index, objects in enumerate(self.__memory[:]):
            if functions.find_item_algorithm(data, objects, self.__useregex):
                self.__events["before_delete"](self.__memory[index])
                if self.__events["should_delete"](self.__memory[index]):
                    save = self.__memory[index]
                    del self.__memory[index]

                    self.__events["after_delete"](save)

                functions.auto_save(
                    self.__autosave,
                    self.__location,
                    self.__memory,
                    self.__events)
                return objects

        return {}

    def count(self, data: dict) -> int:
        """Count data (dict) from database."""

        functions.raise_error(data, "data", dict)

        return len([objects for objects in self.__memory if functions.find_item_algorithm(
            data, objects, self.__useregex)])

    def exists(self, data: dict) -> bool:
        """Checks a data (dict) is in database."""

        functions.raise_error(data, "data", dict)

        return bool([objects for objects in self.__memory if functions.find_item_algorithm(
            data, objects, self.__useregex)])

    has = exists

    def dump(self, location: str, encoding: str = "utf-8") -> bool:
        """Dumps all the data to a file."""

        functions.raise_error(location, "location", str)
        functions.raise_error(encoding, "encoding", str)

        self.__events["before_export"]()
        with open(location, "w+", encoding=encoding) as f:
            f.write(jdump({"database": self.__memory}).decode())

        self.__events["after_export"]()
        gccollect()

        return True

    export = dump

    def load(
            self,
            location: str,
            encoding: str = "utf-8",
            overwrite: bool = True) -> bool:
        """Loads a json file to the database."""

        functions.raise_error(location, "location", str)
        functions.raise_error(encoding, "encoding", str)
        functions.raise_error(overwrite, "overwrite", bool)

        self.__events["before_import"]()
        with open(location, "r", encoding=encoding) as f:
            loaded = jload(f.read())

        if "database" not in loaded:
            raise KeyError("Can't find 'database' array in the json.")
        elif not isinstance(loaded["database"], list):
            raise TypeError("'database' Value must be a list.")

        dicts = ({"_id": functions.create_dict_id(i), **i}
                 for i in loaded["database"] if isinstance(i, dict))

        if overwrite:
            self.__memory = list(dicts)
        else:
            self.__memory.extend(dicts)

        self.__events["after_import"]()
        functions.auto_save(
            self.__autosave,
            self.__location,
            self.__memory,
            self.__events)
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

        functions.auto_save(
            self.__autosave,
            self.__location,
            self.__memory,
            self.__events)
        return True

    def collect_garbage(self) -> list:
        """Returns all the garbage data in database."""

        for item in self.__memory:
            if list(item.keys()) == ['_id']:
                yield item

    def clear_garbage(self) -> bool:
        """Remove all the garbage data in database."""

        self.__events["before_garbage_clear"]()
        for item in self.__memory.copy():
            if list(item.keys()) == ['_id']:
                self.__memory.remove(item)

        self.__events["after_garbage_clear"]()
        functions.auto_save(
            self.__autosave,
            self.__location,
            self.__memory,
            self.__events)
        return True

    def copy(self, data: dict, repeat: int = 1) -> bool:
        """Copy the found data(s) to the database."""

        functions.raise_error(data, "data", dict)
        functions.raise_error(repeat, "repeat", int)

        if self.__safemode:
            if repeat < 1:
                raise errors.ValueTooSmall(
                    "The minimum repeat value can be 1. if you don't want limitation, "
                    "make 'SAFE_MODE' option False. (not recommended.)")
            if repeat > 100_000:
                raise errors.ValueTooBig(
                    "The maximum repeat value can be 100,000. if you don't want limitation, "
                    "make 'SAFE_MODE' option False. (not recommended.)")

        def __give_id_to_data(obj):
            self.__events["before_copy"](obj)
            if self.__events["should_copy"](obj):
                result = {
                    **obj,
                    "_id": functions.create_dict_id(obj)
                }

                self.__events["after_copy"](result)
                return result
            else:
                return {}

        while repeat > 0:
            self.__memory.extend(__give_id_to_data(objects) for objects in self.__memory.copy(
            ) if functions.find_item_algorithm(data, objects, self.__useregex))

            self.clear_garbage()
            repeat -= 1

        functions.auto_save(
            self.__autosave,
            self.__location,
            self.__memory,
            self.__events)
        return True

    def copy_one(self, data: dict) -> Union[dict, None]:
        """Copy the found data(s) to the database."""

        functions.raise_error(data, "data", dict)

        for objects in self.__memory.copy():
            if functions.find_item_algorithm(data, objects, self.__useregex):
                self.__events["before_copy"](objects)
                if self.__events["should_copy"](objects):
                    data = {
                        **objects,
                        "_id": functions.create_dict_id(objects)
                    }

                    self.__memory.append(data)
                    self.__events["after_copy"](data)
                    functions.auto_save(
                        self.__autosave,
                        self.__location,
                        self.__memory,
                        self.__events)
                    return data
                else:
                    return None

    def sort_for_key(self, key: str, reverse: bool = False) -> list:
        """Sort database for key. (not saves, just returns sorted version of database.)"""

        functions.raise_error(key, "key", str)
        functions.raise_error(reverse, "reverse", bool)

        return sorted(
            (i for i in self.__memory if isinstance(
                i,
                dict) and key in i.keys()),
            key=lambda v: v[key],
            reverse=reverse)

    def query(self, query: Callable) -> dict:
        """Query search for database. Function must return a bool."""

        for object in self.__memory:
            if query(object):
                yield object

    def start_backup(self, options: dict = {}) -> None:
        """Opens backup for database. if backup is already open, it will raise error."""

        functions.raise_error(options, "options", dict)
        if self.__safemode:
            if self.__backup:
                raise errors.BackupAlreadyStarted(
                    "Backup is already started. if you wan't to ignore this error,"
                    " make 'SAFE_MODE' option False. (not recommended.)")

            if 'TIME' in options and type(options['TIME']) in (float, int,):
                if options['TIME'] < 30:
                    raise errors.ValueTooSmall(
                        "Backup time value is too small. The minimum time can be 30 second. "
                        "if you wan't to ignore this error, make 'SAFE_MODE' option False. (not recommended.)")
                elif options['TIME'] > 31_557_600:
                    raise errors.ValueTooBig(
                        "Backup time value is too big. The maximum time can be 1 year. "
                        "if you wan't to ignore this error, make 'SAFE_MODE' option False. (not recommended.)")
            else:
                options['TIME'] = 60

        self.__backup = True
        self.__backup_time = options['TIME']
        self.__backup_path = options['PATH'] if 'PATH' in options and isinstance(
            options['PATH'], str) else "datagoose_backups"

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
                self.__events["backup"]()
                sleep(self.__backup_time)

        Thread(target=__wrapper, daemon=True).start()
        self.__events["backup_start"]()

    def stop_backup(self) -> bool:
        """Stops backup for database. if backup is closed, it will not effect."""

        self.__backup = False
        self.__events["backup_finish"]()
        return True

    @property
    def is_backup_open(self) -> bool:
        """Returns auto-backup status."""

        return self.__backup
