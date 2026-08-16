from accum import Accumulator
import pytest

@pytest.mark.accumulator
def test_acc_initial():
    accum=Accumulator()
    assert accum.count==0

@pytest.mark.accumulator 
def test_acc_add_one():
    accum=Accumulator()
    accum.add()
    assert accum.count==1

@pytest.mark.accumulator 
def test_acc_add_three():
    accum=Accumulator()
    accum.add(3)
    assert accum.count==3

@pytest.mark.accumulator
def test_acc_add_twice():
    accum=Accumulator()
    accum.add()
    accum.add()
    assert accum.count==2

@pytest.mark.accumulator    
def test_acc_update():
    accum=Accumulator()
    with pytest.raises(AttributeError,match=r"property 'count' of 'Accumulator' object has no setter") as e:
     accum.count=10