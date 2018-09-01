# sdk config:
class Config:
    # api key:
    exchange_api_key = {
        "bitmex": {
            "public_key": "",
            "secret_key": "",
            "permission": "",
        },
        "okex": {
            "public_key": "3b773537-bbae-4db9-9a9b-42069d7e1fbb",
            "secret_key": "EFAABB4F616059E45557329A86D2B77C",
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
            "rest": {
                "public": [],
                "auth": [],
            },
            "websocket": {}
        },
        "houbi": {

        },

    }
