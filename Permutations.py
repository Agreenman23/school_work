#Alex Greenman
#873392313
#This program generates all of the unique permutations of a set of elements
#using a basic algorithm. The algorithm is coded as an iterator class and as a
#generator function. Both the iterator class and generator function output the
#permutations as tuples.

class MSPermutations:
    '''Initializes the given collection and creates and returns MSPIterator to
    perform an iteration of the given collection'''
    def __init__(self, collection):
        self.collection = collection
    def __iter__(self):
        return MSPIterator(self.collection)

class MSPIterator:
    '''Initializes an MSPIterator object with the given collection, returns the
    current iterator object, and implements the permutation algorithm'''
    def __init__(self, collection):
        #convert initial collection into sorted tuple
        self.collection = tuple(sorted(collection))
        #create a counter used to denote first iteration of '__next__'
        self.count = 0
    def __iter__(self):
        return self
    def __next__(self):
        #if the collection is empty, stop iteration and output nothing
        if len(self.collection) == 0:
            raise StopIteration
        #check if this is the first time 'next' is called; if it is, the
        #original sorted tuple is returned; if not, statement will not execute
        if self.count == 0:
            #increment to indicate iterator has been run at least once
            self.count+=1
            return tuple(self.collection)

        i = len(self.collection) - 1
        #starts by looking at last two indices in self.collection.
        #If last two indices do not satisfy collection[i] < collection[i+1],
        #decrement i by 1. If self.collection[i] < self.collection[i+1]
        #is satisfied, then while loop will not execute.
        while i > 0 and self.collection[i - 1] >= self.collection[i]:
        	i -= 1
        #if at index position zero, there are no more permutations
        if i <= 0:
            raise StopIteration

        j = len(self.collection) - 1
        #compares last index in self.collection to the index position
        #determined by what i has been decremented to minus one. If these
        #indices do not satisfy self.collection[i] < self.collection[j],
        #decrement j by 1. If self.collection[i] < self.collection[j] is
        #satisfied, then while loop will not execute.
        while self.collection[j] <= self.collection[i - 1]:
        	j -= 1
        #convert self.collection to list so it can be reordered
        self.collection = list(self.collection)
        #swap self.collection[i-1] and self.collection [j]
        self.collection[i - 1], self.collection[j] = self.collection[j], self.collection[i - 1]
        #reverse order of all elements from self.collection[i+1] to end.
        self.collection[i : ] = self.collection[len(self.collection) - 1 : i - 1 : -1]

        return tuple(self.collection)

def unique_permutations(collection):
    '''Utilizes the same basic algorithm to yield tuples containing each
    permutation of the given collection'''
    #convert initial collection into sorted list
    collection = sorted(collection)
    #if the collection is empty, stop iteration, output nothing
    if len(collection) == 0:
        return
    #initialize counter to track whether or not this is first call of generator
    counter = 0
    while True:
        #check if this is the first time the generator has been called;
        #if so, return original sorted tuple; if not, statement doesn't execute
        if counter == 0:
            yield tuple(collection)
        output = []
        i = len(collection) - 1
        #Starts by looking at last two indices in collection.
        #If last two indices do not satisfy collection[i] < collection[i+1],
        #decrement i by 1. If collection[i] < collection[i+1] is satisfied,
        #then while loop will not execute.
        while i > 0 and collection[i - 1] >= collection[i]:
        	i -= 1
        #if we are at index position zero, there are no more permutations
        if i <= 0:
            return

        j = len(collection) - 1
        #Compares last index in collection to the index position
        #determined by what i has been decremented to minus one. If these
        #indices do not satisfy collection[i] < collection[j], decrement j by 1.
        #If collection[i] < collection[j] is satisfied, then while loop will
        #not execute.
        while collection[j] <= collection[i - 1]:
        	j -= 1
        #swap collection[i-1] and collection[j]
        collection[i - 1], collection[j] = collection[j], collection[i - 1]
        #reverse order of all elements from collection[i+1] to end.
        collection[i : ] = collection[len(collection) - 1 : i - 1 : -1]
        #add tuples containing each permutation to empty list
        output += tuple(collection)
        yield tuple(output)
        counter +=1
        #increment counter to indicate generator has been run at least once
