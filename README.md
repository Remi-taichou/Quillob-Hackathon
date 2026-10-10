# Quillob-Hackathon
...

After deliberation with Claude; these are the ideas i have based on a time construct and seeing we're behind
(feel free to add anything and by 1pm latest 2pm we would decide on what we would build and ship)


Option 1: Beat the Quantum (CHSH game)(the playground theme of the hackathon)
The game: Two players, Alice and Bob, are separated and can't talk. Each gets a random bit (0 or 1) and must answer with a bit. They win if their answers differ only when both inputs are 1.

•	Classical players: the best strategy wins at most 75% of the time. This is a proven limit.
•	Players sharing an entangled pair: they can win about 85% of the time, just by measuring their qubit at an angle that depends on their input.


What we'd build:
•	A simple web or Python UI where the user plays as Alice (or Alice and Bob) and tries to beat 75%
•	A button to switch to "quantum mode," where Qiskit runs the Bell pair on the simulator
•	A live win-rate graph over hundreds of rounds, so the gap becomes visible

The demo video basically writes itself: "Try to beat 75%. You can't. Now watch entanglement do it."



Option 2 (unlocked)
Grover's Visualizer

The idea: Grover's algorithm finds a marked item in an unsorted list by repeatedly nudging probability toward the right answer.

With 3 qubits (8 items), the right answer's probability goes roughly:
•	Start: 12.5%
•	After 1 step: ~78%
•	After 2 steps: ~94.5%
•	After 3 steps: drops to ~33%, because it overshoots

What we'd build:
•	An animated bar chart of all 8 outcomes
•	A "step" button or slider to apply one Grover iteration at a time
•	The user picks the target item, and the chart shows it rising

The overshoot is the surprising bit that makes people remember it.


How they compare
•	Option 1 is more interactive and has a stronger "wow." It needs a bit more game logic.
•	Option 2 is simpler to code and very clear, but more of a lecture. Adding the user-picked target and the overshoot slider keeps it engaging.

$$-These were just some i came up with usung Claude seeing we're already behind on time.

