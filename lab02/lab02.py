from unittest import TestCase
import random
import urllib.request

ROMEO_SOLILOQUY = """
        But, soft! what light through yonder window breaks?
        It is the east, and Juliet is the sun.
        Arise, fair sun, and kill the envious moon,
        who is already sick and pale with grief,
        That thou her maid art far more fair than she:
        be not her maid, since she is envious;
        her vestal livery is but sick and green
        and none but fools do wear it; cast it off.
        It is my lady, O, it is my love!
        O, that she knew she were!
        She speaks yet she says nothing: what of that?
        Her eye discourses; I will answer it.
        I am too bold, 'tis not to me she speaks:
        two of the fairest stars in all the heaven,
        having some business, do entreat her eyes
        to twinkle in their spheres till they return.
        What if her eyes were there, they in her head?
        The brightness of her cheek would shame those stars,
        as daylight doth a lamp; her eyes in heaven
        would through the airy region stream so bright
        that birds would sing and think it were not night.
        See, how she leans her cheek upon her hand!
        O, that I were a glove upon that hand,
        that I might touch that cheek!"""

toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]


################################################################################
# EXERCISE 1
################################################################################
# Implement this function
def compute_ngrams(toks, n=2):
    """Returns an n-gram dictionary based on the provided list of tokens."""
    n_gram = dict()
    for i in range(len(toks)-n+1): #go through all tokens, excluding last n-1
        
        #make tuple of next n
        temp = tuple(toks[i+1:i+n])

        #add tuple to dict list
        if toks[i] not in n_gram:
            temp_list = [temp]
            n_gram[toks[i]] = temp_list
        else:
            n_gram[toks[i]].append(temp)
    
    return n_gram

def test1():
    test1_1()
    test1_2()
    print('passed test1')

# 20 Points
def test1_1():
    """A smaller test case for your ngram function."""
    tc = TestCase()
    simple_toks = [t.lower() for t in 'I really really like cake.'.split()]

    compute_ngrams(simple_toks)
    tc.assertEqual(compute_ngrams(simple_toks),
                   {'i': [('really',)], 'like': [('cake.',)], 'really': [('really',), ('like',)]})
    tc.assertEqual(compute_ngrams(simple_toks, n=3),
                   {'i': [('really', 'really')],
                    'really': [('really', 'like'), ('like', 'cake.')]})

    romeo_toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]

    dct = compute_ngrams(romeo_toks, n=4)
    tc.assertEqual(dct['but'], [('sick', 'and', 'green'), ('fools', 'do', 'wear')])
    tc.assertEqual(dct['it'],
                   [('is', 'the', 'east,'),
                    ('off.', 'it', 'is'),
                    ('is', 'my', 'lady,'),
                    ('is', 'my', 'love!'),
                    ('were', 'not', 'night.')])

# 30 Points
def test1_2():
    """Test your code on Peter Pan."""
    PETER_PAN_URL = 'https://moss.cs.iit.edu/cs331/data/peterpan.txt'
    peter_pan_text = urllib.request.urlopen(PETER_PAN_URL).read().decode()
    tc = TestCase()
    pp_toks = [t.lower() for t in peter_pan_text.split()]
    dct = compute_ngrams(pp_toks, n=3)
    tc.assertEqual(dct['crocodile'],
                   [('passes,', 'but'),
                    ('that', 'happened'),
                    ('would', 'have'),
                    ('was', 'in'),
                    ('passed', 'him,'),
                    ('is', 'about'),
                    ('climbing', 'it.'),
                    ('that', 'was'),
                    ('pass', 'by'),
                    ('and', 'let'),
                    ('was', 'among'),
                    ('was', 'waiting')])
    tc.assertEqual(len(dct['wendy']), 202)
    tc.assertEqual(len(dct['peter']), 243)

################################################################################
# EXERCISE 2
################################################################################
# Implement this function


def gen_passage(ngram_dict, length=100):
    dict_keys = sorted(ngram_dict.keys())   #dict_keys = sorted list of ngram_dictionary keys
    ans = list()                            #create list for tokens in my generated passage
    start = random.choice(dict_keys)        #randomly pick key from dict_keys to start the passage
    while len(ans) < length:                 #keep the passage at the given length
        ans.append(start)                   #add the current start key to the passage
        current = ngram_dict.get(start)     #get the list of tuples at the current start key
        temp1 = random.choice(current)      #randomly pick tuple from list of tuples at start key. THIS RANDOM CHOICE DOESN'T PICK ANYTHING EXCEPT "really" from the list it's passed.

        ans.extend(temp1)                   #append elements in randomly selected tuple (temp1) to ans
        
        start = temp1[-1]                   #new start is the last element
        if start not in ngram_dict:         #if new start is NOT a key in the dictionary:
            start = random.choice(dict_keys)#make other random key selection
        
    return str(" ".join(ans))               #return joined list as a string

# 50 Points
def test2():
    """Test case for random passage generation."""
    tc = TestCase()
    random.seed(1234)
    simple_toks = [t.lower() for t in 'I really really like cake.'.split()]
    tc.assertEqual(gen_passage(compute_ngrams(simple_toks), 10),
                   'like cake. i really really really really like cake. i')

    random.seed(1234)
    romeo_toks = [t.lower() for t in ROMEO_SOLILOQUY.split()]
    tc.assertEqual(gen_passage(compute_ngrams(romeo_toks), 10),
                   'too bold, \'tis not night. see, how she leans her')

def main():
    test1()
    test2()

if __name__ == '__main__':
    main()
