import pytest

def test_get_price_mock_returns_driver_value(trading_system, mock_driver):
    mock_driver.get_price.return_value = 75000
    result = trading_system.get_price("005930")
    assert result == 75000
    mock_driver.get_price.assert_called_once_with("005930")

@pytest.mark.integration
def test_get_price_kiwer(kiwer_system):
    price = kiwer_system.get_price("005930")
    assert isinstance(price, int)

@pytest.mark.integration
def test_get_price_nemo(nemo_system):
    price = nemo_system.get_price("005930")
    assert isinstance(price, int)
