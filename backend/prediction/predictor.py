from collections import Counter

def analyze_trace(trace, block_size=16):
    if not trace:
        return {"pattern": "No trace", "frequent": [], "stride": None, "next": None, "confidence": 0.0, "details": "Load a trace to analyze patterns."}
    blocks = [a // block_size for a in trace]
    counts = Counter(blocks)
    frequent = counts.most_common(8)
    diffs = [blocks[i+1] - blocks[i] for i in range(len(blocks)-1)]
    stride, stride_count = (Counter(diffs).most_common(1)[0] if diffs else (None, 0))
    confidence = stride_count / len(diffs) if diffs else 0.0

    if len(blocks) >= 4 and len(set(diffs)) == 1 and diffs[0] == 1:
        pattern, next_block, confidence = "Sequential", blocks[-1] + 1, 1.0
    elif len(set(blocks)) <= max(2, len(blocks) // 10):
        pattern, next_block = "Repeated access", counts.most_common(1)[0][0]
        confidence = counts.most_common(1)[0][1] / len(blocks)
    elif len(blocks) >= 8 and any(blocks[-period:] == blocks[-2*period:-period]
                                  for period in range(2, min(16, len(blocks)//2) + 1)):
        period = next(period for period in range(2, min(16, len(blocks)//2) + 1)
                      if blocks[-period:] == blocks[-2*period:-period])
        pattern, next_block, confidence = "Loop-based", blocks[-period], 0.85
    elif diffs and stride is not None and stride != 0 and confidence >= 0.65:
        pattern, next_block = "Stride-based", blocks[-1] + stride
    else:
        pattern, next_block = "Random / irregular", None
        confidence = max(confidence, 0.0) * 0.5

    return {
        "pattern": pattern,
        "frequent": [{"block": b, "accesses": n, "address": f"0x{b*block_size:X}"} for b, n in frequent],
        "stride": stride,
        "next": (next_block * block_size) if next_block is not None else None,
        "confidence": confidence,
        "details": "Pattern detection uses block-level frequency and address-difference heuristics; it is not a trained machine-learning model."
    }
