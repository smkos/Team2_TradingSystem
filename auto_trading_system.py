import time
from stock_broker_driver import StockBrokerDriver

class AutoTradingSystem:
    def __init__(self):
        self._driver: StockBrokerDriver = None

    def select_stock_broker(self, broker: str) -> None:
        raise NotImplementedError

    def login(self, id: str, password: str) -> None:
        raise NotImplementedError

    def buy(self, stock_code: str, price: int, count: int) -> None:
        raise NotImplementedError

    def sell(self, stock_code: str, price: int, count: int) -> None:
        raise NotImplementedError

    def get_price(self, stock_code: str) -> int:
        raise NotImplementedError

    def buy_nice_timing(self, stock_code: str, amount: int) -> None:
        raise NotImplementedError

    def sell_nice_timing(self, stock_code: str, count: int) -> None:
        raise NotImplementedError
