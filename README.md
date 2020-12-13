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

## Test

Run API tests:

```sh
$ python manage.py test
```

Navigate:

[http://localhost:8000](http://localhost:8000)

## Usage example

API can be used to publish demands from companies that need droids parts suppliers.

_For more examples and usage, please consult the [POSTMAN API collection][droids_demand_api.postman_collection.json]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Meta

Danilo Ribeiro – contatodanilors@gmail.com
