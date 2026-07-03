import pytest

def test_login_mock(trading_system, mock_driver):
    trading_system.login("myid", "mypass")
    mock_driver.login.assert_called_once_with("myid", "mypass")

@pytest.mark.integration
def test_login_kiwer(kiwer_system):
    kiwer_system.login("myid", "mypass")

@pytest.mark.integration
def test_login_nemo(nemo_system):
    nemo_system.login("myid", "mypass")
