from random import randint, choice

from src.domain.entities import Book

""""
this module provides sorting and filterning functionalities
each module can be later used
"""

def gnomeSort(iterable, cmpFunction = None, reverse = False):
    """"
    :param iterable: the data structure sorted
    :param cmpFunction used for comparing elements, < if None
    :param reverse : sort in reverse order
    """
    if iterable == None:
        return None
    if reverse == True:
        reverse = -1
    else:
        reverse = 1
    pos = 1
    while pos < len(iterable):
        if cmpFunction == None:
            if reverse * (iterable[pos] - iterable[pos-1]) >= 0:
                pos += 1
            else:
                iterable[pos], iterable[pos-1] = iterable[pos-1], iterable[pos]
        else:
            if reverse * cmpFunction(iterable[pos],iterable[pos-1]) >= 0:
                pos += 1
            else:
                iterable[pos], iterable[pos-1] = iterable[pos-1], iterable[pos]
                if pos > 1:
                    pos -= 1
    return iterable


def filter(iterable, filter_function):
    """"
    Function to filter
    :param iterable: the list to be filtered
    :param filter_function: function to check if the element
    can be filtered or not
    """
    return [x for x in iterable if filter_function(x)]

def isSorted(iterable, cmp_function = None, reverse = False):
    """"
    Function to check if the list is sorted or not
    :param iterable: the data structure that needs to be checked
    :param cmp_function: function used to compare elements
    :param reverse: the reversed order
    :return True / False : list sorted ? list not sorted
    """
    n = len(iterable)
    if reverse == True:
        reverse = -1
    else:
        reverse = 1
    for i in range(n-1):
        if cmp_function == None:
            if reverse * (iterable[i] - iterable[i+1] > 0):
                return False
        else:
            if reverse * cmp_function(iterable[i], iterable[i+1]) > 0:
                return False
    return True


def testSpecialCases():
    """"
    Function that tests special cases when there is no element in the list
    """
    x = []
    assert gnomeSort(x, None, False) == []
    x = None
    assert gnomeSort(x, None, False) == None


def BooksByID(a, b):
    if a.entity_id < b.entity_id:
        return -1
    elif a.entity_id > b.entity_id:
        return 1
    else:
        return 0


def booksByAuthor(a, b):
    if a.author < b.author:
        return -1
    elif a.author > b.author:
        return 1
    else:
        return 0



def testBooksSort():

    x = [Book(0, "Cracking the coding interview", "Must have", "Gayle McDowell"), \
         Book(1, "Introduction to Algorithms", "the programmer's Bible", "Cormen"), \
         Book(2, "Algorithm Design", "best cs tool", "Steve Skiene")
         ]
    gnomeSort(x, booksByAuthor, False)
    assert isSorted(x, booksByAuthor, False) == True
    gnomeSort(x, booksByAuthor, True)
    assert isSorted(x, booksByAuthor, True) == True
    gnomeSort(x, BooksByID, False)
    assert isSorted(x, BooksByID, False) == True


def intLess(x, y):
    if x < y:
        return -1
    elif x > y:
        return 1
    else:
        return 0


def intGre(x, y):
    return -intLess(x, y)


def testIntegerSort():
    """"
    function to test the process of sorting in integer case
    """
    for t in range(10):
        l = randint(1, 1000)
        x = [randint(1, 10000) for x in range(l)]
        gnomeSort(x, intLess, False)
        if not isSorted(x, intLess, False):
            assert False

    for test in range(10):
        l = randint(1, 100)
        x = [randint(1, 10000) for x in range(l)]
        gnomeSort(x, intGre, False)
        if not isSorted(x, intGre, False):
            assert False

def test_sort():
    """"
    Function to call all test functions
    """
    testSpecialCases()
    testBooksSort()
    testIntegerSort()

test_sort()