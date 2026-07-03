import pytest
from unittest.mock import MagicMock
from stock_broker_driver import StockBrokerDriver
from auto_trading_system import AutoTradingSystem

@pytest.fixture
def mock_driver():
    return MagicMock(spec=StockBrokerDriver)

@pytest.fixture
def trading_system(mock_driver):
    ats = AutoTradingSystem()
    ats._driver = mock_driver
    return ats

@pytest.fixture
def kiwer_system():
    ats = AutoTradingSystem()
    ats.select_stock_broker("kiwer")
    return ats

@pytest.fixture
def nemo_system():
    ats = AutoTradingSystem()
    ats.select_stock_broker("nemo")
    return ats
