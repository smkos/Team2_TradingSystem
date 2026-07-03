from abc import ABC, abstractmethod

class StockBrokerDriver(ABC):

    @abstractmethod
    def login(self, id: str, password: str) -> None: ...

    @abstractmethod
    def buy(self, stock_code: str, price: int, count: int) -> None: ...

    @abstractmethod
    def sell(self, stock_code: str, price: int, count: int) -> None: ...

    @abstractmethod
    def get_price(self, stock_code: str) -> int: ...
