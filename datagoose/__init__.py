import json, os, datetime, random, string, time
from hashlib import sha256

class Datagoose:
    def __init__(self, name: str, path: str = "datagoose_files"):
        if not isinstance(name, str):
            raise TypeError("Name argument only can be string, not {0}.".format(type(name).__name__))
            
        if not isinstance(path, str):
            raise TypeError("Path argument only can be string, not {0}.".format(type(path).__name__))

        self.__name = name
        self.__location = f"./{path}/{self.__name}.json"


        if not os.path.exists(f"./{path}"):
            os.mkdir(f"./{path}")


        if not os.path.isfile(self.__location):
            file = open(self.__location, "w+", encoding="utf-8")
            json.dump({"database": []}, file)
            file.close()
        

        self.__memory = json.load(open(self.__location, "r", encoding="utf-8"))["database"]


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

        return sha256(f'{time.time()}_{"".join(random.sample(string.ascii_uppercase + string.digits, random.randint(5, 25)))}_{sha256(json.dumps(data).encode()).hexdigest()}_{"".join(random.sample(string.ascii_lowercase + string.digits, random.randint(10, 25)))}'.encode()).hexdigest()

    
    @property
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
        json.dump({"database": self.__memory}, file, indent=indent)
        file.close()

        return True


    def insert_one(self, data: dict) -> dict:
        """Inserts one data (dict) to database."""

        Datagoose.__raise_error(data, "data", dict)

        hashed = {
            "_id": Datagoose.__create_dict_id(data),
            **data
        }

        self.__memory.append(hashed)

        return hashed
        
    
    def insert_many(self, *args) -> list:
        """Insert many data (dict args) to database."""

        dicts = ({ "_id": Datagoose.__create_dict_id(item), **item } for item in args if isinstance(item, dict))

        self.__memory.extend(list(dicts))
        return list(dicts)

    
    def find(self, data: dict) -> list:
        """Find datas (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        return list((objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)))

    
    def find_one(self, data: dict) -> dict:
        """Find one (first) data (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        for objects in self.__memory:
            if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data):
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

        return [__update_value(index, new_data) for index, objects in enumerate(self.__memory) if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)]

    
    def update_one(self, data: dict, new_data: dict) -> dict:
        """Update one data (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        Datagoose.__raise_error(new_data, "new_data", dict)

        for index, objects in enumerate(self.__memory):
            if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data):
                for values in new_data.items():
                    self.__memory[index][values[0]] = values[1]

                return self.__memory[index]

        return {}

    
    def delete(self, data: dict) -> list:
        """Delete datas (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        def __remove_item(obj):
            self.__memory.remove(obj)
            return obj

        return [__remove_item(objects) for objects in self.__memory.copy() if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)]

    
    def delete_one(self, data: dict) -> dict:
        """Delete one data (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        for index, objects in enumerate(self.__memory):
            if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data):
                self.__memory.remove(objects)
                return objects

        return {}

    
    def count(self, data: dict) -> int:
        """Count datas (dict) from database."""

        Datagoose.__raise_error(data, "data", dict)

        return len(list((objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data))))

    
    def exists(self, data: dict) -> bool:
        """Checks a data (dict) is in database."""

        Datagoose.__raise_error(data, "data", dict)

        return len(list((objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)))) > 1


    has = exists

    
    def dump(self, location: str, encoding: str = "utf-8", indent = None) -> bool:
        """Dumps all the data to a file."""

        Datagoose.__raise_error(location, "location", str)
        Datagoose.__raise_error(encoding, "encoding", str)
        Datagoose.__raise_error(indent, "indent", (int, type(None)))

        file = open(location, "w+", encoding="utf-8")
        json.dump({"database": self.__memory}, file, indent=indent)
        file.close()

        return True


    export = dump

    
    def load(self, location: str, encoding: str = "utf-8", overwrite: bool = True) -> list:
        """Loads a json file to the database."""

        Datagoose.__raise_error(location, "location", str)
        Datagoose.__raise_error(encoding, "encoding", str)
        Datagoose.__raise_error(overwrite, "overwrite", bool)

        loaded = json.load(open(location, "r", encoding=encoding))

        if not "database" in loaded:
            raise NameError("Can't find 'database' array in the json.")
        elif not isinstance(loaded["database"], list):
            raise TypeError("'database' Value must be a list.")

        dicts = ({ "_id": Datagoose.__create_dict_id(i), **i } for i in loaded["database"] if isinstance(i, dict))

        if overwrite:
            self.__memory = list(dicts)
        else:
            self.__memory.extend(list(dicts))
            
        return list(dicts)


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
        return True