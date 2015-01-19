TSP MOOC Overview
=================

[![Build Status](https://travis-ci.org/pfe-asr-2014/tsp-mooc-overview.svg?branch=master)](https://travis-ci.org/pfe-asr-2014/tsp-mooc-overview)
[![Coverage Status](https://img.shields.io/coveralls/pfe-asr-2014/tsp-mooc-overview.svg)](https://coveralls.io/r/pfe-asr-2014/tsp-mooc-overview)
[![Code Health](https://landscape.io/github/pfe-asr-2014/tsp-mooc-overview/master/landscape.svg)](https://landscape.io/github/pfe-asr-2014/tsp-mooc-overview/master)

A service for the TSP MOOC platform right on your computer that let you acces, manage and overview all TMSP docker ready services.

## Run container

```sh
# With boot2docker
docker run -it -p 5000:5000 \
           -v /var/run/docker.sock:/var/run/docker.sock \
           --env HOST_IP=$(boot2docker-cli ip) \
           tsp-mooc-overview

# Without b2d
docker run -it -p 5000:5000 \
           -v /var/run/docker.sock:/var/run/docker.sock \
           tsp-mooc-overview
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
