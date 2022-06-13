kartoza
=======

Portfolio App


Requirements:
-------------

- [python 3.10.3](https://python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [postgresql](https://www.postgresql.org/download/)
- [Geospatial libraries](https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/geolibs/)


Getting Started
---------------

1. Clone the repo:

```
$ git clone https://github.com/g1039/kartoza.git
$ cd kartoza
```

2. Setup the virtualenv

```
$ virtualenv ve
$ source ve/bin/activate
```

3. Install requirements:

```
$ make install
```

4. Setup database

Config your database

```
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```
and then run the following command:

```
$ make migrate
$ make createsuperuser
```

5. Run tests

```
$ make test
```

6. Start the application

```
$ make run
```
