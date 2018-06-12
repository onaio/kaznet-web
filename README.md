# Kaznet Web

[![Build Status](http://cicd.onalabs.org/api/badges/onaio/kaznet-web/status.svg)](http://cicd.onalabs.org/onaio/kaznet-web)

Kaznet web is a Django project that provides the core functionality and APIs for the ILRI Kaznet project.

Kaznet web supports only **Python versions >=3.6** and **Django versions >= 2.0**

Kaznet is primarily a tasking application built on top of [Ona](http://ona.io).

**Table of Contents**

* [Design guidelines](https://github.com/onaio/kaznet-web/blob/master/docs/design.md)
* [Installation](https://github.com/onaio/kaznet-web/blob/master/docs/installation.md)
* [Architecture](https://github.com/onaio/kaznet-web/blob/master/docs/architecture.md)
* [Ona Tasking Application](https://github.com/onaio/tasking)
* [ILRI Kaznet Project](https://github.com/onaio/kaznet-web/blob/master/docs/project.md)
* [Testing](https://github.com/onaio/kaznet-web#testing)

## Contributing

Contributions are welcome.

1. Clone the repo
2. ```pipenv install --dev```
3. ```cp kaznet.settings.local_settings.example.py kaznet.settings.local_settings.py```
4. Modify `kaznet.settings.local_settings.py` to match your local environment

## Testing

```sh

pip install -U tox

tox

```
