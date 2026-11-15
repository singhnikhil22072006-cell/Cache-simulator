from backend.core.simulator import validate_config

def validate_trace(trace):
    if not trace:
        raise ValueError("Please load a non-empty memory trace.")
    if any(not isinstance(a, int) or a < 0 for a in trace):
        raise ValueError("Trace must contain non-negative integer addresses.")
    return True

def validate_all(config, trace):
    validate_config(config)
    validate_trace(trace)
    return True
