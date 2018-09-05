class RestClient(object):

    def __init__(self, exchange_name, product_type, public_key, secret_key):
        self.exchange_name = exchange_name
        self.product_type = product_type
        self.public_key = public_key
        self.secret_key = secret_key

    async def get_order(self, coin_type, price, amount):
        pass

    async def get_orders(self):
        pass

    async def place_order(self):
        pass

    async def place_orders(self, exchange_name, ):
        pass

    async def cancel_order(self):
        pass

    async def check_account_balance(self):
        pass

    async def deposit(self):
        pass

    async def withdraw(self):
        pass
