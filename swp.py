from collections import Counter

def loadGraph(edgeFilename):
    '''Reads in the file of data and returns an adjacency list representation
    of the corresponding undirected graph'''
    di = {}
    with open(edgeFilename, 'r') as read:
        for line in read:
            parts = line.split()
            di.setdefault(int(parts[0]),[]).append(int(parts[1]))
            di.setdefault(int(parts[1]),[]).append(int(parts[0]))

    return di


class Queue:
    def __init__(self):
        self.items = []
    def __str__(self):
        return f'{self.items}'
    def is_empty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        return self.items.pop(0)


def bfs(G, s):
    """Conducts breadth-first-search starting with source vertex s"""
    q = Queue()
    infinity = 10000000000
    distances = [infinity for vertex in range(len(G))]
    distances[s] = 0
    distance = 0
    q.enqueue(s)
    while q.is_empty() == False:
        dq = q.dequeue()
        for i in G[dq]:
            if distances[i] < infinity:
                continue
            distances[i] = distances[dq] + 1
            q.enqueue(i)
    return distances

def distanceDistribution(G):
    '''Computes the distribution of all distances in G and returns a dictionary
    that maps positive distances to frequency of occurrence'''
    distance_count = Counter()
    for key in G:
        list_of_distances = []
        a = bfs(G, key)
        distance_count.update(a)
    d = dict(distance_count)
    value_divisor = sum(d.values())
    d_with_percentages = {k: (v / value_divisor)*100 for k, v in d.items()}
    return d_with_percentages


if __name__ == '__main__':
    graph = loadGraph('edges.txt')
    final_distribution_dict = distanceDistribution(graph)
    print(final_distribution_dict)


####SWP Commentary####

# This network mostly satisfies the small world principle (swp), as the distances between
# roughly 98% of the nodes contained in the 'edges.txt' file were six or less.
# It is worth noting that there are a few pairs of nodes that are greater than
# six degrees apart, so the the 'six degrees of separation' theory holds mostly
# but not completely true in this network. The size of the graph represented in
# the 'edges.txt' file is nowhere near as large as the size of the graph that
# represents Facebook user's friendships, so it would be interesting to see what
# their distances to frequency of occurrence percentages look like as point of comparison. 
