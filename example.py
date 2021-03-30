from datagoose import Datagoose

# create a new database
database = Datagoose("example")

# insert example
database.insert("example", {
    "data": {
        "number": 1,
        "string": "hey!",
        "float": 5.1
    },
    "array": ["h", "e", "l", "l", "o"]
})

database.insert("another", {
    "data": {
        "number": 1,
        "string": "hey!",
        "float": 5.1
    },
    "array": ["h", "e", "l", "l", "o"]
})

# remove data example
database.remove("another")

# ?=> for go to a data
print(database.find("example?=>data?=>number")) # you can close ?=> with short=False.

# update a data from database
database.update({
    "example": {
        "data": {
            "number": 10,
            "string": [1, 2, 3]
        },
        "array": {
            "ok": 200
        },
        "new": "hi!"
    }
}) # note: if you add overwrite=True, it will delete the old data and paste the new one.

# beautify the database
database.beautify()
# database.minify() = minify the database

# read database
print(database.read())

# database info
print(database.info())

# kb size
print(database.info().get("database").get("size") >> 10)

# clear
database.clear()