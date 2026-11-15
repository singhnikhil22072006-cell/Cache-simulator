from collections import deque
from backend.algorithms import fifo, lru, lfu, adaptive

class CacheSet:
    def __init__(self, capacity, policy):
        self.capacity = capacity
        self.policy = policy.upper()
        self.entries = {}
        self.clock = 0
        self.recent_hits = deque(maxlen=32)

    def access(self, block):
        self.clock += 1
        hit = block in self.entries
        self.recent_hits.append(1 if hit else 0)
        if hit:
            self.entries[block]["last_used"] = self.clock
            self.entries[block]["frequency"] += 1
            return True, None, None

        evicted, adaptive_mode = None, None
        if len(self.entries) >= self.capacity:
            if self.policy == "FIFO":
                victim = fifo.choose_victim(self.entries)
            elif self.policy == "LRU":
                victim = lru.choose_victim(self.entries)
            elif self.policy == "LFU":
                victim = lfu.choose_victim(self.entries)
            elif self.policy == "ADAPTIVE":
                victim, adaptive_mode = adaptive.choose_victim(self.entries, self.recent_hits)
            else:
                raise ValueError(f"Unknown replacement policy: {self.policy}")
            evicted = victim
            del self.entries[victim]

        self.entries[block] = {"inserted": self.clock, "last_used": self.clock, "frequency": 1}
        return False, evicted, adaptive_mode

    def invalidate(self, block):
        self.entries.pop(block, None)

class Cache:
    def __init__(self, size, block_size, associativity, policy):
        self.size, self.block_size, self.associativity = size, block_size, associativity
        self.lines = size // block_size
        self.num_sets = self.lines // associativity
        self.sets = [CacheSet(associativity, policy) for _ in range(self.num_sets)]

    def access(self, block):
        set_index = block % self.num_sets
        return self.sets[set_index].access(block)

    def contains(self, block):
        return block in self.sets[block % self.num_sets].entries

    def invalidate(self, block):
        self.sets[block % self.num_sets].invalidate(block)

    def blocks(self):
        return {block for cache_set in self.sets for block in cache_set.entries}
