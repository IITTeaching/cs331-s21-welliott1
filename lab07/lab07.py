import random
from unittest import TestCase

################################################################################
# EXTENSIBLE HASHTABLE
################################################################################
class ExtensibleHashTable:

    def __init__(self, n_buckets=1000, fillfactor=0.5):
        self.n_buckets = n_buckets
        self.fillfactor = fillfactor
        self.buckets = [None] * n_buckets
        self.nitems = 0

    def find_bucket(self, key):
        
        h = hash(key) % self.n_buckets
        try:
            while self.buckets[h][0] != key:
                h += 1
                if h == self.n_buckets:
                    h = 0
            assert self.buckets[h] and self.buckets[h][0] == key
            return h
        except:
            raise KeyError()
        

    def __getitem__(self,  key):
        h = self.find_bucket(key)
        assert self.buckets[h] and self.buckets[h][0] == key
        return self.buckets[h][1]

    def extend(self):
        newdata = ExtensibleHashTable(n_buckets=self.n_buckets*2)
        for el in self.items():
            newdata[el[0]] = el[1]
        self.n_buckets *= 2
        self.buckets = newdata.buckets

    def __setitem__(self, key, value):
        
        if self.nitems/self.n_buckets > self.fillfactor:
            self.extend()
        
        h = hash(key) % self.n_buckets
        while self.buckets[h] and self.buckets[h][0]:
            if self.buckets[h][0] == key:
                break
            h += 1
            if h == self.n_buckets:
                h = 0
        else:
            self.nitems += 1
        self.buckets[h] = (key, value)
        

    def __delitem__(self, key):
        h = self.find_bucket(key)
        self.buckets[h] = (None, None)
        self.nitems -= 1
        

    def __contains__(self, key):
        try:
            _ = self[key]
            return True
        except:
            return False

    def __len__(self):
        return self.nitems

    def __bool__(self):
        return self.__len__() != 0

    def __iter__(self):
        slotcount = 0
        itemcount = 0
        while itemcount < self.nitems and slotcount < self.n_buckets:
            if self.buckets[slotcount] and self.buckets[slotcount][0] != None:
                yield self.buckets[slotcount][0]
                itemcount += 1
            slotcount += 1

    def keys(self):
        return iter(self)

    def values(self):
        slotcount = 0
        itemcount = 0
        while itemcount < self.nitems and slotcount < self.n_buckets:
            if self.buckets[slotcount] and self.buckets[slotcount][0] != None:
                yield self.buckets[slotcount][1]
                itemcount += 1
            slotcount += 1

    def items(self):
        slotcount = 0
        itemcount = 0
        while itemcount < self.nitems and slotcount < self.n_buckets:
            if self.buckets[slotcount] and self.buckets[slotcount][0] != None:
                yield self.buckets[slotcount]
                itemcount += 1
            slotcount += 1

    def __str__(self):
        return '{ ' + ', '.join(str(k) + ': ' + str(v) for k, v in self.items()) + ' }'
        

    def __repr__(self):
        return str(self)

################################################################################
# TEST CASES
################################################################################
# points: 20
def test_insert():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100000)

    for i in range(1,10000):
        h[i] = i
        tc.assertEqual(h[i], i)
        tc.assertEqual(len(h), i)

    random.seed(1234)
    for i in range(1000):
        k = random.randint(0,1000000)
        h[k] = k
        tc.assertEqual(h[k], k)

    for i in range(1000):
        k = random.randint(0,1000000)
        h[k] = "testing"
        tc.assertEqual(h[k], "testing")

# points: 10
def test_getitem():
    tc = TestCase()
    h = ExtensibleHashTable()

    for i in range(0,100):
        h[i] = i * 2

    with tc.assertRaises(KeyError):
        h[200]


# points: 10
def test_iteration():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100)
    entries = [ (random.randint(0,10000), i) for i in range(100) ]
    keys = [ k for k, v in entries ]
    values = [ v for k, v in entries ]

    for k, v in entries:
        h[k] = v

    for k, v in entries:
        tc.assertEqual(h[k], v)

    tc.assertEqual(set(keys), set(h.keys()))
    tc.assertEqual(set(values), set(h.values()))
    tc.assertEqual(set(entries), set(h.items()))

# points: 20
def test_modification():
    tc = TestCase()
    h = ExtensibleHashTable()
    random.seed(1234)
    keys = [ random.randint(0,10000000) for i in range(100) ]

    for i in keys:
        h[i] = 0

    for i in range(10):
        for i in keys:
            h[i] = h[i] + 1

    for k in keys:
        tc.assertEqual(h[k], 10)

# points: 20
def test_extension():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100,fillfactor=0.5)
    nitems = 10000
    for i in range(nitems):
        h[i] = i

    tc.assertEqual(len(h), nitems)
    tc.assertEqual(h.n_buckets, 25600)

    for i in range(nitems):
        tc.assertEqual(h[i], i)


# points: 20
def test_deletion():
    tc = TestCase()
    h = ExtensibleHashTable(n_buckets=100000)
    random.seed(1234)
    keys = [ random.randint(0,1000000) for i in range(10) ]
    for k in keys:
        h[k] = 1

    for k in keys:
        del h[k]

    tc.assertEqual(len(h), 0)
    with tc.assertRaises(KeyError):
        h[keys[0]]

    with tc.assertRaises(KeyError):
        h[keys[3]]

    with tc.assertRaises(KeyError):
        h[keys[5]]

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "*" + "\n" + f.__name__)

def say_success():
    print("SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_insert,
              test_iteration,
              test_getitem,
              test_modification,
              test_deletion,
              test_extension]:
        say_test(t)
        t()
        say_success()

if __name__ == '__main__':
    main()
