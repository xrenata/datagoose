# Datagoose
Easy to use database for python

Quick Tour (example.py):
```py
from datagoose import Datagoose
import random

# create a new database
database = Datagoose("example")

# insert example
for i in range(100):
    database.insert({
        "name": random.choice(["eric", "kyle", "ike", "stan", "tweek"]),
        "lastname": random.choice(["cartman", "marsh"]),
        "age": random.randint(7, 12)
    })

# insert many example
database.insert_many({"user": "hi", "id": 1}, {"user": "ok", "id": 2})

# find example
print(database.find({"lastname": "marsh"})) # database.find() returns all data

# find one example
print(database.find_one({"name": "eric", "lastname": "cartman"}))

# update example
database.update({"name": "eric", "lastname": "cartman"}, {"name": "kyle", "new_data_example": "ok"})

# update one example
database.update_one({"name": "kyle"}, {"lastname": "only one change"})
print(database.find_one({"lastname": "only one change"}))

# delete example
database.delete({"age": 10})
print(database.find({"age": 10}))

# delete one example
print(database.delete_one({"name": "eric"}))

# count example
print(database.count({"name": "ike"}))
print(database.count({"name": "tweek"}))
print(database.count({"name": "stan"}))

# database info
print(database.info())

# beautify database
database.beautify() # database.minify() for reverse

# reset the database (danger zone!)
database.reset()
```
