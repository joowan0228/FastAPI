from datetime import datetime
from delivery import get_eta

def test_get_eta_2023_12_01():
    result = get_eta(datetime(2023, 12, 1))
    assert result == datetime(2023, 12, 4)
