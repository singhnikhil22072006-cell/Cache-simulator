def choose_victim(entries):
    return min(entries, key=lambda block: (entries[block]["frequency"], entries[block]["last_used"]))
