import pytest


@pytest.mark.math
def test_one_plus_one():
    assert 1+1==2
    
    
@pytest.mark.math
def test_one_plus_two():
    a=1
    b=2
    c=3
    assert a+b==c

@pytest.mark.math
def test_exception():
    with pytest.raises(ZeroDivisionError) as e:
        num=1/0
    assert 'division by zero' in str(e.value)
    