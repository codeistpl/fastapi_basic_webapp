from mongoengine.connection import connect

connection = connect(
    "test", host="mongodb://root:example@localhost:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
