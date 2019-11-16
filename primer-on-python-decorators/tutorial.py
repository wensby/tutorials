# Setup

def section(title):
  print(f'\n{title}\n')

section('# Primer on Python Decorators')

section('## Function')

def add_one(number):
  return number + 1

print(add_one(2))

section('### First-Class Objects')

def say_hello(name):
  return f'Hello {name}'

def be_awesome(name):
  return f'Yo {name}, together we are the awesomest!'

def greet_bob(greeter_func):
  return greeter_func('Bob')

print(greet_bob(say_hello))
print(greet_bob(be_awesome))

section('### Inner Functions')

def parent():
  print('Printing from the parent() function')

  def first_child():
    print('Printing from the first_child() function')

  def second_child():
    print('Printing from the second_child() function')

  second_child()
  first_child()

parent()

try:
  first_child()
except Exception as e:
  print(e)

section('### Returning Functions From Functions')

def parent(num):
  def first_child():
    return 'Hi, I am Emma'

  def second_child():
    return 'Call me Liam'

  if num == 1:
    return first_child
  else:
    return second_child

first = parent(1)
second = parent(2)

print(first)
print(second)

print(first())
print(second())

section('## Simple Decorators')

def my_decorator(func):
  def wrapper():
    print('Something is happening before the function is called.')
    func()
    print('Something is happening after the function is called.')
  return wrapper

def say_whee():
  print('Whee!')

say_whee = my_decorator(say_whee)

say_whee()

print(say_whee)

from datetime import datetime

def not_during_the_night(func):
  def wrapper():
    if 7 <= datetime.now().hour < 22:
      func()
    else:
      pass # Hush, the neighbors are asleep
  return wrapper

def say_whee():
  print('Whee!')

say_whee = not_during_the_night(say_whee)

say_whee()

section('### Syntactic Sugar!')

def my_decorator(func):
  def wrapper():
    print('Something is happening before the function is called.')
    func()
    print('Something is happening after the function is called.')
  return wrapper

@my_decorator
def say_whee():
  print('Whee!')

section('### Reusing Decorators')

from decorators import do_twice

@do_twice
def say_whee():
  print('Whee!')

say_whee()

section('### Decorating Functions With Arguments')

from decorators import do_twice

@do_twice
def greet(name):
  print(f'Hello {name}')

try:
  greet('World')
except Exception as e:
  print(e)

from decorators import do_twice2 as do_twice

@do_twice
def say_whee():
  print('Whee!')

@do_twice
def greet(name):
  print(f'Hello {name}')

say_whee()
greet('World')

section('### Returning Values From Decorated Functions')

from decorators import do_twice2 as do_twice

@do_twice
def return_greeting(name):
  print('Creating greeting')
  return f'Hi {name}'

hi_adam = return_greeting('Adam')
print(hi_adam)

from decorators import do_twice3 as do_twice

@do_twice
def return_greeting(name):
  print('Creating greeting')
  return f'Hi {name}'

print(return_greeting('Adam'))

section('### Who Are You, Really?')

print(print)
print(print.__name__)
# help(print)

print(say_whee)
print(say_whee.__name__)
# help(say_whee)

from decorators import do_twice4 as do_twice

@do_twice
def say_whee():
  print('Whee!')

@do_twice
def greet(name):
  print(f'Hello {name}')

print(say_whee)
print(say_whee.__name__)
# help(say_whee)

section('## A Few Real World Examples')

import functools

def decorator(func):
  @functools.wraps(func)
  def wrapper_decorator(*args, **kwargs):
    # Do something before
    value = func(*args, **kwargs)
    # Do something after
    return value
  return wrapper_decorator

section('### Timing Functions')

from decorators import timer

@timer
def waste_some_time(num_times):
  for _ in range(num_times):
    sum([i**2 for i in range(10000)])

waste_some_time(1)
waste_some_time(999)

section('### Debugging Code')

from decorators import debug

@debug
def make_greeting(name, age=None):
  if age is None:
    return f'Howdy {name}!'
  else:
    return f'Whoa {name}! {age} already, you are growing up!'

make_greeting('Benjamin')
make_greeting('Richard', age=112)
make_greeting(name='Dorrisile', age=116)

import math
from decorators import debug

math.factorial = debug(math.factorial)

def approximate_e(terms=18):
  return sum(1 / math.factorial(n) for n in range(terms))

print(approximate_e(5))

section('### Slowing Down Code')

from decorators import slow_down

@slow_down
def countdown(from_number):
  if from_number < 1:
    print('Liftoff!')
  else:
    print(from_number)
    countdown(from_number - 1)

countdown(3)

section('### Registering Plugins')

import random
PLUGINS = dict()

def register(func):
  """Register a function as a plug-in"""
  PLUGINS[func.__name__] = func
  return func

@register
def say_hello(name):
  return f'Hello {name}'

@register
def be_awesome(name):
  return f'Yo {name}, together we are the awesomest!'

def randomly_greet(name):
  greeter, greeter_func = random.choice(list(PLUGINS.items()))
  print(f'Using {greeter!r}')
  return greeter_func(name)

print(PLUGINS)
print(randomly_greet('Alice'))

print(globals())

section('### Is the User Logged In?')

section('## Fancy Decorators')

section('### Decorating Classes')

class Circle:
  def __init__(self, radius):
    self._radius = radius

  @property
  def radius(self):
    """Get value of radius"""
    return self._radius

  @radius.setter
  def radius(self, value):
    """Set radius, raise error if negative"""
    if value >= 0:
      self._radius = value
    else:
      raise ValueError('Radius must be positive')

  @property
  def area(self):
    """Calculate area inside circle"""
    return self.pi() * self.radius**2

  def cylinder_volume(self, height):
    """Calculate volume of cylinder with circle as base"""
    return self.area * height

  @classmethod
  def unit_circle(cls):
    """Factory method creating a circle with radius 1"""
    return cls(1)

  @staticmethod
  def pi():
    """Value of π, could use math.pi instead though"""
    return 3.1415926535

c = Circle(5)
print(c.radius)

print(c.area)

c.radius = 2
print(c.area)

try:
  c.area = 100
except Exception as e:
  print(e)

print(c.cylinder_volume(height=4))

try:
  c.radius = -1
except Exception as e:
  print(e)

c = Circle.unit_circle()
print(c.radius)

print(c.pi())

print(Circle.pi())

from decorators import debug, timer

class TimeWaster:
  @debug
  def __init__(self, max_num):
    self.max_num = max_num

  @timer
  def waste_time(self, num_times):
    for _ in range(num_times):
      sum([i**2 for i in range(self.max_num)])

tw = TimeWaster(1000)
tw.waste_time(999)

from dataclasses import dataclass

@dataclass
class PlayingCard:
  rank: str
  suit: str

@timer
class TimeWaster:
  def __init__(self, max_num):
    self.max_num = max_num

  def waste_time(self, num_times):
    for _ in range(num_times):
      sum([i**2 for i in range(self.max_num)])

tw = TimeWaster(1000)
tw.waste_time(999)

section('### Nesting Decorators')

@debug
@do_twice
def greet(name):
  print(f'Hello {name}')

greet('Eva')

@do_twice
@debug
def greet(name):
  print(f'Hello {name}')

greet('Eva')

section('### Decorators With Arguments')

from decorators import repeat

@repeat(num_times=4)
def greet(name):
  print(f'Hello {name}')

greet('World')

section('### Both Please, But Never Mind the Bread')

from decorators import repeat2 as repeat

@repeat
def say_whee():
  print('Whee!')

@repeat(num_times=3)
def greet(name):
  print(f'Hello {name}')

say_whee()
greet('Penny')

section('### Stateful Decorators')

from decorators import count_calls

@count_calls
def say_whee():
  print('Whee!')

say_whee()
say_whee()

section('### Classes as Decorators')

class Counter:
  def __init__(self, start=0):
    self.count = start

  def __call__(self):
    self.count += 1
    print(f'Current count is {self.count}')

counter = Counter()
counter()
counter()
print(counter.count)

from decorators import CountCalls

@CountCalls
def say_whee():
  print('Whee!')

say_whee()
say_whee()
print(say_whee.num_calls)

section('## More Real World Examples')

section('### Slowing Down Code, Revisited')

from decorators import slow_down2 as slow_down

@slow_down(rate=2)
def countdown(from_number):
  if from_number < 1:
    print('Liftoff!')
  else:
    print(from_number)
    countdown(from_number - 1)

countdown(3)

section('### Creating Singletons')

from decorators import singleton

@singleton
class TheOne:
  pass

first_one = TheOne()
another_one = TheOne()

print(id(first_one))
print(id(another_one))
print(first_one is another_one)

section('### Caching Return Values')

@count_calls
def fibonacci(num):
  if num < 2:
    return num
  return fibonacci(num - 1) + fibonacci(num - 2)

print(fibonacci(10))
print(fibonacci.num_calls)

from decorators import cache

@cache
@count_calls
def fibonacci(num):
  if num < 2:
    return num
  return fibonacci(num - 1) + fibonacci(num - 2)

print(fibonacci(10))
print(fibonacci(8))

@functools.lru_cache(maxsize=4)
def fibonacci(num):
  print(f'Calculating fibonacci({num})')
  if num < 2:
    return num
  return fibonacci(num - 1) + fibonacci(num - 2)

print(fibonacci(10))
print(fibonacci(8))
print(fibonacci(5))
print(fibonacci(8))
print(fibonacci.cache_info())

section('### Adding Information About Units')

from decorators import set_unit

@set_unit('cm^3')
def volume(radius, height):
  return math.pi * radius**2 * height

print(volume(3, 5))
print(volume.unit)

import pint
ureg = pint.UnitRegistry()
vol = volume(3, 5) * ureg(volume.unit)

print(vol)
print(vol.to('cubic inches'))
print(vol.to('gallons').m)

from decorators import use_unit

@use_unit('meters per second')
def average_speed(distance, duration):
  return distance / duration

bolt = average_speed(100, 9.58)
print(repr(bolt))
print(repr(bolt.to('km per hour')))
print(repr(bolt.to('mph').m))

section('### Validating JSON')

section('## Conclusion')

section('## Further Reading')
