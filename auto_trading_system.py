import time
from stock_broker_driver import StockBrokerDriver
from kiwer_driver import KiwerDriver
from nemo_driver import NemoDriver

class AutoTradingSystem:
    PRICE_CHECK_COUNT = 3
    PRICE_CHECK_INTERVAL_SECONDS = 0.2

    def __init__(self):
        self._driver: StockBrokerDriver = None

    def select_stock_broker(self, broker: str) -> None:
        if broker == "kiwer":
            self._driver = KiwerDriver()
        elif broker == "nemo":
            self._driver = NemoDriver()
        else:
            ValueError(f"Unknown broker: {broker}")

    def login(self, id: str, password: str) -> None:
        self._driver.login(id, password)

    def buy(self, stock_code: str, price: int, count: int) -> None:
        self._driver.buy(stock_code, price, count)

    def sell(self, stock_code: str, price: int, count: int) -> None:
        self._driver.sell(stock_code, price, count)

    def get_price(self, stock_code: str) -> int:
        return self._driver.get_price(stock_code)

    def _get_prices(self, stock_code: str) -> list[int]:
        prices = []

        for index in range(self.PRICE_CHECK_COUNT):
            prices.append(self._driver.get_price(stock_code))

            if index < self.PRICE_CHECK_COUNT - 1:
                time.sleep(self.PRICE_CHECK_INTERVAL_SECONDS)

        return prices

    def _is_rising_trend(self, prices: list[int]) -> bool:
        return prices[0] < prices[1] < prices[2]

    def _calculate_buy_count(self, amount: int, price: int) -> int:
        return amount // price

    def buy_nice_timing(self, stock_code: str, amount: int) -> None:
        prices = self._get_prices(stock_code)

        if not self._is_rising_trend(prices):
            return

        buy_price = prices[-1]
        count = self._calculate_buy_count(amount, buy_price)

        if count <= 0:
            return

        self._driver.buy(stock_code, buy_price, count)

    def sell_nice_timing(self, stock_code: str, count: int) -> None:
        CHECK_COUNT = 3
        prices = []
        for i in range(CHECK_COUNT):
            prices.append(self._driver.get_price(stock_code))
            time.sleep(0.2)

        if self.check_nice_timing(prices):
            self._driver.sell(stock_code, prices[-1], count)

    def check_nice_timing(self, prices) -> bool:
        for i in range(len(prices)-1):
            if prices[i] <= prices[i + 1]:
                return False
        return True
