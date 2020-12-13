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

_For more examples and usage, please refer to the [API Manual][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Meta

Danilo Ribeiro – contatodanilors@gmail.com

Distributed under the XYZ license. See `LICENSE` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->

[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
