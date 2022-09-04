import itertools
import heapq

REMOVED = '<remove>'

class PriorityQueue:
    """
    Priority queue, based on the example in
    the Python docs:https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """
    def __init__(self):
        self.heap = []
        # map of item -> heap entry
        self.reverse_lookup = {}
        # Counter for keeping track of 
        # insertion order
        self.counter = itertools.count()
    
    def __len__(self):
        total = 0
        for x in self.heap:
            if x[-1] != REMOVED:
                total += 1
        return total
    
    def add(self, item, priority):
        if item in self.reverse_lookup:
            self.remove(item)

        count = next(self.counter)
        entry = [priority, count, item]
        self.reverse_lookup[item] = entry
        heapq.heappush(self.heap, entry)
    
    def remove(self, item):
        entry = self.reverse_lookup.pop(item)
        entry[-1] = REMOVED
    
    def pop(self):
        """
        Remove and return the lowest-priority task,
        or none if the queue is empty
        """
        while self.heap:
            _, _, item = heapq.heappop(self.heap)
            if item is not REMOVED:
                del self.reverse_lookup[item]
                return item
        return None