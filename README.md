TSP MOOC Overview
=================

[![Build Status](https://travis-ci.org/pfe-asr-2014/tsp-mooc-overview.svg?branch=master)](https://travis-ci.org/pfe-asr-2014/tsp-mooc-overview)
[![Coverage Status](https://img.shields.io/coveralls/pfe-asr-2014/tsp-mooc-overview.svg)](https://coveralls.io/r/pfe-asr-2014/tsp-mooc-overview)

A service for the TSP MOOC platform right on your computer that let you acces, manage and overview all TMSP docker ready services.

## Run container

```sh
# With boot2docker
docker run -it --env HOST_IP=$(ip route|awk '/192/ { print $9 }') debian bash

# Without b2d
docker run -it debian bash
```

## Tests

```sh
# Running tests
fig run app nosetests

# With coverage
fig run app nosetests --with-coverage --cover-html --cover-package=overview

```

## Acknowledgement

* tests containers are based on [rockymeza/django-docker-example](https://github.com/rockymeza/django-docker-example).
