import random
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

sim = AerSimulator(max_parallel_threads=1)
A = [0, np.pi/2]
B = [np.pi/4, -np.pi/4]

def build_circuit(x, y):
    qc = QuantumCircuit(2, 2)
    qc.h(0); qc.cx(0, 1)
    qc.ry(-A[x], 0); qc.ry(-B[y], 1)
    qc.measure([0, 1], [0, 1])
    return qc

def make_pool(shots=500):
    """Run each input pair once in a batch and keep every shot's result."""
    pool = {}
    for x in (0, 1):
        for y in (0, 1):
            mem = sim.run(build_circuit(x, y), shots=shots, memory=True).result().get_memory()
            pool[(x, y)] = [(int(m[1]), int(m[0])) for m in mem]  # (Alice, Bob)
    return pool

def play_round_quantum(x, y, pool):
    return random.choice(pool[(x, y)])

def play_round_classical(x, y):
    return 0, 0  # best classical strategy, wins 75%

if __name__ == "__main__":
    pool = make_pool()
    wins = 0
    for _ in range(1000):
        x, y = random.randint(0, 1), random.randint(0, 1)
        a, b = play_round_quantum(x, y, pool)
        wins += (a ^ b) == (x & y)
    print(wins / 1000)

    MJcMFNLNZRH2OMgZQzwqlOm1u6YfXuyT
