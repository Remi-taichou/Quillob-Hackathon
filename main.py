import math
from qiskit import QuantumCircuit

A = [0, math.pi / 2]        # Alice's angle for input 0 or 1
B = [math.pi / 4, -math.pi / 4]  # Bob's angle for input 0 or 1
SHOTS = 500

def build(x, y, measure=True):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)                      # Bell pair: the entanglement
    qc.ry(-A[x], 0)
    qc.ry(-B[y], 1)
    if measure:
        qc.measure([0, 1], [0, 1])
    return qc

def get_counts(x, y):
    try:
        # Qollab's pre-created backend
        return backend.run(build(x, y), shots=SHOTS).result().get_counts()
    except Exception as e:
        print("(backend run failed, using exact simulation:", type(e).__name__, ")")
        from qiskit.quantum_info import Statevector
        sv = Statevector.from_instruction(build(x, y, measure=False))
        return sv.sample_counts(SHOTS)

print("BEAT THE QUANTUM: CHSH game")
print("Win rule: answers differ only when both inputs are 1")
print("Best classical strategy: 75%")
print()

wins = total = 0
for x in (0, 1):
    for y in (0, 1):
        counts = get_counts(x, y)
        w = n = 0
        for bits, c in counts.items():
            a, b = int(bits[-1]), int(bits[-2])
            n += c
            if (a ^ b) == (x & y):
                w += c
        wins += w
        total += n
        print(f"inputs x={x}, y={y}: win rate {w / n:.1%}  {dict(counts)}")

print()
print(f"OVERALL QUANTUM WIN RATE: {wins / total:.1%}")
print("Classical limit: 75.0%   Quantum maximum: 85.4%")
print("The gap comes entirely from the shared entangled pair.")