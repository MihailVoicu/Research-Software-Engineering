import pytest
from simplemaths.simplemaths import SimpleMaths as sm
import os
import yaml


with open(os.path.join(os.path.dirname(__file__),'fixtures.yml')) as fixtures_file:
    fixtures = yaml.load(fixtures_file)
	

def test_constructor(test='potato'):
    with pytest.raises(TypeError) as exception: sm(test)

@pytest.mark.parametrize("fixture", fixtures[0:3]) 
def test_square(fixture):
    answer = fixture['answer']
    inpt = fixture['input']
    assert sm(inpt).square() == answer