from kiwer_api import KiwerAPI
from stock_broker_driver import StockBrokerDriver

class KiwerDriver(StockBrokerDriver):
    def __init__(self):
        self._api = KiwerAPI()

    def login(self, id: str, password: str) -> None:
        raise NotImplementedError

    def buy(self, stock_code: str, price: int, count: int) -> None:
        self._api.buy(stock_code, count, price)
        # 종목코드, 수량, 가격

    def sell(self, stock_code: str, price: int, count: int) -> None:
        self._api.sell(stock_code, count, price)

    def get_price(self, stock_code: str) -> int:
        return self._api.current_price(stock_code)
