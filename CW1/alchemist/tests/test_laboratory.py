import yaml, os, pytest

from collections import Counter
from pytest import raises, approx
from ..laboratory import Laboratory
from ..laboratory import Substance

'''
Testing the Pyalchemist package

Description: use some tests for Merlin's laboratory simulation. These include:
1. Tests of run_full_experiment(): obvious cases, empty shelves, negative tests
2. Tests of update_shelves(): obvious update cases, updates of substances at start/end of list
3. Tests of the Substance class and can_react() method
4. Tests of do_a_reaction(): random updates of shelves

The fixtures.yaml file contains setups of many labs indexed in the following way:
1. X labs from positions 0:5 in the fixtures.yaml file to test for obvious cases
2. Y labs from positions 6:10 in the fixtures.yaml file to test for...
'''	


''' Check a list is a permutation of another list: used to check that 
answer = lab solution due to the random selection of substances in do_a_reaction()'''
def is_permutation(s1, s2):
    return Counter(s1) == Counter(s2)	

''' Import fixtures from fixtures.yaml within \alchemist\tests '''
with open(os.path.join(os.path.dirname(__file__), 'fixtures.yaml')) as fixtures_file:				   
    fixtures = yaml.load(fixtures_file)   


	
''' 1.1. run_full_experiment() sanity tests, empty shelves, no reactions take place '''
@pytest.mark.parametrize("fixture", fixtures[0:8])
def test_run_full_exp(fixture):
    answer = fixture.pop('answer')
    assert is_permutation(str(Laboratory(fixture).run_full_experiment()), answer)

''' 1.2. Laboratory negative tests on inputs: one missing shelf, wrong datatype,
wrong number of shelves (TypeError is raised)'''
@pytest.mark.parametrize("fixture", fixtures[8:14])
def negat_test_run_full_exp(fixture):
    with raises(TypeError) as exception: Laboratory(fixture)


	
''' 2. update_shelves() sanity tests, negative test '''
def test_update_shelves():

    ''' given the lab below '''
    input ={'lower':['A', 'antiB', 'C', 'X', 'X', 'X', 'X'],
            'upper':['antiA', 'antiC', 'antiA', 'Giorgio', 'antiX', 'antiA']}
    lab = Laboratory(input)
	
    ''' test shelves update with substance in the middle (index 2 in upper) '''
    lab.update_shelves('A', 2)
    assert lab.shelf1 == ['antiB', 'C', 'X', 'X', 'X', 'X']
    assert lab.shelf2 == ['antiA', 'antiC', 'Giorgio', 'antiX', 'antiA']
	
    ''' test shelves update even though substances cannot react, for a given index
	This is fine here since update_shelves runs given can_react() is successful! '''
    lab.update_shelves('antiB', 2)
    assert lab.shelf1 == ['C', 'X', 'X', 'X', 'X']
    assert lab.shelf2 == ['antiA', 'antiC', 'antiX', 'antiA']
	
    ''' test shelves update with substance in corner (end of list) '''
    lab.update_shelves('X', 2)
    assert lab.shelf1 == ['C', 'X', 'X', 'X']
    assert lab.shelf2 == ['antiA', 'antiC', 'antiA']
    
    ''' negative test: shelves fail to update with upper shelf substance if outside of range (throw ValueError) '''
    with raises(ValueError) as Exception: lab.update_shelves('C', 5)	

	
	
''' 3.1. can_react() sanity tests, antiantianti... substances '''
@pytest.mark.parametrize("fixture", fixtures[14:19])
def test_Substance_class(fixture):
    assert Substance(fixture['subst1'], fixture['subst2']).can_react() == True
	
''' 3.2. can_react() different reactions: 'sub' instead of 'anti' '''
@pytest.mark.parametrize("fixture", fixtures[19:21])
def test_Substance_class(fixture):
    reaction = "sub"
    assert Substance(fixture['subst1'], fixture['subst2'], reaction_type = reaction).can_react() == True
	
''' 3.3. can_react() negative tests: wrong format of substance, no substance,  '''
@pytest.mark.parametrize("fixture", fixtures[21:25])
def negative_test_Substance_class(fixture):
	with raises(TypeError) as Exception: Substance(fixture['subst1'], fixture['subst2'])

	
	
''' 4. do_a_reaction() test: substances from upper shelf selected with equal probability'''	
@pytest.mark.parametrize("fixture", fixtures[25:])	
def test_equal_prob_do_a_reaction(fixture):

    ''' For the lab tested here, substance A from lower shelf can react with 3
		antiA substances form the upper shelf. antiA substances are at the start,
		end and middle positions on the upper shelf (also tests corner cases)
		
		Test over 10,000 trials that probas are unbiased (close to uniform)
		
		Note: only the 1st substance that can react from the lower shelf is used to
		test the upper shelf since all other lower shelf substances that can react
		will react in the same way
	'''
	
    original_upper = fixture['upper']
    trials = 10000
    probas = [0] * len(original_upper)
	
    for i in range(trials):
		
        lab = Laboratory(fixture)
        lab.do_a_reaction()
        updated_upper = lab.shelf2
        
        j = 0
        while True:
            updated_copy = updated_upper.copy()
            updated_copy.insert(j, 'antiA')
            j += 1
            if updated_copy == original_upper:
                break
		  
        probas[j-1] += 1

    probas = [count / trials for count in probas]
    count_nonzero = [i for i, x in enumerate(probas) if x != 0.]
    final_probas = [probas[i] for i in count_nonzero]
    unbiased_probas = [1/len(final_probas)] * len(final_probas)
    # test probab of selecting substance is unbiased ()
    assert final_probas == approx(unbiased_probas, 0.1)

