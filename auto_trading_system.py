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
        pass

    def get_price(self, stock_code: str) -> int:
        pass

    def buy_nice_timing(self, stock_code: str, amount: int) -> None:
        raise NotImplementedError

    def sell_nice_timing(self, stock_code: str, count: int) -> None:
        prices = []
        for _ in range(3):
            prices.append(self._driver.get_price(stock_code))
            time.sleep(0.2)

        check_sell = True
        for i in range(2):
            if prices[i] <= prices[i+1]:
                check_sell = False

        if check_sell:
            self._driver.sell(stock_code, prices[-1], count)


