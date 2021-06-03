<img alt="logo" src="https://raw.githubusercontent.com/5elenay/datagoose/main/logo.png">

**Datagoose**
===
Datagoose is an __easy to use__ JSON based database for python.

[![Version](https://badge.fury.io/py/datagoose.svg)](https://pypi.python.org/pypi/datagoose)
[![Downloads](https://img.shields.io/pypi/dm/datagoose.svg)](https://pypi.python.org/pypi/datagoose)
![Stars](https://img.shields.io/github/stars/5elenay/datagoose)
![Commits](https://img.shields.io/github/commit-activity/w/5elenay/datagoose)

# With Datagoose:
- Best performance. Datagoose is a lightweight database.
- Methods that makes your job easier.
- Regex supports.
  - You must enable `USE_REGEX` option.
- Safe to use.
- Auto or manual save, for who wants better performance.
- Easy to use database. Created for everyone.
- Rich options. includes hash keys, database path, regexp and more.
- Auto backup
- Can be dumped, also can load a data from JSON file.
  - `<Datagoose>.load()`
  - `<Datagoose>.dump()`

# Update (1.6.0)
- Added `PIN` option for encryption.
  - If you used `1.5.0` encryption, use PIN `2` or dump your database and make a new one. 
- Added `.replace`, `.replace_one` methods.
- Added 3 new event.
- Added `ENCRYPTED` option for auto-backup.
- Removed `.save_with_indent` method.

# Download
You can download with `pip install -U datagoose` ([PyPi Page](https://pypi.org/project/datagoose/)) or, you can use with source code.

**Note**: Current stable version is `1.6.1`. You can download stable version with `pip install datagoose==1.6.1` ([PyPi](https://pypi.org/project/datagoose/1.6.1/)).

**Quick Documentation**
===
# Before Start
## You should know these things before using datagoose;
- Datagoose keeps data in **memory**, _not in a file_.
  - You can save with `<Datagoose>.save()` for remember the database next time.
  - Also now you can enable `AUTO_SAVE` option for auto-saving.
  
- Datagoose is not a professional database.

<br>

# Performance
Test Result (Auto-Save Enabled):
- 100 Data with insert many:
  - ```
    Starting Insert...
    Inserting Finished in  0:00:00.007002
    ```
- 1,000 Data with insert many:
  - ```
    Starting Insert...
    Inserting Finished in  0:00:00.032004
    ```
- 10,000 Data with insert many:
  - ```
    Starting Insert...
    Inserting Finished in  0:00:00.278020
    ```
- 100,000 Data with insert many:
  - ```
    Starting Insert...
    Inserting Finished in  0:00:02.808687
    ```
- 1,000,000 Data with insert many:
  - ```
    Starting Insert...
    Inserting Finished in  0:00:31.908481
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
# HASHING:
  # Type: List
  # Description: Key list for replace data with sha256 hash when inserted.
  # Default: []
# SAFE_MODE:
  # Type: Bool
  # Description: Enable/Disable safe mode. do not recommending to disable this option. if you know what are you doing, then good luck. 
  # Default: True
# USE_REGEX:
  # Type: Bool
  # Description: Enable/Disable regex option. 
  # Default: False
# ENCRYPTED:
  # Type: Bool
  # Description: Enable/Disable encrypting data. 
  # Default: False
# PIN:
  # Type: Int
  # Description: Decryption key for encryption. you should not expose this key.
  # Default: 2

# Example:
database = Datagoose("example", {
    "AUTO_SAVE": True,
    "USE_REGEX": True,
    "ENCRYPTED": True,
    "PIN": 69 * 420,
    "HASHING": [
        "PASSWORD"
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

# <Datagoose>.length -> Returns total data count
  # Return Type: Integer
  # Example(s):
    print(database.length)

# <Datagoose>.uptime -> Returns database uptime
  # Return Type: datetime.timedelta
  # Example(s):
    print(database.uptime)

# <Datagoose>.save() -> Saves the database
  # Return Type: Bool
  # Example(s): 
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
  # Return Type: Generator? (Dict Yield)
  # Argument: data
    # Description: The data will find from database.
  # Example(s):
    found = database.find({
        "age": 25
    }) # -> {'name': 'test', 'age': 25}, {'name': 'test2', 'age': 25} ...

    for result in found:
      print(result)

# <Datagoose>.query({check:function}) -> Query data from database with function. *New in 1.4.1*
  # Return Type: Generator? (Dict Yield)
  # Argument: check
    # Description: Functions for check, must return bool.
  # Example(s):
    for i in database.query(lambda data: 'POINT' in data and data['POINT'] >= 1337):
      print(i)

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
    
# <Datagoose>.update_one({data:dict}, {new_data:dict}) -> Update one data from database
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
# Replace Data
```py
# <Datagoose>.replace({data:dict}, {new_data:dict}) -> Replace data from database
  # Return Type: List
  # Argument: data
    # Description: The data will find from database.
  # Argument: new_data
    # Description: The data will be replaced with found data.
  # Example(s):
    database.replace({
        "age": 25
    }, {
        "thing": True, 
        "age": 26
    }) # Now every data has 'age' and 'age' key value is 25, changed with new data.
    
# <Datagoose>.replace_one({data:dict}, {new_data:dict}) -> Replace one data from database
  # Return Type: Dict
  # Argument: data
    # Description: The data will find from database.
  # Argument: new_data
    # Description: The data will be replaced with found data.
  # Example(s):
    database.replace_one({
        "user_id": 2486718956
    }, {
        "banned": True,
        "ban_time": "30d",
        "user_id": 2486718956
    }) # Now only one data replaced.
```

<p style="font-size: 18px;">Note: The difference between update and replace, replace changes the entire data with new one. update only updates the key that given.</p>

# Deleting Data
```py
# <Datagoose>.delete({data:dict}) -> Delete data from database
  # Return Type: List
  # Argument: data
    # Description: The data will be deleted from database.
  # Example(s):
    database.delete({
        "total_hours": 1
    }) # Now datagoose deleted all data contains key 'total_hours' and key value is 1

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
# Quick example for using regex in datagoose.
# You must enable USE_REGEX option for using regex in datagoose.

for i in db.find({"ANSWER": r"yes|y"}):
    print(i)
```
# Load & Dump
```py
# <Datagoose>.dump({location:str}, [encoding:str:utf-8]) -> Dumps the database to JSON file.
  # Return Type: None
  # Argument: location
    # Description: The location that will dump.
  # Argument: encoding
    # Description: Encoding while write.
  # Example(s):
    database.dump("./dump.json")

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
# Collecting Garbage Data
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

# <Datagoose>.find_and_sort({data:dict}, {key:str}, [reverse:bool:False]) -> Find and sort database for key.
  # Return Type: List
  # Argument: data
    # Description: The data for find.
  # Argument: key
    # Description: The key for sort.
  # Argument: reverse
    # Description: Reverse the result.
  # Example(s):
    finished = database.find_and_sort({"finished": True}, "time", reverse=True)
    winner = finished[0]

    print(f"Congrats, {winner['name']}. You won the game!")
```

<p style="font-size: 18px;">Note: .sort_for_key() not changes the database, just returns sorted version of database.</p>

# Auto-Backup
```py
# <Datagoose>.start_backup([options:dict:{}]) -> Starts backup for every x second. Raises error when already started.
  # Return Type: None
  # Argument: options
    # Description: Options for auto-backup
  # Example(s):
    database.start_backup({
      "TIME": 60, # Second for repeat time. Minimum 30 second, Maximum 31,557,600 (1 year) second.
      "PATH": "database/backups", # Path for backup files.
      "ENCRYPTED": True # Encryption for database.
    })

# <Datagoose>.stop_backup() -> Stops backup loop. Will not effect if already stopped.
  # Return Type: Bool
  # Example(s):
    database.stop_backup()

# <Datagoose>.is_backup_open -> Returns backup status.
  # Return Type: Bool
  # Example(s):
    if not database.is_backup_open:
      print("Backup Disabled.")
```
# Using Events
```py
# You can use an event with .on(event_name, function).
# Example:

database.on("before_insert", lambda v: print("Starting to insert data: {0}".format(v)))
# Or:
def before_insert_function(value):
    # ...
    print("Starting to insert value: {0}".format(value))

database.on("before_insert", before_insert_function)
```
# Event List
All events and quick descriptions;
```py
{
  "before_insert": lambda value: None, # Runs before insert.
  "should_insert": lambda value: True, # Check method for should value insert.
  "after_insert": lambda value: None, # Runs after insert.

  "before_update": lambda now, changes: None, # Runs before update.
  "should_update": lambda now, changes: True, # Check method for should data update.
  "after_update": lambda now, old: None, # Runs after update.

  "before_replace": lambda now, new: None, # Runs before replace.
  "should_replace": lambda now, new: True, # Check method for should data replace.
  "after_replace": lambda now, old: None, # Runs after replace.

  "before_delete": lambda value: None, # Runs before delete.
  "should_delete": lambda value: True, # Check method for should data delete.
  "after_delete": lambda value: None, # Runs after delete.

  "before_copy": lambda value: None, # Runs before copy.
  "should_copy": lambda value: True, # Check method for should data copy.
  "after_copy": lambda value: None, # Runs after copy.

  "before_save": lambda: None, # Runs before save.
  "after_save": lambda: None, # Runs after save.

  "before_export": lambda: None, # Runs before using .dump() (export)
  "after_export": lambda: None, # Runs after using .dump() (export)

  "before_import": lambda: None, # Runs before using .load() (import)
  "after_import": lambda: None, # Runs after using .load() (import)

  "backup_start": lambda: None, # Runs when auto-backup starts.
  "backup": lambda: None, # Runs when backup data.
  "backup_finish": lambda: None, # Runs when auto-backup finish

  "before_garbage_clear": lambda: None, # Runs before garbage clear.
  "after_garbage_clear": lambda: None # Runs after garbage clear.
}
```