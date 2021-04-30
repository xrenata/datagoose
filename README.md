**Datagoose**
===
Datagoose is __easy to use__ database for *python*. with new datagoose;

- Performance increased. datagoose is now optimized for fastest result!
- Added new functions, and features.
- Can be dumped, also can load a data from JSON file.
  - `<Datagoose>.load()`
  - `<Datagoose>.dump()`
- Bugs fixed.


Updates (1.0.3)
===
- info, length and read is now property.
  - Now you can call with: `<Datagoose>.length` ...
- Added clear()
  - Usage: `<Datagoose>.clear()`

<br>

**Quick Documentation**
===
# Before Start
## You should know these things before using datagoose;
- Datagoose keeps datas in **memory**, _not in a file_.
  - You can save with `<Datagoose>.save()` for remember the database next time.
  
- Datagoose is not a professional database. created for *easy to use* database.

<br>

# Methods
## Quick Start

```
[] - Optinal
[argument_name:argument_type:argument_default_value] - Optinal Argument Name | Optional Argument Type | Optional Argument Default Value

{} - Normal
{argument_name:argument_type} - Argument Name | Argument Type

* - Args
```
```py
from datagoose import Datagoose

database = Datagoose("example")
```

```py
# <Datagoose>.read -> Returns the entire data
  # Return Type: List
  # Example(s):
    full_database = database.read

# <Datagoose>.info -> Returns database info
  # Return Type: Dict
  # Example(s):
    print(database.info)

# <Datagoose>.length -> Returns data length
  # Return Type: Integer
  # Example(s):
    print(database.length)

# <Datagoose>.save([indent:(NoneType | int):None]) -> Saves the database
  # Return Type: Bool
  # Argument: indent
    # Description: Indentation that will write to JSON file.
  # Example(s): 
    database.save(4)
    database.save()

# <Datagoose>.clear() -> Clears the entire database
  # Return Type: Bool
  # Example(s): 
    database.clear()
```
# Inserting Data
```py
# <Datagoose>.insert_one({data:dict}) -> Insert one data to database
  # Return Type: Dict
  # Argument: data
    # Description: The data will be inserted into database.
  # Example(s):
    database.insert_one({
        "name": "John",
        "lastname": "Doe",
        "age": 25,
        "city": "New York",
        "country": "USA",
        "job": "Doctor"
    })

# <Datagoose>.insert_many(*{data:dict}) -> Insert many data to database
  # Return Type: List
  # Args:
    # Description: The data(s) will be inserted into database.
  # Example(s):
    database.insert_many({
        "user": 1,
        "nickname": "normal_guy_100"
    }, {
        "user": 2,
        "nickname": "user_555"
    })
```

<p style="font-size: 18px;">Note: Datagoose adds unique hash ("_id") to every document that inserted. Make sure do not add same "_id" to documents.</p>

```py
# Example

database.insert_one({ "_id": 1, "name": "an_user" })
database.insert_one({ "_id": 1, "name": "another_user" })
# This example will not give an error. But when you use delete or update, datagoose may confuse while find the object.
```
# Finding Data
```py
# <Datagoose>.find({data:dict}) -> Find data from database
  # Return Type: List
  # Argument: data
    # Description: The data will find from database.
  # Example(s):
    found = list(database.find({
        "age": 25
    }))
    print(found) # -> [{'name': 'test', 'age': 25}, {'name': 'test2', 'age': 25}...]

# <Datagoose>.find_one({data:dict}) -> Find one data from database
  # Return Type: Dict
  # Argument: data
    # Description: The data will find from database.
  # Example(s):
    result = database.find_one({
        "user_id": 295818619
    })
    print(result["nickname"])
```
# Updating Data
```py
# <Datagoose>.update({data:dict}, {new_data:dict}) -> Update data from database
  # Return Type: List
  # Argument: data
    # Description: The data will find from database.
  # Argument: new_data
    # Description: The data will be changed with found data.
  # Example(s):
    database.update({
        "age": 25
    }, {
        "age": 26
    }) # Now every data has 'age' and 'age' key value is 25, changed with 'age' = 26 
    
# <Datagoose>.update_one({data:dict}, {new_data:dict}) -> Find one data from database
  # Return Type: Dict
  # Argument: data
    # Description: The data will find from database.
  # Argument: new_data
    # Description: The data will be changed with found data.
  # Example(s):
    database.update_one({
        "user_id": 2486718956
    }, {
        "banned": True,
        "ban_time": "30d"
    }) # Now only one data updated.
```

<p style="font-size: 18px;">Note: When you add new key and value to new_data dictionary, it will insert into data.</p>

```py
# Example

database.insert_one({ "_id": 1, "name": "an_user" })
database.update_one({
    "_id": 1
}, {
    "total_kill": 16
})
# Now our data is:
{
    "_id": 1,
    "name": "an_user",
    "total_kill": 16
}
```
# Deleting Data
```py
# <Datagoose>.delete({data:dict}) -> Delete data from database
  # Return Type: List
  # Argument: data
    # Description: The data will be deleted from database.
  # Example(s):
    database.delete({
        "total_hours": 1
    }) # Now datagoose deleted all datas contains key 'total_hours' and key value is 1

# <Datagoose>.delete_one({data:dict}) -> Delete one data from database
  # Return Type: Dict
  # Argument: data
    # Description: The data will be deleted from database.
  # Example(s):
    database.delete_one({
        "user_id": 6811
    })
```
# Count & Exists
```py
# <Datagoose>.count({data:dict}) -> Count all data contains data argument
  # Return Type: Integer
  # Argument: data
    # Description: The data will count.
  # Example(s):
    database.count({
        "name": "John",
        "age": 40
    }) # -> 6157

# <Datagoose>.exists({data:dict}) -> Checks data exists
  # Return Type: Bool
  # Argument: data
    # Description: The data will be checked.
  # Example(s):
    result = database.exists({
        "name": "a_guy_11"
    })

    if result:
        database.delete_one({ "name": "a_guy_11" })
```

<p style="font-size: 18px;">Note: "has" is an alias for exists.</p>

```py
# Example

result = database.has({
    "name": "a_guy_11"
})

if result:
    database.delete_one({ "name": "a_guy_11" })

# is same with:

result = database.exists({
    "name": "a_guy_11"
})

if result:
    database.delete_one({ "name": "a_guy_11" })
```
# Load & Dump
```py
# <Datagoose>.dump({location:str}, [encoding:str:utf-8], [indent:(int | NoneType):None]) -> Dumps the database to JSON file.
  # Return Type: None
  # Argument: location
    # Description: The location that will dump.
  # Argument: encoding
    # Description: Encoding while write.
  # Argument: indent
    # Description: The indentation while dump the JSON file.
  # Example(s):
    # 1.
      database.dump("./dump.json")
    # 2.
      database.dump("./dump.json", indent=4)

# <Datagoose>.load({location:str}, [encoding:str:utf-8], [overwrite:bool:True]) -> Load database from JSON file.
  # Return Type: Dict
  # Argument: location
    # Description: The location that will dump.
  # Argument: encoding
    # Description: Encoding while write.
  # Argument: overwrite
    # Description: If True, it will delete old data and paste loaded one. Else, it will extend data with loaded JSON.
  # Example(s):
    # 1.
      database.load("./old_database.json", overwrite=False)
    # 2.
      database.load("./old_database.json")
```

<p style="font-size: 18px;">Note: for .load(), the JSON will loaded must have 'database' key and value must be a list. Also in list, values must be dict.</p>

<p style="font-size: 18px;">Note: "export" is an aliases for .dump().</p>

```py
# Example

database.export("./dump.json", indent=4)

# is same with:

database.dump("./dump.json", indent=4)
```