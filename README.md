# Droids Demand API

Rest API that makes it possible to publish quotations for specific pieces of droids.

![](header.png)

## Dependencies

- Django v3.1.4
- Docker v19.03.8
- Python v3.8.3

## Installation

OS X & Linux:

Build the image:

```sh
$ cd droids_demand_api
$ docker-compose build
$ docker-compose up -d
```

## Usage example

Navigate:

[http://localhost:8000](http://localhost:8000)

API can be used to publish demands from companies that need droids parts suppliers.

_For more examples and usage, please consult the [POSTMAN API collection](https://github.com/danribeiro/droids_demand_api/blob/master/droids_demand_api.postman_collection.json)._

## Test

Run API tests:

```sh
$ python manage.py test
```

## Meta

Danilo Ribeiro – contatodanilors@gmail.com
