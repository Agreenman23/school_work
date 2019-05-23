# Alex Greenman
# 873392313


class MSPermutations:
    def __init__(self, collection):
        self.collection = collection
    def __iter__(self):
        return MSPIterator(self.collection)



class MSPIterator:
    def __init__(self, collection):
        #self.iter = iter(collection)
        self.collection = collection
        collection = tuple(sorted(collection))
        #this is here because next 'steps through' a collectionber of times whereas, we'd have to add a flag that tells it to only sort once,
        #whereas here it's initialized once to create the object and we're done
    def __str__(self):
        #to return a printable representation of the Iterator object
        return f'{self.collection}'
    def __repr__(self):
        #returns valid expression that could help recreate Iterator object
        return f'MSPIterator({self.collection!r})'
    def __iter__(self):
        return self
    def __next__(self):
        i = len(self.collection) - 1
        #find indices
        while i > 0 and self.collection[i - 1] >= self.collection[i]:
        	i -= 1
        #if we are at index position zero, there are no more permutations
        if i <= 0:
            raise StopIteration

        j = len(self.collection) - 1
        #find indices
        while self.collection[j] <= self.collection[i - 1]:
        	j -= 1
        self.collection = list(self.collection)
        #swap collections
        self.collection[i - 1], self.collection[j] = self.collection[j], self.collection[i - 1]
        #reverse order of all elements from collection[i+1] to end.
        self.collection[i : ] = self.collection[len(self.collection) - 1 : i - 1 : -1]

        return tuple(self.collection)



        #not putting them in lexicographical order each time
        #need to change to tuples, and also need to return the original permutation


        #small changes in the generator syntax


def unique_permutations(nums):
    ans = [[]]
    for n in nums:
        new_ans = []
        for l in ans:
            for i in range(len(l)+1):
                new_ans.append(l[:i]+[n]+l[i:])
                if i<len(l) and l[i]==n:
                    break              #handles duplication
        ans = new_ans
    for elements in ans:
        yield tuple(elements)
