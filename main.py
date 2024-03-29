# Copyright 2021 Group 21 @ PI (120)


import uvicorn

from api.core import api
from api.config.configs import get_api_config


def main():
    uvicorn.run(api, host=get_api_config().host, port=get_api_config().port)


if __name__ == '__main__':
    main()
