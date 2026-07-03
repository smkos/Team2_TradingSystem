from nemo_api import NemoAPI
from stock_broker_driver import StockBrokerDriver

class NemoDriver(StockBrokerDriver):
    def __init__(self):
        self._api = NemoAPI()

    def login(self, id: str, password: str) -> None:
        raise NotImplementedError

    def buy(self, stock_code: str, price: int, count: int) -> None:
        raise NotImplementedError

    def sell(self, stock_code: str, price: int, count: int) -> None:
        raise NotImplementedError

    def get_price(self, stock_code: str) -> int:
        raise NotImplementedError
