def calculate_metrics(rows, config):
    total = len(rows)
    if not total:
        raise ValueError("Cannot calculate metrics for an empty trace.")
    l1_hits = sum(r["l1_hit"] for r in rows)
    l1_misses = total - l1_hits
    l2_hits = sum(r["l2_hit"] is True for r in rows)
    memory_misses = sum(r["memory"] for r in rows)
    l1_miss_rate = l1_misses / total
    l2_conditional_miss_rate = (memory_misses / l1_misses) if l1_misses else 0.0
    overall_hits = l1_hits + l2_hits
    overall_miss_rate = memory_misses / total
    amat = config["l1_latency"] + l1_miss_rate * (
        config["l2_latency"] + l2_conditional_miss_rate * config["memory_latency"]
    )
    return {
        "total_accesses": total, "l1_hits": l1_hits, "l1_misses": l1_misses,
        "l2_hits": l2_hits, "memory_misses": memory_misses,
        "overall_hits": overall_hits, "overall_miss_rate": overall_miss_rate,
        "l1_hit_rate": l1_hits / total, "l1_miss_rate": l1_miss_rate,
        "l2_conditional_hit_rate": (l2_hits / l1_misses) if l1_misses else 0.0,
        "l2_conditional_miss_rate": l2_conditional_miss_rate,
        "overall_hit_rate": overall_hits / total, "amat": amat
    }
