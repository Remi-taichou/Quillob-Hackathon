import json
from engine import make_pool

pool = make_pool(500)
with open("pool.json", "w") as f:
    json.dump({f"{x}{y}": v for (x, y), v in pool.items()}, f)
print("saved pool.json")