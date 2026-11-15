from backend.core.cache import Cache

def test_lru_eviction():
    cache=Cache(32,16,2,"LRU")
    assert cache.access(0)[0] is False
    assert cache.access(1)[0] is False
    assert cache.access(0)[0] is True
    hit, evicted, _=cache.access(2)
    assert hit is False
    assert evicted == 1
    assert cache.contains(0)
    assert not cache.contains(1)

def test_direct_mapping_conflict():
    cache=Cache(32,16,1,"FIFO")
    cache.access(0)
    _,evicted,_=cache.access(2)
    assert evicted == 0
