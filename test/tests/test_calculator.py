from calculator import add, subtract

def test_simple() -> None:
    print("test")

def test_add() -> None:
    a, b = 1, 1
    result = add(a, b)
    assert result == 2

def test_subtract() -> None:
    result = subtract(5, 3)
    assert result == 2
