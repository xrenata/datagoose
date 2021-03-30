# Imports
import json, os, datetime

# Tool Class
class DatagooseTools:
    # Save Function
    def Save(file, key, data):
        database = DatagooseTools.Read(file)
        database.update({key: data})
        with open(file, "w", encoding="utf-8") as f:
            json.dump(database, f)
            f.close()

        return True

    # Remove Function
    def Remove(file, data):
        database = DatagooseTools.Read(file)
        del database[data]

        with open(file, "w", encoding="utf-8") as f:
            json.dump(database, f)
            f.close()

        return True

    # Update Function
    def Update(file, data, overwrite):
        database = DatagooseTools.Read(file)

        def MergeUpdate(dict1, dict2):
            for key, value in dict1.items(): 
                if key not in dict2:
                    dict2[key] = value
                elif isinstance(value, dict):
                    MergeUpdate(value, dict2[key]) 
            return dict2

        if overwrite == False:
            database = MergeUpdate(database, data)
        else:
            database.update(data)

        with open(file, "w", encoding="utf-8") as f:
            json.dump(database, f)
            f.close()

        return True

    # Read Function
    def Read(file, test: bool = False):
        date_first = datetime.datetime.now()
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        if test == True:
            return {
                "data": data,
                "performance": (datetime.datetime.now() - date_first).total_seconds() * 1000
            }
        else:
            return data

    # Find Function
    def Find(file, data, short):
        database = DatagooseTools.Read(file)
        if short:
            data_split = data.split("?=>")

            for split in data_split:
                database = database.get(split)

            return database
        else:
            return database.get(data)

    # Clear Function
    def Clear(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump({}, f)
            f.close()

        return True

# Main
class Datagoose:
    # init
    def __init__(self, name):
        self.name = name
        self.location = f"./datagoose/{self.name}.json"

        # create folder if not exists
        if not os.path.exists("./datagoose"):
            os.mkdir("./datagoose")

        # create database if not exists
        if not os.path.isfile(self.location):
            with open(self.location, "w+", encoding="utf-8") as f:
                json.dump({}, f)


    # database info
    def info(self):
        """
        returns informations about database.
        """
        return {
            "name": self.name,
            "database": {
                "data": DatagooseTools.Read(self.location),
                "location": self.location,
                "size": os.path.getsize(self.location)
            },
        }

    # insert data to database
    def insert(self, key, data):
        """
        insert a data to database.
        """
        return DatagooseTools.Save(self.location, key, data)

    # read data from database
    def read(self, test: bool = False):
        """
        read a data from database.
        """
        return DatagooseTools.Read(self.location, test)

    # find data from database
    def find(self, data, short: bool = True):
        """
        find a data from database.
        """
        return DatagooseTools.Find(self.location, data, short)

    # update data from database
    def update(self, data, overwrite: bool = False):
        """
        update a data from database.
        """
        return DatagooseTools.Update(self.location, data, overwrite)

    # remove data from database
    def remove(self, data):
        """
        remove a data from database.
        """
        return DatagooseTools.Remove(self.location, data)

    # clear the database
    def clear(self):
        """
        clear the database
        """
        return DatagooseTools.Clear(self.location)

    # beautify database
    def beautify(self):
        """
        beautify database.
        """
        database = DatagooseTools.Read(self.location)
        with open(self.location, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4)
            f.close()

        return True

    # minify database
    def minify(self):
        """
        minify database.
        """
        database = DatagooseTools.Read(self.location)
        with open(self.location, "w", encoding="utf-8") as f:
            json.dump(database, f)
            f.close()

        return True