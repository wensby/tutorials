# Setup the database which the tutorial expects and some helper functions

import setup
setup.run()

def printelems(elems):
  for elem in elems:
    print(elem)

def printsection(title, depth):
  print(f"\n{'#'*depth} {title}\n")

printsection('Viewing Table Details', 1)

import sqlalchemy as db

engine = db.create_engine('sqlite:///census.sqlite')
connection = engine.connect()
metadata = db.MetaData()
census = db.Table('census', metadata, autoload=True, autoload_with=engine)
print(census.columns.keys())
print(repr(metadata.tables['census']))

printsection('Querying', 1)

query = db.select([census])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
printelems(ResultSet[:3])

printsection('where', 2)

printelems(connection.execute(db.select([census]).where(census.columns.sex == 'F')).fetchall())

printsection('in', 2)

printelems(connection.execute(db.select([census]).where(census.columns.state.in_(['Texas', 'New York']))).fetchall())

printsection('and, or, not', 2)

printelems(connection.execute(db.select([census]).where(db.and_(census.columns.state == 'California', census.columns.sex != 'M'))).fetchall())

printsection('order by', 2)

printelems(connection.execute(db.select([census]).order_by(db.desc(census.columns.state), census.columns.pop2000)).fetchall())

printsection('functions', 2)

printelems(connection.execute(db.select([db.func.sum(census.columns.pop2008)])).fetchall())

printsection('group by', 2)

printelems(connection.execute(db.select([db.func.sum(census.columns.pop2008).label('pop2008'), census.columns.sex]).group_by(census.columns.sex)).fetchall())

printsection('distinct', 2)

printelems(connection.execute(db.select([census.columns.state.distinct()])).fetchall())

printsection('case & cast', 2)

female_pop = db.func.sum(db.case([(census.columns.sex == 'F', census.columns.pop2000)], else_=0))
total_pop = db.cast(db.func.sum(census.columns.pop2000), db.Float)
query = db.select([female_pop/total_pop * 100])
result = connection.execute(query).scalar()
print(result)

printsection('joins', 2)

import pandas as pd
state_fact = db.Table('state_fact', metadata, autoload=True, autoload_with=engine)

printsection('Automatic Join', 3)

query = db.select([census.columns.pop2008, state_fact.columns.abbreviation])
result = connection.execute(query).fetchall()
df = pd.DataFrame(result)
df.columns = result[0].keys()
df.head(5)
print(df)

printsection('Manual Join', 3)

query = db.select([census, state_fact])
query = query.select_from(census.join(state_fact, census.columns.state == state_fact.columns.name))
results = connection.execute(query).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
df.head(5)
print(df)

printsection('Creating and Inserting Data into Tables', 1)

printsection('Creating Database and Table', 2)

engine = db.create_engine('sqlite:///test.sqlite')
connection = engine.connect()
metadata = db.MetaData()

emp = db.Table('emp', metadata,
              db.Column('Id', db.Integer()),
              db.Column('name', db.String(255), nullable=False),
              db.Column('salary', db.Float(), default=100.0),
              db.Column('active', db.Boolean(), default=True)
              )
metadata.create_all(engine)

printsection('Inserting Data', 2)

query = db.insert(emp).values(Id=1, name='naveen', salary=60000.00, active=True)
ResultProxy = connection.execute(query)

query = db.insert(emp)
values_list = [{'Id':'2', 'name':'ram', 'salary':80000, 'active':False},
               {'Id':'3', 'name':'ramesh', 'salary':70000, 'active':True}]
ResultProxy = connection.execute(query,values_list)

results = connection.execute(db.select([emp])).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
df.head(4)
print(df)

printsection('Updating data in Databases', 1)

engine = db.create_engine('sqlite:///test.sqlite')
metadata = db.MetaData()
connection = engine.connect()
emp = db.Table('emp', metadata, autoload=True, autoload_with=engine)
results = connection.execute(db.select([emp])).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
df.head(4)
print(df)
query = db.update(emp).values(salary = 100000)
query = query.where(emp.columns.Id == 1)
results = connection.execute(query)
results = connection.execute(db.select([emp])).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
df.head(4)
print(df)

printsection('Delete Table', 1)

engine = db.create_engine('sqlite:///test.sqlite')
metadata = db.MetaData()
connection = engine.connect()
emp = db.Table('emp', metadata, autoload=True, autoload_with=engine)
results = connection.execute(db.select([emp])).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
df.head(4)
print(df)
query = db.delete(emp)
query = query.where(emp.columns.salary < 100000)
results = connection.execute(query)
results = connection.execute(db.select([emp])).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
df.head(4)
print(df)
