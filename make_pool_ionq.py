import json
import random
from qiskit import transpile
from qiskit_ionq import IonQProvider
from engine import build_circuit

provider = IonQProvider()  # reads IONQ_API_KEY from the environment
backend = provider.get_backend("simulator")

SHOTS = 500
pool = {}
for x in (0, 1):
    for y in (0, 1):
        qc = transpile(build_circuit(x, y), backend, optimization_level=1)
        job = backend.run(qc, shots=SHOTS)
        counts = job.result().get_counts()
        print(x, y, counts)
        bits = random.choices(list(counts), weights=list(counts.values()), k=SHOTS)
        pool[f"{x}{y}"] = [(int(m[-2]), int(m[-1])) for m in bits]

with open("pool.json", "w") as f:
    json.dump(pool, f)
print("saved pool.json from IonQ simulator")