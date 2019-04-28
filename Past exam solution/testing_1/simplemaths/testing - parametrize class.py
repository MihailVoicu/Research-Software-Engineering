import pytest
from pytest import raises
from simplemaths.simplemaths import SimpleMaths as sm

class TestSimpleMaths():
    
    @pytest.mark.parametrize('input', [5, 10, 500])
    def testInitPos(self, input):
        TestInit = sm(input)

    @pytest.mark.parametrize('input', [5.0, '5', None])
    def testInitNeg(self, input):
        with raises(TypeError):
            TestInit = sm(input)
    
    @pytest.mark.parametrize('input, output', [(5, 25), (4, 16), (-3, 9)])
    def testSquare(self, input, output):
        TestSquare = sm(input)
        assert TestSquare.square() == output
        