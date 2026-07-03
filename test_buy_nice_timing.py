import pytest
from unittest.mock import patch

def test_buy_nice_timing_uptrend_buys(trading_system, mock_driver):
    # 1000 → 1100 → 1200 : 단조 증가 → 매수 실행
    mock_driver.get_price.side_effect = [1000, 1100, 1200]
    with patch('auto_trading_system.time.sleep'):
        trading_system.buy_nice_timing("005930", 10000)
    # 10000 // 1200 = 8
    mock_driver.buy.assert_called_once_with("005930", 1200, 8)

def test_buy_nice_timing_no_uptrend_no_buy(trading_system, mock_driver):
    # 1200 → 1100 → 1000 : 하락 추세 → 매수 안 함
    mock_driver.get_price.side_effect = [1200, 1100, 1000]
    with patch('auto_trading_system.time.sleep'):
        trading_system.buy_nice_timing("005930", 10000)
    mock_driver.buy.assert_not_called()

def test_buy_nice_timing_flat_no_buy(trading_system, mock_driver):
    # 1000 → 1000 → 1000 : 횡보 → 매수 안 함
    mock_driver.get_price.side_effect = [1000, 1000, 1000]
    with patch('auto_trading_system.time.sleep'):
        trading_system.buy_nice_timing("005930", 10000)
    mock_driver.buy.assert_not_called()

def test_buy_nice_timing_sleep_called(trading_system, mock_driver):
    mock_driver.get_price.side_effect = [1000, 1100, 1200]
    with patch('auto_trading_system.time.sleep') as mock_sleep:
        trading_system.buy_nice_timing("005930", 10000)
    assert mock_sleep.call_count == 2
    mock_sleep.assert_called_with(0.2)

'''
@pytest.mark.integration
def test_buy_nice_timing_kiwer(kiwer_system):
    kiwer_system.buy_nice_timing("005930", 100000)

@pytest.mark.integration
def test_buy_nice_timing_nemo(nemo_system):
    nemo_system.buy_nice_timing("005930", 100000)
'''