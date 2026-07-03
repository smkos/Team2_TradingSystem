from nemo_api import NemoAPI
from stock_broker_driver import StockBrokerDriver

class NemoDriver(StockBrokerDriver):
    def __init__(self):
        self._api = NemoAPI()

    def login(self, id: str, password: str) -> None:
        raise NotImplementedError

    def buy(self, stock_code: str, price: int, count: int) -> None:
        self._api.purchasing_stock(stock_code, price, count)
        # 종목코드, 가격, 수량

    def sell(self, stock_code: str, price: int, count: int) -> None:
        self._api.selling_stock(stock_code, price, count)

    def get_price(self, stock_code: str) -> int:
        raise NotImplementedError
