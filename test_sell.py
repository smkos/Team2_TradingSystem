import pytest

def test_sell_mock_calls_driver(trading_system, mock_driver):
    trading_system.sell("005930", 70000, 10)
    mock_driver.sell.assert_called_once_with("005930", 70000, 10)

def test_sell_mock_price_before_count(trading_system, mock_driver):
    trading_system.sell("005930", 70000, 3)
    args = mock_driver.sell.call_args[0]
    assert args[1] == 70000  # price가 두 번째 인자
    assert args[2] == 3      # count가 세 번째 인자

@pytest.mark.integration
def test_sell_kiwer(kiwer_system):
    kiwer_system.sell("005930", 70000, 10)

@pytest.mark.integration
def test_sell_nemo(nemo_system):
    nemo_system.sell("005930", 70000, 10)
