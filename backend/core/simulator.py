import pandas as pd
from backend.core.cache_hierarchy import CacheHierarchy
from backend.core.metrics import calculate_metrics
from backend.core.cache_mapping import locate, geometry

POLICIES = ["FIFO", "LRU", "LFU", "ADAPTIVE"]

def validate_config(config):
    for key in ("l1_size", "l2_size", "block_size", "associativity",
                "l1_latency", "l2_latency", "memory_latency"):
        if int(config[key]) <= 0:
            raise ValueError(f"{key} must be greater than zero.")
    if config["l1_size"] > config["l2_size"]:
        raise ValueError("L1 cache size should not exceed L2 cache size.")
    for level in ("l1_size", "l2_size"):
        geometry(config[level], config["block_size"], config["associativity"])

def simulate(trace, config, policy="LRU"):
    validate_config(config)
    if policy.upper() not in POLICIES:
        raise ValueError(f"Policy must be one of {POLICIES}.")
    if not trace:
        raise ValueError("Trace is empty. Load a CSV or sample dataset first.")
    hierarchy = CacheHierarchy(config, policy)
    rows = []
    for index, address in enumerate(trace, start=1):
        result = hierarchy.access(int(address))
        block, set_index, tag = locate(int(address), config["block_size"], hierarchy.l1.num_sets)
        rows.append({
            "access_no": index, "address": f"0x{int(address):X}", "address_decimal": int(address),
            "block": block, "set": set_index, "tag": tag,
            "l1": "HIT" if result["l1_hit"] else "MISS",
            "l2": "—" if result["l2_hit"] is None else ("HIT" if result["l2_hit"] else "MISS"),
            "main_memory": "YES" if result["memory"] else "NO",
            "l1_hit": result["l1_hit"], "l2_hit": result["l2_hit"],
            "memory": result["memory"], "l1_evicted": result["l1_evicted"],
            "l2_evicted": result["l2_evicted"], "adaptive_mode": result["adaptive_mode"]
        })
    metrics = calculate_metrics(rows, config)
    return {"rows": rows, "metrics": metrics, "policy": policy.upper(),
            "config": config.copy(), "dataframe": pd.DataFrame(rows)}
