**Datagoose**
===
Datagoose is __easy to use__ database for *python*. with datagoose;

- Best performance. Datagoose is a lightweight database.
- Methods that makes your job easier.
- Regex supports.
- Safe to use.
- Auto or manual save, for who wants better performance.
- Easy to use database. Created for everyone.
- Rich options. includes hash keys, database path, garbage leak option and more.
- Auto backup
- Can be dumped, also can load a data from JSON file.
  - `<Datagoose>.load()`
  - `<Datagoose>.dump()`

# Update (1.2.0)
- Fixed folder bug
- Added start & stop auto-backup.

**Quick Documentation**
===
# Before Start
## You should know these things before using datagoose;
- Datagoose keeps datas in **memory**, _not in a file_.
  - You can save with `<Datagoose>.save()` for remember the database next time.
  - Also now you can enable `AUTO_SAVE` option for auto-saving.
  
- Datagoose is not a professional database. created for *easy to use* database.

<br>

# Performance
Test Result (Auto-Save Enabled):
- 100 Data with insert many:
  - ```
    Starting
    Finished In: 0:00:00.004998
    ```
- 1,000 Data with insert many:
  - ```
    Starting
    Finished In: 0:00:00.051003
    ```
- 10,000 Data with insert many:
  - ```
    Starting
    Finished In: 0:00:00.468040
    ```
- 100,000 Data with insert many:
  - ```
    Starting
    Finished In: 0:00:04.680622
    ```
- 1,000,000 Data with insert many:
  - ```
    Starting
    Finished In: 0:00:49.217345
    ```

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

## Options
```py
# Options must be a dict. lets get informations about current options.

# PATH:
  # Type: String
  # Description: Custom path for JSON file.
  # Note: please add path like: "databases/datagoose" not "./databases/datagoose/"
  # Default: datagoose_files
# AUTO_SAVE:
  # Type: Bool
  # Description: When enabled, auto-saves the database when an action performed.
  # Default: False
# LEAK_GARBAGE:
  # Type: Bool
  # Description: Enables adding garbage data to database. not recommending.
  # Default: False
# HASHING:
  # Type: List
  # Description: Key list for replace data with sha256 hash when inserted.
  # Default: []
# SAFE_MODE:
  # Type: Bool
  # Description: Enable/Disable safe mode. do not recommending to disable this option. if you know what are you doing, then good luck. 
  # Default: True

# Example:
database = Datagoose("example", {
    "AUTO_SAVE": True, # Now it will save-auto when an action performed.
    "HASHING": [
        "PASSWORD" # Now when you insert a data. if data has 'PASSWORD' key, it will replace value with sha256 hash for value.
    ]
})
```

```py
# <Datagoose>.read() -> Returns the entire data
  # Return Type: List
  # Example(s):
    full_database = database.read()

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
  # Return Type: Bool
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
  # Return Type: Generator
  # Argument: data
    # Description: The data will find from database.
  # Example(s):
    found = database.find({
        "age": 25
    }) # -> {'name': 'test', 'age': 25}, {'name': 'test2', 'age': 25} ...

    for result in found:
      print(result)

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
# Using Regex
```py
# Quick Example For Using Regex in Datagoose.

for i in db.find({"ANSWER": r"yes|y"}):
    print(i)
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
# Copying Data
```py
# <Datagoose>.copy({data:dict}, [repeat:int:1]) -> Copy data to database
  # Return Type: Bool
  # Argument: data
    # Description: The data will be copied to database.
  # Argument: repeat
    # Description: Repeat number for copy. Must be between 1 - 100000
  # Example(s):
    database.copy({
        "total_hours": 1
    }) # Now datagoose copied all data contains these informations.

# <Datagoose>.repeat_one({data:dict}) -> Copy one data to database
  # Return Type: Dict
  # Argument: data
    # Description: The data will be copied to database.
  # Example(s):
    database.copy_one({
        "user_id": 6811
    })
```
# Collecting Garbage Datas
```py
# <Datagoose>.collect_garbage() -> Returns all garbage data in database
  # Return Type: Generator
  # Example(s):
    getgc = database.collect_garbage()
    for garbage in getgc:
      print("Found Garbage Data: ", garbage)

# <Datagoose>.clear_garbage() -> Clear all garbage data in database
  # Return Type: Bool
  # Example(s):
    database.clear_garbage()
```
# Sorting Database
```py
# <Datagoose>.sort_for_key({key:str}, [reverse:bool:False]) -> Sort database for key.
  # Return Type: List
  # Argument: key
    # Description: The key for sort.
  # Argument: reverse
    # Description: Reverse the result.
  # Example(s):
    point_list = database.sort_for_key("point", reverse=True)
    winner = point_list[0]

    print(f"Congrats, {winner['name']}. You won the game!")
```

<p style="font-size: 18px;">Note: .sort_for_key() not changes the database, just returns sorted version of database.</p>

# Auto-Backup \*New in v1.2.0
```py
# <Datagoose>.start_backup([options:dict:{}]) -> Starts backup for every x second. Raises error when already started.
  # Return Type: None
  # Argument: options
    # Description: Options for auto-backup
  # Example(s):
    database.start_backup({
      "TIME": 60 # Second for repeat time. Minimum 30 second, Maximum 31,557,600 (1 year) second.
      "PATH": "database/backups" # Path for backup files.
    })

# <Datagoose>.stop_backup() -> Stops backup loop. Will not effect if already stopped.
  # Return Type: Bool
  # Example(s):
    database.stop_backup()
```