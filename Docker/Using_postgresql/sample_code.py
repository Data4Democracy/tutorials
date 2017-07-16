import json
import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy import Column, Text


connection_string = 'postgresql://user:pass@postgresql/mydatabase'

db = sqlalchemy.create_engine(connection_string)  
engine = db.connect() 
meta = sqlalchemy.MetaData(engine)
meta.reflect(bind=engine)

# list all tables
# there shouldn't be any... yet!
meta.tables


# create table
table = sqlalchemy.Table("twitterusers", 
                         meta,  
                         Column('screen_name', Text, primary_key=True),
                         Column('last_scraped', Text),
                         extend_existing=True)
table.create(engine)

# some sample data to be stored
entries = [
    {'screen_name': 'katie', 'last_scraped': 'today'},
    {'screen_name': 'hunter', 'last_scraped': 'yesterday'},
    {'screen_name': 'felix', 'last_scraped': 'last week'},
    {'screen_name': 'audie', 'last_scraped': 'last year'},
]

# Insert data
record = sqlalchemy.table("twitterusers", 
                          Column('screen_name', Text),
                          Column('last_scraped', Text))
for entry in entries:
    statement = record.insert().values(
        screen_name = entry['screen_name'],
        last_scraped = entry['last_scraped'],
    )
    engine.execute(statement)

# Updating entries
t = table.update().values(last_scraped='guajiro').where(table.c.screen_name=='hunter')
engine.execute(t)

#find_user = table.select().where(table.c.screen_name=='hunter')


# Look up data
table = meta.tables['twitterusers']
res = engine.execute(select([table.c.screen_name, table.c.last_scraped]))
rows = res.fetchall()
