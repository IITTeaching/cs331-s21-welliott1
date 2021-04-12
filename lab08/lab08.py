from unittest import TestCase
import random
import functools

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################
class Heap:
    def __init__(self, key=lambda x:x):
        self.data = []
        self.key  = key

    @staticmethod
    def _parent(idx):
        return (idx-1)//2

    @staticmethod
    def _left(idx):
        return idx*2+1

    @staticmethod
    def _right(idx):
        return idx*2+2

    def posExists(self,n):
        return n < len(self.data)

    def hasParent(self,n):
        return (n-1)//2 >=0

    def swap(self,parent,child):
        parent_temp = self.data[parent]
        child_temp = self.data[child]
        self.data[parent] = child_temp
        self.data[child] = parent_temp

    def heapify(self, idx=0):
        swapee = None
        while self.posExists(self._left(idx)):
            swapee = self._left(idx)
            if self.posExists(self._right(idx)) and self.key(self.data[self._right(idx)]) > self.key(self.data[self._left(idx)]):
                swapee = self._right(idx)
            if self.key(self.data[idx]) > self.key(self.data[swapee]):
                break
            else:
                self.swap(idx,swapee)
            idx = swapee


    def add(self, x):
        self.data.append(x)
        idx = len(self.data)-1
        while self.hasParent(idx) and self.key(self.data[self._parent(idx)]) < self.key(self.data[idx]):
                temp = self._parent(idx)
                self.swap(self._parent(idx),idx)
                idx = temp


    def peek(self):
        return self.data[0]

    def pop(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data)-1]
        del self.data[len(self.data)-1]
        self.heapify()
        return ret

    def __iter__(self):
        return self.data.__iter__()

    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################

# (6 point)
def test_key_heap_1():
    from unittest import TestCase
    import random

    tc = TestCase()
    h = Heap()

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [97, 61, 65, 49, 51, 53, 62, 5, 38, 33])

# (6 point)
def test_key_heap_2():
    tc = TestCase()
    h = Heap(lambda x:-x)

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [5, 33, 53, 38, 49, 65, 62, 97, 51, 61])

# (6 points)
def test_key_heap_3():
    tc = TestCase()
    h = Heap(lambda s:len(s))

    h.add('hello')
    h.add('hi')
    h.add('abracadabra')
    h.add('supercalifragilisticexpialidocious')
    h.add('0')

    tc.assertEqual(h.data,
                   ['supercalifragilisticexpialidocious', 'abracadabra', 'hello', 'hi', '0'])

# (6 points)
def test_key_heap_4():
    tc = TestCase()
    h = Heap()

    random.seed(0)
    lst = list(range(-1000, 1000))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in range(999, -1000, -1):
        tc.assertEqual(x, h.pop())

# (6 points)
def test_key_heap_5():
    tc = TestCase()
    h = Heap(key=lambda x:abs(x))

    random.seed(0)
    lst = list(range(-1000, 1000, 3))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in reversed(sorted(range(-1000, 1000, 3), key=lambda x:abs(x))):
        tc.assertEqual(x, h.pop())

################################################################################
# 2. MEDIAN
################################################################################
def running_medians(iterable):
    medians = []
    higher_min_heap = Heap(lambda x: -1 * x)
    lower_max_heap = Heap()
    median = None
    for i,x in enumerate(iterable):
        if len(medians)==0:
            median = iterable[0]
            higher_min_heap.add(x)
            medians.append(iterable[0])
        elif x>median:
            higher_min_heap.add(x)
        elif x<median:
            lower_max_heap.add(x)
        else:
            if len(lower_max_heap) <= len(higher_min_heap):
                lower_max_heap.add(x)
            else:
                higher_min_heap.add(x)
            

        if abs(len(higher_min_heap) - len(lower_max_heap)) > 1:
            if len(higher_min_heap) > len(lower_max_heap):
                while len(higher_min_heap) - len(lower_max_heap) >1:
                    lower_max_heap.add(higher_min_heap.pop())
            else:
                while len(lower_max_heap) - len(higher_min_heap) >1:
                    higher_min_heap.add(lower_max_heap.pop())
        if i>0:
            if len(higher_min_heap) == len(lower_max_heap):
                median = ((higher_min_heap.peek() + lower_max_heap.peek())) / 2
            elif len(higher_min_heap) > len(lower_max_heap):
                median = higher_min_heap.peek()
            elif len(lower_max_heap) > len(higher_min_heap):
                median = lower_max_heap.peek()
            medians.append(median)

    return medians

################################################################################
# TESTS
################################################################################
def running_medians_naive(iterable):
    values = []
    medians = []
    for i, x in enumerate(iterable):
        values.append(x)
        values.sort()
        if i%2 == 0:
            medians.append(values[i//2])
        else:
            medians.append((values[i//2] + values[i//2+1]) / 2)
    return medians

# (13 points)
def test_median_1():
    tc = TestCase()
    tc.assertEqual([3, 2.0, 3, 6.0, 9], running_medians([3, 1, 9, 25, 12]))

# (13 points)
def test_median_2():
    tc = TestCase()
    vals = [random.randrange(10000) for _ in range(1000)]
    tc.assertEqual(running_medians_naive(vals), running_medians(vals))

# MUST COMPLETE IN UNDER 10 seconds!
# (14 points)
def test_median_3():
    tc = TestCase()
    vals = [random.randrange(100000) for _ in range(100001)]
    m_mid   = sorted(vals[:50001])[50001//2]
    m_final = sorted(vals)[len(vals)//2]
    running = running_medians(vals)
    tc.assertEqual(m_mid, running[50000])
    tc.assertEqual(m_final, running[-1])

################################################################################
# 3. TOP-K
################################################################################
def topk(items, k, keyf):
    ### BEGIN SOLUTION
    pass
    ### END SOLUTION

################################################################################
# TESTS
################################################################################

def get_age(s):
    return s[1]

def naive_topk(l,k,keyf):
    revkey = lambda x: keyf(x) * -1
    return sorted(l, key=revkey)[0:k]

# (30 points)
def test_topk_students():
    tc = TestCase()
    students = [ ('Peter', 33), ('Bob', 23), ('Alice', 21), ('Gertrud', 53) ]

    tc.assertEqual(naive_topk(students, 2, get_age),
                   topk(students, 2, get_age))

    tc.assertEqual(naive_topk(students, 1, get_age),
                   topk(students, 1, get_age))

    tc.assertEqual(naive_topk(students, 3, get_age),
                   topk(students, 3, get_age))

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
    for t in [test_key_heap_1,
              test_key_heap_2,
              test_key_heap_3,
              test_key_heap_4,
              test_key_heap_5,
              test_median_1,
              test_median_2,
              test_median_3,
              test_topk_students
              ]:
        say_test(t)
        t()
        say_success()

if __name__ == '__main__':
    main()
