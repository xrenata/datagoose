# Imports
import json, os, datetime, time

# Tool Class
class DatagooseTools:
    # Read Database
    def LoadDatabase(file):
        return json.loads(open(file, "r", encoding="utf-8").read())

    # Save Function
    def SaveFile(file, new):
        database = DatagooseTools.LoadDatabase(file)
        new["__time__"] = time.time()
        database["database"].append(new)
        
        with open(file, "w", encoding="utf-8") as f:
            json.dump(database, f)
            f.close()

        return new

    # Save Many Data Function
    def SaveManyToFile(file, args):
        database = DatagooseTools.LoadDatabase(file)
        addeds = []
        for data in args:
            if type(data).__name__ == "dict":
                data["__time__"] = time.time()
                database["database"].append(data)
                addeds.append(data)
                
                with open(file, "w", encoding="utf-8") as f:
                    json.dump(database, f)
                    f.close()
            else:
                continue

        return addeds

    # Find Function
    def FindFile(file, data):
        database = DatagooseTools.LoadDatabase(file)
        db_copy = database["database"].copy()
        founds = []

        if data == None:
            founds = [obj for i, obj in enumerate(db_copy)]
            return founds

        for index, objects in enumerate(db_copy):
            sameValue = 0
            for item in data.items():
                if item[0] in objects and item[1] == objects.get(item[0]):
                    sameValue += 1

            if sameValue == len(list(data)):
                founds.append(objects)

        return founds

    # Find One Function
    def FindOneFromFile(file, data):
        database = DatagooseTools.LoadDatabase(file)
        db_copy = database["database"].copy()

        for index, objects in enumerate(db_copy):
            sameValue = 0
            for item in data.items():
                if item[0] in objects and item[1] == objects.get(item[0]):
                    sameValue += 1

            if sameValue == len(list(data)):
                return objects

        return None

    # Update Function
    def UpdateFile(file, data, new):
        database = DatagooseTools.LoadDatabase(file)
        db_copy = database["database"].copy()
        founds = []

        for index, objects in enumerate(db_copy):
            sameValue = 0
            for item in data.items():
                if item[0] in objects and item[1] == objects.get(item[0]):
                    sameValue += 1

            if sameValue == len(list(data)):
                founds.append(objects)
                for values in new.items():
                    database["database"][index][values[0]] = values[1]

                    with open(file, "w", encoding="utf-8") as f:
                        json.dump(database, f)
                        f.close()

        return founds

    # Update One Function
    def UpdateOneFromFile(file, data, new):
        database = DatagooseTools.LoadDatabase(file)
        db_copy = database["database"].copy()

        for index, objects in enumerate(database["database"]):
            sameValue = 0
            for item in data.items():
                if item[0] in objects and item[1] == objects.get(item[0]):
                    sameValue += 1

            if sameValue == len(list(data)):
                for values in new.items():
                    database["database"][index][values[0]] = values[1]

                    with open(file, "w", encoding="utf-8") as f:
                        json.dump(database, f)
                        f.close()

                return objects

        return None

    # Delete Function
    def DeleteFromFile(file, data):
        database = DatagooseTools.LoadDatabase(file)
        db_copy = database["database"].copy()
        deleted = []

        for index, objects in enumerate(db_copy):
            sameValue = 0
            for item in data.items():
                if item[0] in objects and item[1] == objects.get(item[0]):
                    sameValue += 1

            if sameValue == len(list(data)):
                database["database"].remove(objects)

                with open(file, "w", encoding="utf-8") as f:
                    json.dump(database, f)
                    f.close()

                deleted.append(objects)

        return deleted

    # Delete One Function
    def DeleteOneFromFile(file, data):
        database = DatagooseTools.LoadDatabase(file)
        db_copy = database["database"].copy()

        for index, objects in enumerate(db_copy):
            sameValue = 0
            for item in data.items():
                if item[0] in objects and item[1] == objects.get(item[0]):
                    sameValue += 1

            if sameValue == len(list(data)):
                database["database"].remove(objects)

                with open(file, "w", encoding="utf-8") as f:
                    json.dump(database, f)
                    f.close()

                return objects

        return None

    # Count Document Function
    def CountFromFile(file, data):
        database = DatagooseTools.LoadDatabase(file)
        db_copy = database["database"].copy()

        counts = 0
        for index, objects in enumerate(database["database"]):
            sameValue = 0
            for item in data.items():
                if item[0] in objects and item[1] == objects.get(item[0]):
                    sameValue += 1

            if sameValue == len(list(data)):
                counts += 1

        return counts

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
                json.dump({"database": []}, f)


    # database info
    def info(self):
        """
        returns informations about database.
        """
        return {
            "name": self.name,
            "location": self.location,
            "size": os.path.getsize(self.location)
        }

    def insert(self, data):
        """
        insert a data to database
        """
        return DatagooseTools.SaveFile(self.location, data)

    def insert_many(self, *args):
        """
        insert many data to database
        """
        return DatagooseTools.SaveManyToFile(self.location, args)

    def find(self, data = None):
        """
        find data from database
        """
        return DatagooseTools.FindFile(self.location, data)

    def find_one(self, data = None):
        """
        find one data from database
        """
        return DatagooseTools.FindOneFromFile(self.location, data)

    def update(self, data, new):
        """
        update data from database
        """
        return DatagooseTools.UpdateFile(self.location, data, new)

    def update_one(self, data, new):
        """
        update one data from database
        """
        return DatagooseTools.UpdateOneFromFile(self.location, data, new)

    def delete(self, data):
        """
        delete data from database
        """
        return DatagooseTools.DeleteFromFile(self.location, data)

    def delete_one(self, data):
        """
        delete one data from database
        """
        return DatagooseTools.DeleteOneFromFile(self.location, data)

    def count(self, data):
        """
        count documents from database
        """
        return DatagooseTools.CountFromFile(self.location, data)

    def beautify(self):
        """
        beautify database
        """
        database = DatagooseTools.LoadDatabase(self.location)
        with open(self.location, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=4)

        return True

    def minify(self):
        """
        minify database
        """
        database = DatagooseTools.LoadDatabase(self.location)
        with open(self.location, "w", encoding="utf-8") as f:
            json.dump(database, f)

        return True

    def reset(self):
        """
        reset the database (danger zone!)
        """
        with open(self.location, "w", encoding="utf-8") as f:
            json.dump({"database": []}, f)

        return True