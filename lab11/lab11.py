from unittest import TestCase
import random

def quicksort(lst,pivot_fn):
    qsort(lst,0,len(lst) - 1,pivot_fn)

def qsort(lst,low,high,pivot_fn):
    ### BEGIN SOLUTION
    if low<high:
        p = pivot_fn(lst,low,high)
        qsort(lst,low,p-1,pivot_fn)
        qsort(lst,p+1,high,pivot_fn)
        
    
    
    ### END SOLUTION

def pivot_first(lst,low,high):
    ### BEGIN SOLUTION
    pivot = lst[low]

    h = high

    for k in range(high,low,-1):
        if lst[k] > pivot:
            lst[h], lst[k] = lst[k], lst[h]
            h = h-1
    
    lst[h],lst[low] = lst[low], lst[h]

    return h
    ### END SOLUTION

def pivot_random(lst,low,high):
    ### BEGIN SOLUTION
    rint = random.randint(low,high)
    pivot = lst[rint]
    lst[rint],lst[low] = lst[low], lst[rint]

    h = high

    for k in range(high,low,-1):
        if lst[k] > pivot:
            lst[h], lst[k] = lst[k], lst[h]
            h = h-1
    
    lst[h],lst[low] = lst[low], lst[h]
    
    return h
    ### END SOLUTION

def pivot_median_of_three(lst,low,high):
    ### BEGIN SOLUTION
    med = find_median(lst,low,((low+high)//2),high)
    pivot = lst[med]
    lst[med],lst[low] = lst[low],lst[med]
    h = high

    for k in range(high,low,-1):
        if lst[k] > pivot:
            lst[h], lst[k] = lst[k], lst[h]
            h = h-1
    
    lst[h],lst[low] = lst[low], lst[h]

    return h
    ### END SOLUTION

def find_median(lst,left,mid,right):
    leftel = lst[left]
    midel = lst[mid]
    rightel = lst[right]

    if (leftel > midel and leftel < rightel) or (leftel > rightel and leftel < midel):
        return left
    elif (midel > leftel and midel < rightel) or (midel > rightel and midel < leftel):
        return mid
    elif (rightel > midel and rightel < leftel) or (rightel > leftel and rightel < midel):
        return right
    return left

################################################################################
# TEST CASES
################################################################################
def randomize_list(size):
    lst = list(range(0,size))
    for i in range(0,size):
        l = random.randrange(0,size)
        r = random.randrange(0,size)
        lst[l], lst[r] = lst[r], lst[l]
    return lst

def test_lists_with_pfn(pfn):
    lstsize = 20
    tc = TestCase()
    exp = list(range(0,lstsize))

    lst = list(range(0,lstsize))
    quicksort(lst, pivot_first)
    tc.assertEqual(lst,exp)

    lst = list(reversed(range(0,lstsize)))
    quicksort(lst, pivot_first)
    tc.assertEqual(lst,exp)

    for i in range(0,100):
        lst = randomize_list(lstsize)
        quicksort(lst, pfn)
        tc.assertEqual(lst,exp)

# 30 points
def test_first():
    test_lists_with_pfn(pivot_first)

# 30 points
def test_random():
    test_lists_with_pfn(pivot_random)

# 40 points
def test_median():
    test_lists_with_pfn(pivot_median_of_three)

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_first,
              test_random,
              test_median]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()
