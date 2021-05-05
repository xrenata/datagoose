from json import dump as jdump
from json import dumps as jdumps
from json import load as jload
from os import path as opath
from os import mkdir
from random import sample, randint
from string import ascii_lowercase, ascii_uppercase, digits
from time import time, sleep
from re import findall
from hashlib import sha256
from datetime import datetime
from threading import Thread

class GarbageDataError(Exception):
    pass

class ValueTooSmall(Exception):
    pass

class ValueTooBig(Exception):
    pass

class BackupAlreadyStarted(Exception):
    pass

class Datagoose:
    def __init__(self, name: str, options: dict = {}):
        if not isinstance(name, str):
            raise TypeError("Name argument only can be string, not {0}.".format(type(name).__name__))
            
        if not isinstance(options, dict):
            raise TypeError("Options argument only can be dict, not {0}.".format(type(path).__name__))

        self.__path = options['PATH'] if 'PATH' in options and type(options['PATH']) == str else "datagoose_files"
        self.__autosave = options['AUTO_SAVE'] if 'AUTO_SAVE' in options and type(options['AUTO_SAVE']) == bool else False
        self.__leakgarbage = options['LEAK_GARBAGE'] if 'LEAK_GARBAGE' in options and type(options['LEAK_GARBAGE']) == bool else False
        self.__hashing = [i for i in options['HASHING'] if type(i) == str] if 'HASHING' in options and type(options['HASHING']) == list else []
        self.__safemode = options['SAFE_MODE'] if 'SAFE_MODE' in options and type(options['SAFE_MODE']) == bool else True

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

        if not opath.exists(f"./{self.__path}"):
            mkdir(f"./{self.__path}")

        if not opath.isfile(self.__location):
            file = open(self.__location, "w+", encoding="utf-8")
            jdump({"database": []}, file)
            file.close()

        self.__memory = jload(open(self.__location, "r", encoding="utf-8"))["database"]

    def __auto_save(option: bool, location: str, memory: list):
        if option:
            file = open(location, "w+", encoding="utf-8")
            jdump({"database": memory}, file, indent=4)
            file.close()

    def __garbage_check(option: bool, data: dict):
        if not option and not bool(data):
            raise GarbageDataError("You can't insert garbage data right now. if you want to disable this setting (not recommended), make 'LEAK_GARBAGE' True.")

    def __hash_keys(keys: list, data: dict):
        for key in data.keys():
            if key in keys:
                data[key] = sha256(str(data[key]).encode()).hexdigest()

        return data

    def __raise_error(value: str, argument_name: str, check):
        if type(check) == tuple:
            if not type(value) in check:
                raise TypeError(f"Argument '{argument_name}' type must be {' / '.join([i.__name__ for i in check])}, not {type(value).__name__}.")
        else:
            if not isinstance(value, check):
                raise TypeError(f"Argument '{argument_name}' type must be {check.__name__}, not {type(value).__name__}.")

    def __create_dict_id(data: dict) -> str:
        """Creates special id for dict."""
        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        return sha256(f'{time()}_{"".join(sample(digits, 10))}_{sha256(jdumps(data).encode()).hexdigest()}_{"".join(sample(ascii_lowercase, randint(10, 25)))}'.encode()).hexdigest()

    def read(self) -> list:
        """Returns database memory."""

        return self.__memory
    
    @property
    def length(self) -> int:
        """Returns database total length."""

        return len(self.__memory)
       
    def save(self, indent=None) -> bool:
        """Saves database memory to json file."""

        Datagoose.__raise_error(indent, "indent", (int, type(None)))

        file = open(self.__location, "w+", encoding="utf-8")
        jdump({"database": self.__memory}, file, indent=indent)
        file.close()

        return True

    def insert_one(self, data: dict) -> dict:
        """Inserts one data (dict) to database."""

        Datagoose.__raise_error(data, "data", dict)
        Datagoose.__garbage_check(self.__leakgarbage, data)

        hashed = Datagoose.__hash_keys(self.__hashing, {
            "_id": Datagoose.__create_dict_id(data),
            **data
        })

        self.__memory.append(hashed)
        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)

        return hashed
        
    def insert_many(self, *args) -> bool:
        """Insert many data (dict args) to database."""

        def __insert_data(data): 
            Datagoose.__garbage_check(self.__leakgarbage, data)
            return Datagoose.__hash_keys(self.__hashing, {
                "_id": Datagoose.__create_dict_id(data),
                **data
            })

        self.__memory.extend(__insert_data(item) for item in args if isinstance(item, dict))
        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
        return True

    def find(self, data: dict) -> type(x for x in [1, 2, 3]):
        """Find datas (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        for objects in self.__memory:
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data):
                yield objects
    
    def find_one(self, data: dict) -> dict:
        """Find one (first) data (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        for objects in self.__memory:
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data):
                return objects

        return {}
    
    def update(self, data: dict, new_data: dict) -> list:
        """Update datas (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)
        Datagoose.__raise_error(new_data, "new_data", dict)

        def __update_value(index, new_data):
            for values in new_data.items():
                self.__memory[index][values[0]] = values[1]

            return self.__memory[index]

        result = [__update_value(index, new_data) for index, objects in enumerate(self.__memory) if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data)]
        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
        return result
    
    def update_one(self, data: dict, new_data: dict) -> dict:
        """Update one data (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        Datagoose.__raise_error(new_data, "new_data", dict)

        for index, objects in enumerate(self.__memory):
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data):
                for values in new_data.items():
                    self.__memory[index][values[0]] = values[1]

                Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
                return self.__memory[index]

        return {}
    
    def delete(self, data: dict) -> list:
        """Delete datas (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        def __remove_item(obj):
            self.__memory.remove(obj)
            return obj

        result = [__remove_item(objects) for objects in self.__memory.copy() if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data)]
        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
        return result
    
    def delete_one(self, data: dict) -> dict:
        """Delete one data (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        for index, objects in enumerate(self.__memory):
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data):
                self.__memory.remove(objects)
                
                Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
                return objects

        return {}
    
    def count(self, data: dict) -> int:
        """Count datas (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        return len(list((objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data))))
    
    def exists(self, data: dict) -> bool:
        """Checks a data (dict) is in database."""

        Datagoose.__raise_error(data, "data", dict)

        return len(list((objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data)))) > 1

    has = exists
    
    def dump(self, location: str, encoding: str = "utf-8", indent = None) -> bool:
        """Dumps all the data to a file."""

        Datagoose.__raise_error(location, "location", str)
        Datagoose.__raise_error(encoding, "encoding", str)
        Datagoose.__raise_error(indent, "indent", (int, type(None)))

        file = open(location, "w+", encoding="utf-8")
        jdump({"database": self.__memory}, file, indent=indent)
        file.close()

        return True

    export = dump

    def load(self, location: str, encoding: str = "utf-8", overwrite: bool = True) -> bool:
        """Loads a json file to the database."""

        Datagoose.__raise_error(location, "location", str)
        Datagoose.__raise_error(encoding, "encoding", str)
        Datagoose.__raise_error(overwrite, "overwrite", bool)

        loaded = jload(open(location, "r", encoding=encoding))

        if not "database" in loaded:
            raise KeyError("Can't find 'database' array in the json.")
        elif not isinstance(loaded["database"], list):
            raise TypeError("'database' Value must be a list.")

        dicts = ({ "_id": Datagoose.__create_dict_id(i), **i } for i in loaded["database"] if isinstance(i, dict))

        if overwrite:
            self.__memory = list(dicts)
        else:
            self.__memory.extend(dicts)
            
        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
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
        
        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
        return True

    def collect_garbage(self) -> type(x for x in [1, 2, 3]):
        """Returns all the garbage data in database."""

        for item in self.__memory:
            if list(item.keys()) == ['_id']:
                yield item

    def clear_garbage(self) -> bool:
        """Remove all the garbage data in database."""

        for item in self.__memory.copy():
            if list(item.keys()) == ['_id']:
                self.__memory.remove(item)

        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
        return True
        
    def copy(self, data: dict, repeat: int = 1) -> bool:
        """Copy the found data(s) to the database."""

        Datagoose.__raise_error(data, "data", dict)
        Datagoose.__raise_error(repeat, "repeat", int)

        if self.__safemode:
            if repeat < 1:
                raise ValueTooSmall("The minimum repeat value can be 1. if you don't want limitation, make 'SAFE_MODE' option False. (not recommended.)")
            if repeat > 100_000:
                raise ValueTooBig("The maximum repeat value can be 100,000. if you don't want limitation, make 'SAFE_MODE' option False. (not recommended.)")

        def __give_id_to_data(data):
            return {
                **data,
                "_id": Datagoose.__create_dict_id(data)
            }

        while repeat > 0:
            self.__memory.extend(
                __give_id_to_data(objects) for objects in self.__memory.copy() if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data)
            )

            repeat -= 1

        Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
        return True
        
    def copy_one(self, data: dict) -> dict:
        """Copy the found data(s) to the database."""

        Datagoose.__raise_error(data, "data", dict)

        for objects in self.__memory.copy():
            if len([item for item in data.items() if item[0] in objects and (item[1] == objects[item[0]] or ( (type(item[1]), type(objects[item[0]])) == (str, str, ) and findall(item[1], objects[item[0]])))]) == len(data):
                data = {
                    **objects,
                    "_id": Datagoose.__create_dict_id(objects)
                }

                self.__memory.append(data)
                Datagoose.__auto_save(self.__autosave, self.__location, self.__memory)
                return data

    def sort_for_key(self, key: str, reverse: bool = False) -> list:
        """Sort database for key. (not saves, just returns sorted version of database.)"""

        Datagoose.__raise_error(key, "key", str)
        Datagoose.__raise_error(reverse, "reverse", bool)

        return sorted((i for i in self.__memory if type(i) == dict and key in i.keys()), key=lambda v: v[key], reverse=reverse)

    def start_backup(self, options: dict = {}) -> None:
        """Opens backup for database. if backup is already open, it will raise error."""

        Datagoose.__raise_error(options, "options", dict)
        if self.__safemode:
            if self.__backup:
                raise BackupAlreadyStarted("Backup is already started. if you wan't to ignore this error, make 'SAFE_MODE' option False. (not recommended.)")

            if 'TIME' in options and type(options['TIME']) in (float, int, ):
                if options['TIME'] < 30:
                    raise ValueTooSmall("Backup time value is too small. The minimum time can be 30 second. if you wan't to ignore this error, make 'SAFE_MODE' option False. (not recommended.)")
                elif options['TIME'] >  31_557_600:
                    raise ValueTooBig("Backup time value is too big. The maximum time can be 1 year. if you wan't to ignore this error, make 'SAFE_MODE' option False. (not recommended.)")
            else:
                options['TIME'] = 60


        self.__backup = True
        self.__backup_time = options['TIME']
        self.__backup_path = options['PATH'] if 'PATH' in options and type(options['PATH']) == str else "datagoose_backups"

        def __wrapper():
            while self.__backup:
                last_path = "./"
                for path in self.__backup_path.split("/"):
                    if not opath.exists(f"{last_path}{path}"):
                        mkdir(f"{last_path}{path}")
                    last_path += f"{path}/"

                file = open(f"./{self.__backup_path}/backup_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.json", "w+", encoding="utf-8")
                jdump({"database": self.__memory}, file, indent=4)
                file.close()

                sleep(self.__backup_time)

        Thread(target=__wrapper, daemon=True).start()

    def stop_backup(self) -> bool:
        """Stops backup for database. if backup is closed, it will not effect."""

        self.__backup = False
        return True