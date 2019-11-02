# Tutorial Setup

def print_heading(heading):
  print(f'\n === {heading} ===\n')

# Tutorial
print_heading('Version Check')

import sqlalchemy

print(sqlalchemy.__version__)


print_heading('Connecting')

from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)


print_heading('Declare a Mapping')

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import Column, Integer, String

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  fullname = Column(String)
  nickname = Column(String)

  def __repr__(self):
    return "<User(name='%s', fullname='%s', nickname='%s')>" % (
        self.name, self.fullname, self.nickname)


print_heading('Create a Schema')

print(repr(User.__table__))
Base.metadata.create_all(engine)


print_heading('Create an Instance of the Mapped Class')

ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
print(ed_user.name)
print(ed_user.nickname)
print(ed_user.id)


print_heading('Creating a Session')

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
# Session = sessionmaker()
# Session.configure(bind=engine) # once engine is available

session = Session()


print_heading('Adding and Updating Objects')

ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)
our_user = session.query(User).filter_by(name='ed').first()
print(str(our_user))
print(ed_user is our_user)
session.add_all([
  User(name='wendy', fullname='Wendy Williams', nickname='windy'),
  User(name='mary', fullname='Mary Contrary', nickname='mary'),
  User(name='fred', fullname='Fred Flintstone', nickname='freddy')])
ed_user.nickname = 'eddie'
print(session.dirty)
print(session.new)
session.commit()
print(ed_user.id)


print_heading('Rolling Back')

ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid', nickname='12345')
session.add(fake_user)
print(session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all())
session.rollback()
print(ed_user.name)
print(fake_user in session)
print(session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all())


print_heading('Querying')

for instance in session.query(User).order_by(User.id):
  print(instance.name, instance.fullname)
for name, fullname in session.query(User.name, User.fullname):
  print(name, fullname)
for row in session.query(User, User.name).all():
  print(row.User, row.name)
for row in session.query(User.name.label('name_label')).all():
  print(row.name_label)

from sqlalchemy.orm import aliased

user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all():
  print(row.user_alias)
for u in session.query(User).order_by(User.id)[1:3]:
  print(u)
for name, in session.query(User.name).\
    filter_by(fullname='Ed Jones'):
  print(name)
for name, in session.query(User.name).\
    filter(User.fullname=='Ed Jones'):
  print(name)
for user in session.query(User).\
    filter(User.name=='ed').\
    filter(User.fullname=='Ed Jones'):
  print(user)


print_heading('Common Filter Operators')


print_heading('Returning Lists and Scalaras')

query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
print(query.all())
print(query.first())
try:
  user = query.one()
except Exception as e:
  print(e)
try:
  user = query.filter(User.id == 99).one()
except Exception as e:
  print(e)
query = session.query(User.id).filter(User.name == 'ed').\
    order_by(User.id)
print(query.scalar())


print_heading('Using Textual SQL')

from sqlalchemy import text

for user in session.query(User).\
    filter(text('id<224')).\
    order_by(text('id')).all():
  print(user.name)
print(session.query(User).filter(text('id<:value and name=:name')).\
    params(value=224, name='fred').order_by(User.id).one())
print(session.query(User).from_statement(
    text('SELECT * FROM users WHERE name=:name')).\
    params(name='ed').all())
stmt = text('SELECT name, id, fullname, nickname '
    'FROM users WHERE name=:name')
stmt = stmt.columns(User.name, User.id, User.fullname, User.nickname)
print(session.query(User).from_statement(stmt).params(name='ed').all())
stmt = text('SELECT name, id FROM users WHERE name=:name')
stmt = stmt.columns(User.name, User.id)
print(session.query(User.id, User.name).\
    from_statement(stmt).params(name='ed').all())


print_heading('Counting')

print(session.query(User).filter(User.name.like('%ed')).count())

from sqlalchemy import func

print(session.query(func.count(User.name), User.name).group_by(User.name).all())
print(session.query(func.count('*')).select_from(User).scalar())
print(session.query(func.count(User.id)).scalar())


print_heading('Building a Relationship')

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
  __tablename__ = 'addresses'
  id = Column(Integer, primary_key=True)
  email_address = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))

  user = relationship('User', back_populates='addresses')

  def __repr__(self):
    return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship(
    'Address', order_by=Address.id, back_populates='user')
Base.metadata.create_all(engine)


print_heading('Working with Related Objects')

jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
print(jack.addresses)
jack.addresses = [
    Address(email_address='jack@google.com'),
    Address(email_address='j25@yahoo.com')]
print(jack.addresses[1])
print(jack.addresses[1].user)
session.add(jack)
session.commit()
jack = session.query(User).\
    filter_by(name='jack').one()
print(jack)
print(jack.addresses)


print_heading('Querying with Joins')

for u, a in session.query(User, Address).\
    filter(User.id==Address.user_id).\
    filter(Address.email_address=='jack@google.com').\
    all():
  print(u)
  print(a)
print(session.query(User).join(Address).\
    filter(Address.email_address=='jack@google.com').\
    all())


print_heading('Using Aliases')

from sqlalchemy.orm import aliased

adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in \
    session.query(User.name, adalias1.email_address, adalias2.email_address).\
    join(adalias1, User.addresses).\
    join(adalias1, User.addresses).\
    filter(adalias1.email_address=='jack@google.com').\
    filter(adalias2.email_address=='j25@yahoo.com'):
  print(username, email1, email2)


print_heading('Using subqueries')

from sqlalchemy.sql import func

stmt = session.query(Address.user_id, func.count('*').\
    label('address_count')).\
    group_by(Address.user_id).subquery()
for u, count in session.query(User, stmt.c.address_count).\
    outerjoin(stmt, User.id==stmt.c.user_id).order_by(User.id):
  print(u, count)


print_heading('Selecting Entities from Subqueries')

stmt = session.query(Address).\
    filter(Address.email_address != 'j25@yahoo.com').\
    subquery()
adalias = aliased(Address, stmt)
for user, address in session.query(User, adalias).\
    join(adalias, User.addresses):
  print(user)
  print(address)


print_heading('Using EXISTS')

from sqlalchemy.sql import exists

stmt = exists().where(Address.user_id==User.id)
for name, in session.query(User.name).filter(stmt):
  print(name)
for name, in session.query(User.name).\
    filter(User.addresses.any()):
  print(name)
for name, in session.query(User.name).\
    filter(User.addresses.any(Address.email_address.like('%google%'))):
  print(name)
print(session.query(Address).\
    filter(~Address.user.has(User.name=='jack')).all())


print_heading('Common Relationship Operators')


print_heading('Eager Loading')


print_heading('Selecting Load')

from sqlalchemy.orm import selectinload

jack = session.query(User).\
    options(selectinload(User.addresses)).\
    filter_by(name='jack').one()
print(jack)
print(jack.addresses)


print_heading('Joined Load')

from sqlalchemy.orm import joinedload

jack = session.query(User).\
    options(joinedload(User.addresses)).\
    filter_by(name='jack').one()
print(jack)
print(jack.addresses)


print_heading('Explicit Join + Eagerload')

from sqlalchemy.orm import contains_eager
jacks_addresses = session.query(Address).\
    join(Address.user).\
    filter(User.name=='jack').\
    options(contains_eager(Address.user)).\
    all()
print(jacks_addresses)
print(jacks_addresses[0].user)


print_heading('Deleting')

session.delete(jack)
print(session.query(User).filter_by(name='jack').count())
print(session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
  ).count())


print_heading('Configuring delete/delete-orphan Cascade')

session.close()
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  fullname = Column(String)
  nickname = Column(String)

  addresses = relationship('Address', back_populates='user',
      cascade='all, delete, delete-orphan')

  def __repr__(self):
    return "<User(name='%s', fullname='%s', nickname='%s')>" % (
        self.name, self.fullname, self.nickname)

class Address(Base):
  __tablename__ = 'addresses'
  id = Column(Integer, primary_key=True)
  email_address = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship('User', back_populates='addresses')

  def __repr__(self):
    return "<Address(email_address='%s')>" % self.email_address

jack = session.query(User).get(5)
del jack.addresses[1]
print(session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
  ).count())
session.delete(jack)
print(session.query(User).filter_by(name='jack').count())
print(session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
  ).count())


print_heading('Building a Many to Many Relationship')

from sqlalchemy import Table, Text
# accociative table
post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
  )

class BlogPost(Base):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id'))
  headline = Column(String(255), nullable=False)
  body = Column(Text)

  # many to many BlogPost<->Keyword
  keywords = relationship('Keyword',
      secondary=post_keywords,
      back_populates='posts')

  def __init__(self, headline, body, author):
    self.author = author
    self.headline = headline
    self.body = body

  def __repr__(self):
    return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)

class Keyword(Base):
  __tablename__ = 'keywords'

  id = Column(Integer, primary_key=True)
  keyword = Column(String(50), nullable=False, unique=True)
  posts = relationship('BlogPost',
      secondary=post_keywords,
      back_populates='keywords')

  def __init__(self, keyword):
    self.keyword = keyword

BlogPost.author = relationship(User, back_populates='posts')
User.posts = relationship(BlogPost, back_populates='author', lazy='dynamic')
Base.metadata.create_all(engine)
wendy = session.query(User).\
    filter_by(name='wendy').\
    one()
post = BlogPost("Wendy's Blog Post", 'This is a test', wendy)
session.add(post)
post.keywords.append(Keyword('wendy'))
post.keywords.append(Keyword('firstpost'))
print(session.query(BlogPost).\
    filter(BlogPost.keywords.any(keyword='firstpost')).\
    all())
print(session.query(BlogPost).\
    filter(BlogPost.author==wendy).\
    filter(BlogPost.keywords.any(keyword='firstpost')).\
    all())
print(wendy.posts.\
    filter(BlogPost.keywords.any(keyword='firstpost')).\
    all())
