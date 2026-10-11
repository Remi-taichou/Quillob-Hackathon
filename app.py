import json
import random
import streamlit as st

st.title("Beat the Quantum")
st.write("Alice and Bob can't talk. They win if their answers differ **only when both inputs are 1**.")

mode = st.radio("Mode", ["classical", "quantum"], horizontal=True)
a0 = a1 = b0 = b1 = 0
if mode == "classical":
    st.write("**Design the best classical strategy you can.** Each player answers based only on their own input.")
    c = st.columns(4)
    a0 = c[0].selectbox("Alice, input 0", [0, 1], key="a0")
    a1 = c[1].selectbox("Alice, input 1", [0, 1], key="a1")
    b0 = c[2].selectbox("Bob, input 0", [0, 1], key="b0")
    b1 = c[3].selectbox("Bob, input 1", [0, 1], key="b1")

@st.cache_resource
def get_pool():
    with open("pool.json") as f:
        raw = json.load(f)
    return {(int(k[0]), int(k[1])): [tuple(p) for p in v] for k, v in raw.items()}

def play_round_quantum(x, y, pool):
    return random.choice(pool[(x, y)])

def play_round_classical(x, y):
    return 0, 0

def reset():
    st.session_state.wins = 0
    st.session_state.rounds = 0
    st.session_state.history = []

if "wins" not in st.session_state:
    reset()

if st.session_state.get("last_mode") != mode:
    reset()
    st.session_state.last_mode = mode

def record(x, y, a, b):
    st.session_state.rounds += 1
    st.session_state.wins += int((a ^ b) == (x & y))
    st.session_state.history.append(st.session_state.wins / st.session_state.rounds)

col1, col2 = st.columns(2)
play = col1.button("Auto-play 200 rounds")
col2.button("Reset", on_click=reset)

if play:
    pool = get_pool() if mode == "quantum" else None
    for _ in range(200):
        x, y = random.randint(0, 1), random.randint(0, 1)
        if mode == "quantum":
            a, b = play_round_quantum(x, y, pool)
        else:
            a, b = (a0, a1)[x], (b0, b1)[y]
        record(x, y, a, b)

if st.session_state.rounds:
    rate = st.session_state.wins / st.session_state.rounds
    st.metric("Win rate", f"{rate:.1%}", f"{st.session_state.rounds} rounds")
    st.line_chart(st.session_state.history)
    st.caption("Classical limit: 75%")