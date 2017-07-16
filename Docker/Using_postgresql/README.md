# Using Postgresql with Docker :-)

Hello everyone, this will be a nice and quick hands on tutorial on basic SQLian
operations and the wonderfullness of Docker.

The only thing you need to get this thing going (and anything else) is to have
docker installed in your machine -> [installing Docker](https://docs.docker.com/engine/installation/).

# Getting started
[Let's get it started](https://www.youtube.com/watch?v=IKqV7DB8Iwg#t=08s)..

## Getting the code
Open up a terminal and...
```
git clone https://github.com/Data4Democracy/tutorials
cd tutorials/Docker/Using_postgresql
```

The above commands will place you in the postgres + docker world we are going
to need.

## Gettting a PostgreSQL DB running
Now, do
```
docker-compose up --build -d && docker-compose ps
```

you will see we have two containers running: `postgresql` + `app`.
[postgresql](https://hub.docker.com/_/postgres/) is the official docker image
and app is the thing that is being defined in our `Dockerfile`.


## Connecting to Postgres
In your terminal type:
```
docker exec -it app bash
```

This will take you to a bash shell [INSIDE your docker container!](https://tinyurl.com/yb8aqrkp)

Finally type
```
ipython
```

### Using sqlalchemy
Here is where you can deviate and try this awesome [tutorial](https://www.compose.com/articles/using-json-extensions-in-postgresql-from-python-2/)
or go along with this other example (go through both!):

```
Python 3.6.1 |Continuum Analytics, Inc.| (default, May 11 2017, 13:09:58) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.1.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import json                                                                     
   ...: import sqlalchemy                                                               
   ...: from sqlalchemy.sql import select                                               
   ...: from sqlalchemy import Column, Text                                             
   ...:                                                                                 
   ...:                                                                                 
   ...: connection_string = 'postgresql://user:pass@postgresql/mydatabase'              
   ...:                                                                                 
   ...: db = sqlalchemy.create_engine(connection_string)                                
   ...: engine = db.connect()                                                           
   ...: meta = sqlalchemy.MetaData(engine)                                              
   ...: meta.reflect(bind=engine)  
   ...: 

In [2]: # list all tables                                                               
   ...: # there shouldn't be any... yet!                                                
   ...: meta.tables 
Out[2]: immutabledict({})

In [3]: # create table                                                                  
   ...: table = sqlalchemy.Table("twitterusers",                                        
   ...:                          meta,                                                  
   ...:                          Column('screen_name', Text, primary_key=True),         
   ...:                          Column('last_scraped', Text),                          
   ...:                          extend_existing=True)                                  
   ...: table.create(engine)       
   ...:                          

In [4]: # some sample data to be stored                                                 
   ...: entries = [                                                                     
   ...:     {'screen_name': 'katie', 'last_scraped': 'today'},                          
   ...:     {'screen_name': 'hunter', 'last_scraped': 'yesterday'},                     
   ...:     {'screen_name': 'felix', 'last_scraped': 'last week'},                      
   ...:     {'screen_name': 'audie', 'last_scraped': 'last year'},                      
   ...: ]  

In [5]: # Insert data                                                                   
   ...: record = sqlalchemy.table("twitterusers",                                       
   ...:                           Column('screen_name', Text),                           
   ...:                           Column('last_scraped', Text))                         
   ...: for entry in entries:                                                           
   ...:     statement = record.insert().values(                                         
   ...:         screen_name = entry['screen_name'],                                     
   ...:         last_scraped = entry['last_scraped'],                                   
   ...:     )                                                                           
   ...:     engine.execute(statement) 
   ...:     

In [6]: # Look up data                                                                  
   ...: table = meta.tables['twitterusers']                                             
   ...: res = engine.execute(select([table.c.screen_name, table.c.last_scraped]))       
   ...: rows = res.fetchall()  
   ...: 

In [7]: rows
Out[7]: 
[('katie', 'today'),
 ('hunter', 'yesterday'),
 ('felix', 'last week'),
 ('audie', 'last year')]

In [8]: # Updating entries                                                              
   ...: t = table.update().values(last_scraped='this century').where(table.c.screen_name=='hunter')
   ...: engine.execute(t)  
   ...: 

Out[8]: <sqlalchemy.engine.result.ResultProxy at 0x7f0be063a898>

In [9]: # Look up data                                                                  
   ...: table = meta.tables['twitterusers']                                             
   ...: res = engine.execute(select([table.c.screen_name, table.c.last_scraped]))       
   ...: rows = res.fetchall()
   ...: rows
   ...: 

Out[9]: 
[('katie', 'today'),
 ('felix', 'last week'),
 ('audie', 'last year'),
 ('hunter', 'this century')]

```
