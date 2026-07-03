import pytest
from kiwer_driver import KiwerDriver
from nemo_driver import NemoDriver
from auto_trading_system import AutoTradingSystem

def test_select_kiwer_sets_driver():
    ats = AutoTradingSystem()
    ats.select_stock_broker("kiwer")
    assert isinstance(ats._driver, KiwerDriver)

def test_select_nemo_sets_driver():
    ats = AutoTradingSystem()
    ats.select_stock_broker("nemo")
    assert isinstance(ats._driver, NemoDriver)
