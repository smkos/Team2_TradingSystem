import time
from typing import Any

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
        CHECK_COUNT = 3
        prices = []
        for i in range(CHECK_COUNT):
            prices.append(self._driver.get_price(stock_code))
            time.sleep(0.2)

        if self.check_nice_timing(prices):
            self._driver.sell(stock_code, prices[-1], count)

    def check_nice_timing(self, prices: list[Any]) -> bool:
        for i in range(len(prices)-1):
            if prices[i] <= prices[i + 1]:
                return False
        return True


