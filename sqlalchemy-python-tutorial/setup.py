import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Census(Base):
  __tablename__ = 'census'
  id = Column(Integer, primary_key=True)
  state = Column(String(30))
  sex = Column(String(1))
  age = Column(Integer)
  pop2000 = Column(Integer)
  pop2008 = Column(Integer)

class StateFact(Base):
  __tablename__ = 'state_fact'
  id = Column(Integer, primary_key=True)
  name = Column(String(30))
  abbreviation  = Column(String(10))
  country = Column(String)
  type = Column(String)
  occupied = Column(String)
  notes = Column(String)
  fips_state = Column(Integer)
  assoc_press = Column(String)
  standard_federal_region = Column(String)
  census_region = Column(Integer)
  census_region_name = Column(String)
  census_division = Column(Integer)
  census_division_name = Column(String)
  circuit_court = Column(Integer)

def run():
  if os.path.exists('census.sqlite'):
    os.remove('census.sqlite')
  if os.path.exists('test.sqlite'):
    os.remove('test.sqlite')
  engine = create_engine('sqlite:///census.sqlite')
  Base.metadata.create_all(engine)
  Session = sessionmaker(bind=engine)
  session = Session()
  session.add(Census(state='California', sex='M', age=0, pop2000=33226, pop2008=23456))
  session.add(Census(state='California', sex='F', age=0, pop2000=78357, pop2008=23456))
  session.add(Census(state='Texas', sex='F', age=0, pop2000=78357, pop2008=23456))
  session.add(Census(state='New York', sex='F', age=0, pop2000=78358, pop2008=23456))
  session.add(Census(state='Illinois', sex='F', age=0, pop2000=78358, pop2008=23456))
  session.add(Census(state='Illinois', sex='M', age=0, pop2000=89600, pop2008=89600))
  session.add(Census(state='Illinois', sex='M', age=1, pop2000=88445, pop2008=91829))
  session.add(Census(state='Illinois', sex='M', age=2, pop2000=88729, pop2008=89547))
  session.add(StateFact(
    name='Illinois', 
    abbreviation='IL',
    country='USA',
    type='state',
    occupied='occupied',
    fips_state=17,
    assoc_press='Ill.',
    standard_federal_region='V',
    census_region=2,
    census_region_name='Midwest',
    census_division=3,
    census_division_name='East North Central',
    circuit_court=7
  ))

  session.commit()
  session.close()
