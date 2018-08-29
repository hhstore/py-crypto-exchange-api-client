# sdk config:
class Config:
    # api key:
    exchange_api_key = {
        "bitmex": {
            "public_key": "",
            "secret_key": "",
            "permission": "",
        }
    }

    # api list:
    exchange_api_endpoints = {
        "bitmex": {
            "rest": {
                "public": [],
                "auth": [],
            },
            "websocket": {
                "public": [],
                "auth": [],
            },
        },
        "bitfinex": {

        },
        "okex": {

        },
        "houbi": {

        },

    }
