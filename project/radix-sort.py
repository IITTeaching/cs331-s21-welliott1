import urllib
import requests
import unittest

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    return radixSort(book_to_words())

def countingSort(array, index, maximum):
 
    length = len(array)
    result = [0]*length
    countarr = [0]*256
 
    for i in range(0, length):
        
        diff = maximum-len(array[i])
        
        if diff >= index+1:
            index2 = 0
            countarr[index2]+=1

        else:
            index2 = int(array[i][diff-(index+1)])
            countarr[index2]+=1
 
    for i in range(0, 256):
        countarr[i]+=countarr[i-1]

    i = length-1

    while i >= 0:

        diff = maximum-len(array[i])
        if diff >= index+1:
            index2 = 0

        else:
            index2 = int(array[i][diff-(index+1)])
        result[countarr[index2] - 1] = array[i]
        countarr[index2] -= 1
        i-=1
 
    i = 0
    for i in range(0, len(array)):
        array[i] = result[i]
 

def radixSort(array):
 
    answer = array
    maximum = len(array[0])
    
    for s in array:
        if maximum < len(s):
            maximum = len(s)

    for i in range(maximum):
        countingSort(answer, i, maximum)
    
    return answer

def test1():
    
    tc = unittest.TestCase()
    book_url='https://www.gutenberg.org/files/84/84-0.txt'
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    words = bookascii.split()
    radix_sort, sort = radix_a_book(), sorted(words)
    test_do(radix_sort, sort)
    say_success()

def test_do(radix_sort, sort):
    """everything"""
    print("\t-sort the entire book.")
    tc = unittest.TestCase()
    tc.assertTrue(radix_sort == sort)

def say_success():
    print("\t\t*** SUCCESS ***")

def main():
    test1()
    print(80 * "#" + "\nentire book sorted SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()