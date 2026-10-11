Beat the Quantum

Built from scratch during the hackathon window (October 9-11, 2026)

An interactive demo of the CHSH game, showing a case where entanglement does something no classical strategy can. Built for the Global Qollab Quantum Hackathon (Quantum Playground theme).


Demo video: (https://drive.google.com/drive/folders/1CVn2C7A0JjvwM9-c2-qODCvewJ63WhbW?usp=sharing)

Qollab project page:(https://qollab.xyz/p/01a12cde-afb6-727a-9ebd-5d8d49eabd97?v=v1.0)





What it is:
Alice and Bob are far apart and can't communicate. Each one gets a random bit (0 or 1) and must answer with a bit. They win the round if:
their answers are different when both inputs are 1
their answers are the same otherwise
Try to design the best strategy you can. Then switch to quantum mode and watch the win rate climb past what any strategy can reach.

Why entanglement is essential:
Classical players can agree on any strategy in advance, but each answer can only depend on that player's own input. The best they can do is win 75% of rounds. This is a proven limit (Bell/CHSH inequality), and the app lets you try all 16 deterministic strategies to see it for yourself.
Quantum players share an entangled Bell pair. Each player measures their qubit at an angle chosen by their input bit. The correlations between the two measurements let them win about 85% of rounds (theoretical value: cos²(π/8) ≈ 85.4%).
Without the shared entangled pair, the quantum mode has no advantage. The gap between 75% and 85% comes entirely from entanglement.


How to play:
The Qollab project runs the quantum core in main.py. The full interactive Streamlit game is in the GitHub repo and demo video.
To just play the game, you only need 'pip install streamlit' and 'streamlit run app.py', because 'pool.json' is included.
Classical mode: pick an answer for each player and each input (four dropdowns), then click Auto-play 200 rounds. No choice beats ~75%.
Quantum mode: click Auto-play 200 rounds and watch the win rate settle near 85%.
Use Reset to clear the chart. Switching modes also resets it.

How to run:
pip install qiskit qiskit-aer qiskit-ionq streamlit numpy
export IONQ_API_KEY="your-key"   # only needed for make_pool_ionq.py
python make_pool_ionq.py         # or: python make_pool.py (local)
streamlit run app.py

How the quantum results are made:
make_pool_ionq.py builds the Bell-pair circuit for each of the four input pairs (x, y), runs it for 500 shots on IonQ’s cloud simulator through the Qiskit IonQ provider, and saves every measurement result to pool.json. During a game, each quantum round draws one of those real measurement results for the chosen inputs. make_pool.py is a local Aer version for running without an IonQ account.
The circuit for inputs (x, y):
Hadamard on qubit 0, then CNOT from qubit 0 to qubit 1 (creates the Bell pair)
Rotate Alice's qubit based on x and Bob's qubit based on y
Measure both qubits

Files:
- `engine.py`: circuit construction and the shot pool
- `make_pool_ionq.py`: runs the circuits on IonQ's simulator and writes `pool.json`
- `make_pool.py`: local Aer version of the same step
- `pool.json`: the saved measurement results (from the IonQ simulator), so the app runs without an API key
- `app.py`: Streamlit game UI


Team Undecided lol

License
MIT. See LICENSE.