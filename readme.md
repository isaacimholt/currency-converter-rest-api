# currency-converter-rest-api

Simple rest api for converting currency.

## Getting Started

These instructions will cover usage information and for the docker container 

### Prerequisites

In order to run this container you'll need docker installed.

* [Windows](https://docs.docker.com/windows/started)
* [OS X](https://docs.docker.com/mac/started/)
* [Linux](https://docs.docker.com/linux/started/)

### Usage

#### Run

```shell
docker-compose -f docker-compose.yml up
```

#### Dev

```shell
docker-compose -f docker-compose.dev.yml up
```

#### Test

```shell
docker-compose -f docker-compose.test.yml up
```

## Built With

* flask 1.*
* flask-restful 0.*
* requests 2.*
* redis 2.*
* pytest 3.*

## Public Repo

* [GitHub](https://github.com/isaacimholt/currency-converter-rest-api)