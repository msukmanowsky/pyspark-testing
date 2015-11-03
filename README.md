Testing with PySpark is a pain, so let's make it a little easier by example.

[![Build Status](https://travis-ci.org/msukmanowsky/pyspark-testing.svg?branch=master)](https://travis-ci.org/msukmanowsky/pyspark-testing)

This project serves as an example of some good practices to follow when
developing and testing PySpark applications/driver scripts.

## Tip 1: Use Python packages

Spark requires that any code your driver needs to be on the `PYTHONPATH` of
the executors which launch `python` processes. This means that either every
node in the cluster needs to be properly provisioned with all the required
dependencies, or that code your driver needs is sent to executors via
`spark-submit --py-files /path/to/myegg.egg` or `sc.addPyFile()`.

For requirements that do not change often, doing a global `pip install ...` on
all nodes as part of provisioning/bootstrapping is fine, but for proprietary
code that changes frequently, a better solution is needed.

To do this, you have one of two chocies:

1. Manually create a regular zip file, and ship it via `--py-files` or
   `addPyFile()`
2. Build an egg (`python setup.py bdist_egg`) or source distribution
   `python setup.py sdist`

Building a regular zip file is fine, albeit a little more tedious than being
able to run:

```bash
python setup.py clean bdist_egg
```

Of course the other benefit from creating a package is that you can benefit
from sharing your code if you've created something that's pip installable.

## Tip 2: Try to avoid lambdas

By design, Spark requires a functional programming approach to driver scripts.
Python functions are pickled, sent across the network and executed on remote
servers when tranformation methods like `map`, `filter` or `reduce` are called.

It's tempting to write the bulk of functions as:

```python
data = (sc.textFile('/path/to/data')
        .map(lambda d: d.split(','))
        .map(lambda d: d[0].upper())
        .filter(lambda d: d == 'THING'))
```

Anonymous lambda's like these are quick and easy, but suffer from two big
problems:

1. They aren't unit testable
2. They aren't self-documenting

Instead, we could rewrite the code above like so:

```python
def parse_line(line):
    parts = line.split(',')
    return parts[0].upper()

def is_valid_thing(thing):
    return thing == 'THING'

data = (sc.textFile('/path/to/data')
        .map(parse_line)
        .filter(is_valid_thing))
```

More verbose, sure, but `parse_line` and `is_valid_thing` are now easily unit
testable and arguably, self-documenting.

## Tip 3: Abstract your data with models

The code above is good, but it's still pretty annoying that we have to deal with
strings that are split and then remember the array index of fields we want to
work with.

To improve on this, we could create a model that encapsulates the data
structures we're playing with.

```python
class Person(object):

    __slots__ = ('first_name', 'last_name', 'birth_date')

    def __init__(first_name, last_name, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    @classmethod
    def from_csv_line(cls, line):
        parts = line.split(',')
        if len(parts) != 3:
            raise Exception('Bad line')

        return cls(*parts)
```

Now we can play with a class who's attributes are known:

```python
def is_valid_person(person):
    return person.first_name is not None and person.last_name is not None


data = (sc.textFile('/path/to/data')
        .map(Person.from_csv_line)
        .filter(is_valid_person))
```

Astute Pythonistas will question why I didn't use a `namedtuple` and instead
resorted to an object using `__slots__`. The answer is performance. In some
testing we've done internally, allocating lots of slot-based objects is both
faster and more memory efficient than using anything like `namedtuple`s.

Given that you'll often allocate millions if not billions of these objects,
speed and memory are important to keep in mind.


## Tip 4: Use test-ready closures for database connections

When working with external databases, give yourself the ability to send a mock
connection object to facilitate tests later on:

```python
def enrich_data(db_conn=None):
    def _enrich_data(partition):
        db_conn = db_conn or create_db_conn()
        for datum in partition:
            # do something with db_conn like join additional data
            enriched_datum = do_stuff(datum, db_conn)
            yield enriched_datum
    return _enrich_data

my_rdd.mapPartitions(enrich_data())
```

By creating a closure like this, we can still independently test `enrich_data`
by passing in a `MagicMock` for our `db_conn` instance.

## Tip 4: Use some `unittest` magic for integration tests

How does one create an integration test that relies on Spark running? This repo
serves as a perfect example! Check out:

- [the integration test harness](https://github.com/msukmanowsky/pyspark-testing/blob/master/tests/pyspark_testing/integration/__init__.py)
- [the sample integration tests](https://github.com/msukmanowsky/pyspark-testing/blob/master/tests/pyspark_testing/integration/test_driver.py)
- [the Travis CI config](https://github.com/msukmanowsky/pyspark-testing/blob/master/.travis.yml)

## Notes on the data set used in this project

The data set used in this project is the
[National Broadband Data Set](http://open.canada.ca/data/en/dataset/00a331db-121b-445d-b119-35dbbe3eedd9)
which is provided thanks to the Government of Canada's Open Government
initiative.
