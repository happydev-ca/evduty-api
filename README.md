[![Build, test and publish](https://github.com/happydev-ca/evduty-api/actions/workflows/publish.yml/badge.svg)](https://github.com/happydev-ca/evduty-api/actions/workflows/publish.yml)

# evduty-api

Library to communicate with EVduty REST API.

## Usage

```python
import aiohttp
import asyncio
import os

from evdutyapi import EVDutyApi


async def run():
    async with aiohttp.ClientSession() as session:
        api = EVDutyApi(os.environ['EMAIL'], os.environ['PASSWORD'], session)
        stations = await api.async_get_stations()
        print(stations)


asyncio.run(run())
```

### Build and test locally

```shell
make venv
source .venv/bin/activate
make test
make build
```

### Logging

Enable debug level to log API requests and responses.
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Release version

```shell
make release bump=patch|minor|major
```