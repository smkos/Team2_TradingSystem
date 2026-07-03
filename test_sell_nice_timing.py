import pytest
from unittest.mock import patch

def test_sell_nice_timing_downtrend_sells(trading_system, mock_driver):
    # 1200 → 1100 → 1000 : 단조 감소 → 매도 실행
    mock_driver.get_price.side_effect = [1200, 1100, 1000]
    with patch('auto_trading_system.time.sleep'):
        trading_system.sell_nice_timing("005930", 5)
    mock_driver.sell.assert_called_once_with("005930", 1000, 5)

def test_sell_nice_timing_no_downtrend_no_sell(trading_system, mock_driver):
    # 1000 → 1100 → 1200 : 상승 추세 → 매도 안 함
    mock_driver.get_price.side_effect = [1000, 1100, 1200]
    with patch('auto_trading_system.time.sleep'):
        trading_system.sell_nice_timing("005930", 5)
    mock_driver.sell.assert_not_called()

def test_sell_nice_timing_flat_no_sell(trading_system, mock_driver):
    # 1000 → 1000 → 1000 : 횡보 → 매도 안 함
    mock_driver.get_price.side_effect = [1000, 1000, 1000]
    with patch('auto_trading_system.time.sleep'):
        trading_system.sell_nice_timing("005930", 5)
    mock_driver.sell.assert_not_called()

def test_sell_nice_timing_sleep_called(trading_system, mock_driver):
    mock_driver.get_price.side_effect = [1200, 1100, 1000]
    with patch('auto_trading_system.time.sleep') as mock_sleep:
        trading_system.sell_nice_timing("005930", 5)
    assert mock_sleep.call_count == 3
    mock_sleep.assert_called_with(0.2)

@pytest.mark.integration
def test_sell_nice_timing_kiwer(kiwer_system):
    kiwer_system.sell_nice_timing("005930", 5)

@pytest.mark.integration
def test_sell_nice_timing_nemo(nemo_system):
    nemo_system.sell_nice_timing("005930", 5)
