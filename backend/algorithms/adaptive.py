def choose_victim(entries, recent_hits):
    """Adaptive heuristic: favor LRU under temporal locality, LFU otherwise."""
    hit_ratio = (sum(recent_hits) / len(recent_hits)) if recent_hits else 0.0
    if hit_ratio >= 0.5:
        return min(entries, key=lambda block: entries[block]["last_used"]), "LRU"
    return min(entries, key=lambda block: (entries[block]["frequency"], entries[block]["last_used"])), "LFU"
