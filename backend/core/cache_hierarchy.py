from backend.core.cache import Cache

class CacheHierarchy:
    """Inclusive two-level hierarchy: every L1-resident block also resides in L2."""
    def __init__(self, config, policy):
        self.config = config
        self.l1 = Cache(config["l1_size"], config["block_size"], config["associativity"], policy)
        self.l2 = Cache(config["l2_size"], config["block_size"], config["associativity"], policy)

    def access(self, address):
        block = address // self.config["block_size"]
        # Probe L1 first. A miss must not allocate/evict until the lower level
        # has been checked; otherwise a provisional L1 insert can evict a line.
        if self.l1.contains(block):
            self.l1.access(block)  # update recency/frequency metadata
            return {"l1_hit": True, "l2_hit": None, "memory": False,
                    "l1_evicted": None, "l2_evicted": None, "adaptive_mode": None}

        l2_hit, l2_evict, l2_mode = self.l2.access(block)
        if l2_evict is not None:
            # Inclusive policy: an L2 eviction invalidates any corresponding L1 copy.
            self.l1.invalidate(l2_evict)

        _, l1_evict, l1_mode = self.l1.access(block)
        return {"l1_hit": False, "l2_hit": l2_hit, "memory": not l2_hit,
                "l1_evicted": l1_evict, "l2_evicted": l2_evict,
                "adaptive_mode": l1_mode or l2_mode}
