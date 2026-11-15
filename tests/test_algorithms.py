from backend.core.simulator import simulate
from tests.helpers import CONFIG, TRACE

def test_all_policies_run():
    for policy in ["FIFO","LRU","LFU","ADAPTIVE"]:
        result=simulate(TRACE,CONFIG,policy)
        assert result["metrics"]["total_accesses"] == len(TRACE)
        assert 0 <= result["metrics"]["overall_hit_rate"] <= 1
