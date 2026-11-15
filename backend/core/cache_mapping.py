def geometry(cache_size: int, block_size: int, associativity: int):
    """Return (number_of_lines, number_of_sets), validating cache geometry."""
    if cache_size <= 0 or block_size <= 0 or associativity <= 0:
        raise ValueError("Cache size, block size, and associativity must be positive.")
    if cache_size % block_size:
        raise ValueError("Cache size must be divisible by block size.")
    lines = cache_size // block_size
    if lines % associativity:
        raise ValueError("Number of cache lines must be divisible by associativity.")
    return lines, lines // associativity

def locate(address: int, block_size: int, number_of_sets: int):
    block = address // block_size
    set_index = block % number_of_sets
    tag = block // number_of_sets
    return block, set_index, tag
