# Imports
import json, os, datetime, random, string, time
from hashlib import sha256

# Main
class Datagoose:
    # init
    def __init__(self, name):
        # check name is not string
        if not isinstance(name, str):
            raise TypeError("Name argument only can be string, not {0}.".format(type(name).__name__))

        self.__name = name
        self.__location = f"./datagoose_files/{self.__name}.json"

        # create folder if not exists
        if not os.path.exists("./datagoose_files"):
            os.mkdir("./datagoose_files")

        # create database if not exists
        if not os.path.isfile(self.__location):
            with open(self.__location, "w+", encoding="utf-8") as f:
                json.dump({"database": []}, f)
                f.close()
        
        # load database
        self.__memory = json.load(open(self.__location, "r", encoding="utf-8"))["database"]

    # creates special id for dict
    def __create_dict_id(data: dict):
        """Creates special id for dict."""
        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        return sha256(f'{time.time()}_{"".join(random.sample(string.ascii_uppercase + string.digits, random.randint(5, 25)))}_{sha256(json.dumps(data).encode()).hexdigest()}_{"".join(random.sample(string.ascii_lowercase + string.digits, random.randint(10, 25)))}'.encode()).hexdigest()

    def read(self):
        """Returns database memory."""

        return self.__memory

    def length(self):
        """Returns database total length."""

        return len(self.__memory)
    
    def save(self, indent=None):
        """Saves database memory to json file."""

        if not isinstance(indent, (int, type(None))):
             raise TypeError("Indent argument only can be int or none, not {0}.".format(type(indent).__name__))

        with open(self.__location, "w+", encoding="utf-8") as f:
            json.dump({"database": self.__memory}, f, indent=indent)
            f.close()

        return True

    def insert_one(self, data: dict):
        """Inserts one data (dict) to database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        hashed = {
            "_id": Datagoose.__create_dict_id(data),
            **data
        }

        self.__memory.append(hashed)

        return hashed
        
    def insert_many(self, *args):
        """Insert many data (dict args) to database."""

        dicts = ({ "_id": Datagoose.__create_dict_id(item), **item } for item in args if isinstance(item, dict))

        self.__memory.extend(list(dicts))
        return dicts

    def find(self, data: dict):
        """Find datas (dict) from database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        return (objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data))

    def find_one(self, data: dict):
        """Find one (first) data (dict) from database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        return [objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)][0]

    def update(self, data: dict, new_data: dict):
        """Update datas (dict) from database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        if not isinstance(new_data, dict):
            raise TypeError("New data argument only can be dict, not {0}.".format(type(new_data).__name__))

        def __update_value(index, new_data):
            for values in new_data.items():
                self.__memory[index][values[0]] = values[1]

            return self.__memory[index]

        return [__update_value(index, new_data) for index, objects in enumerate(self.__memory) if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)]

    def update_one(self, data: dict, new_data: dict):
        """Update one data (dict) from database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        if not isinstance(new_data, dict):
            raise TypeError("New data argument only can be dict, not {0}.".format(type(new_data).__name__))

        for index, objects in enumerate(self.__memory):
            if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data):
                for values in new_data.items():
                    self.__memory[index][values[0]] = values[1]

                return self.__memory[index]

        return {}

    def delete(self, data: dict):
        """Delete datas (dict) from database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        def __remove_item(obj):
            self.__memory.remove(obj)
            return obj

        return [__remove_item(objects) for objects in self.__memory.copy() if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)]

    def delete_one(self, data: dict):
        """Delete one data (dict) from database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        for index, objects in enumerate(self.__memory):
            if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data):
                self.__memory.remove(objects)
                return objects

        return {}

    def count(self, data: dict):
        """Count datas (dict) from database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        return len(list((objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data))))

    def exists(self, data: dict):
        """Checks a data (dict) is in database."""

        if not isinstance(data, dict):
            raise TypeError("Data argument only can be dict, not {0}.".format(type(data).__name__))

        return len(list((objects for objects in self.__memory if len([item for item in data.items() if item[0] in objects and item[1] == objects[item[0]]]) == len(data)))) > 1

    # aliases for exists
    has = exists

    def dump(self, location: str, encoding: str = "utf-8", indent = None):
        """Dumps all the data to a file."""

        if not isinstance(location, str):
            raise TypeError("Location argument only can be string, not {0}.".format(type(location).__name__))

        if not isinstance(encoding, str):
            raise TypeError("Encoding argument only can be string, not {0}.".format(type(encoding).__name__))

        if not isinstance(indent, (type(None), int)):
            raise TypeError("Indent argument only can be int or none-type, not {0}.".format(type(indent).__name__))

        with open(location, "w+", encoding=encoding) as f:
            json.dump({"database": self.__memory}, f, indent=indent)
            f.close()

    def load(self, location: str, encoding: str = "utf-8", overwrite: bool = True):
        """Loads a json file to the database."""

        if not isinstance(location, str):
            raise TypeError("Location argument only can be string, not {0}.".format(type(location).__name__))

        if not isinstance(encoding, str):
            raise TypeError("Encoding argument only can be string, not {0}.".format(type(encoding).__name__))

        if not isinstance(overwrite, bool):
            raise TypeError("Overwrite argument only can be bool, not {0}.".format(type(encoding).__name__))

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
            
        return dicts
