# AutoTradingSystem 설계 문서

**날짜:** 2026-07-03  
**작성자:** 팀장  

---

## 1. 개요

GitHub 팀 협업 기반의 자동 주식 매매 시스템.  
팀장이 유닛 테스트를 먼저 작성해 배포하고, 팀원들이 구현 후 PR을 제출하면 팀장이 코드 리뷰 후 main에 머지한다.

---

## 2. 아키텍처

```
AutoTradingSystem
    │
    └── StockBrokerDriver (interface)
            ├── KiwerDriver  →  KiwerAPI
            └── NemoDriver   →  NemoAPI
```

- **StockBrokerDriver**: 증권사 API 명세 차이를 추상화하는 인터페이스
- **KiwerDriver / NemoDriver**: 인터페이스를 구현하며 각 API의 메서드명/파라미터 순서를 내부에서 정규화
- **AutoTradingSystem**: 비즈니스 로직 담당. 드라이버를 주입받아 사용

---

## 3. 프로젝트 구조 (플랫 구조)

```
team_project/
├── stock_broker_driver.py      # 인터페이스 (팀장 작성)
├── kiwer_driver.py             # 시그니처만 (팀원 구현)
├── nemo_driver.py              # 시그니처만 (팀원 구현)
├── auto_trading_system.py      # 시그니처만 (팀원 구현)
├── kiwer_api.py                # 기존 파일 (수정 불가)
├── nemo_api.py                 # 기존 파일 (수정 불가)
├── conftest.py                 # 공통 픽스처 (팀장 작성)
├── test_login.py               # 팀장
├── test_buy_nice_timing.py     # 팀원 1
├── test_sell_nice_timing.py    # 팀원 2
├── test_buy.py                 # 팀원 3
├── test_sell.py                # 팀원 3
├── test_select_broker.py       # 팀원 4
└── test_get_price.py           # 팀원 4
```

---

## 4. 인터페이스 설계

### StockBrokerDriver

```python
# stock_broker_driver.py
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
```

**파라미터 정규화 기준:**
- `buy` / `sell`: `(stock_code, price, count)` 순서 — price 먼저
- KiwerAPI는 `(stock_code, count, price)` 순서이므로 KiwerDriver 내부에서 순서를 맞춰줌
- NemoAPI의 `get_market_price(stock_code, minute)`는 `minute=1` 기본값으로 처리

### AutoTradingSystem 시그니처

```python
# auto_trading_system.py
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
        raise NotImplementedError

    def get_price(self, stock_code: str) -> int:
        raise NotImplementedError

    def buy_nice_timing(self, stock_code: str, amount: int) -> None:
        raise NotImplementedError

    def sell_nice_timing(self, stock_code: str, count: int) -> None:
        raise NotImplementedError
```

---

## 5. 핵심 기능 명세

### buy_nice_timing(stock_code, amount)
1. `get_price()`를 200ms 간격으로 3회 호출
2. `prices[0] < prices[1] < prices[2]` 이면 상승 추세로 판단
3. `count = amount // prices[2]` 로 최대 수량 계산
4. `buy(stock_code, prices[2], count)` 호출
5. 추세 미충족 시 아무 행동도 하지 않음

### sell_nice_timing(stock_code, count)
1. `get_price()`를 200ms 간격으로 3회 호출
2. `prices[0] > prices[1] > prices[2]` 이면 하락 추세로 판단
3. `sell(stock_code, prices[2], count)` 호출
4. 추세 미충족 시 아무 행동도 하지 않음

---

## 6. 테스트 전략

### 공통 원칙
- **Mock 먼저**: 드라이버 없이 Mock으로 ATS 로직 검증
- **실제 드라이버**: KiwerDriver, NemoDriver 각각 연결하여 동작 확인
- **conftest.py**: 팀장이 공통 픽스처를 미리 작성해 배포

### conftest.py

```python
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
```

### buy_nice_timing / sell_nice_timing 테스트 주의사항
- `time.sleep`을 `mock.patch('auto_trading_system.time.sleep')`으로 반드시 패치
- `get_price` side_effect로 상승/하락/횡보 시나리오를 각각 테스트

---

## 7. 팀원 업무 배분

| 담당자 | 담당 기능 | 테스트 파일 수 | 작성할 테스트 수 | 드라이버 구현 |
|--------|-----------|---------------|----------------|--------------|
| 팀원 1 | `buy_nice_timing` | 1개 | Mock 2~3개 + Kiwer 1개 + Nemo 1개 | 없음 |
| 팀원 2 | `sell_nice_timing` | 1개 | Mock 2~3개 + Kiwer 1개 + Nemo 1개 | 없음 |
| 팀원 3 | `buy` + `sell` | 2개 | 기능당 Mock 2개 + Kiwer 1개 + Nemo 1개 | `KiwerDriver.buy/sell`, `NemoDriver.buy/sell` |
| 팀원 4 | `select_stock_broker` + `login` + `get_price` | 3개 | 기능당 Mock 1~2개 + Kiwer 1개 + Nemo 1개 | `KiwerDriver.login/get_price`, `NemoDriver.login/get_price` |

**팀장 역할:** `stock_broker_driver.py`, `auto_trading_system.py` 시그니처, `conftest.py`, 각 `test_*.py` 스켈레톤 작성 → 코드 리뷰 및 main 머지

---

## 8. 개발 순서 (팀원 기준)

1. `stock_broker_driver.py` (인터페이스) 확인
2. `conftest.py` 픽스처 확인
3. 담당 `test_*.py` 파일 구현 (Mock 테스트 먼저)
4. `auto_trading_system.py` 해당 기능 구현
5. `kiwer_driver.py` / `nemo_driver.py` 해당 기능 구현
6. 실제 드라이버 테스트 통과 확인
7. PR 제출
