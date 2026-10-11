import json
import random
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Beat the Quantum", page_icon="⚛️")


def quantum_theme():
    symbols = ["|0⟩", "|1⟩", "|ψ⟩", "⟨ψ|", "|+⟩", "|Φ⁺⟩", "H", "⊗", "ħ", "∿"]
    rng = random.Random(7)
    items = ""
    for _ in range(20):
        s = rng.choice(symbols)
        color = rng.choice(["#22D3EE", "#8B5CF6"])
        items += (f'<span style="left:{rng.randint(0, 95)}%;font-size:{rng.randint(16, 40)}px;'
                  f'color:{color};animation-duration:{rng.randint(14, 30)}s;'
                  f'animation-delay:-{rng.randint(0, 30)}s">{s}</span>')
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Share+Tech+Mono&display=swap');
    h1,h2,h3{font-family:'Orbitron',sans-serif !important;}
    html,body,.stApp,[data-testid="stMarkdownContainer"],label,button,[data-testid="stCaptionContainer"]{
        font-family:'Share Tech Mono',monospace !important;}
    [data-testid="stMetricValue"]{font-family:'Orbitron',sans-serif !important;}
    .stApp{background-image:
        linear-gradient(rgba(34,211,238,.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(34,211,238,.06) 1px, transparent 1px);
        background-size:44px 44px;}
    h1{color:#22D3EE !important;text-shadow:0 0 18px rgba(34,211,238,.7), 0 0 40px rgba(139,92,246,.5);
       letter-spacing:2px;}
    [data-testid="stMetricValue"]{color:#22D3EE;text-shadow:0 0 14px rgba(34,211,238,.8);}
    .stButton>button{background:transparent;border:1px solid #22D3EE;color:#22D3EE;
        box-shadow:0 0 10px rgba(34,211,238,.35);transition:all .2s;}
    .stButton>button:hover{background:rgba(34,211,238,.15);box-shadow:0 0 22px rgba(34,211,238,.8);
        color:#fff;border-color:#8B5CF6;}
    .qbg{position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:0;}
    .qbg span{position:absolute;bottom:-60px;opacity:.22;font-family:monospace;
        animation-name:qfloat;animation-timing-function:linear;animation-iteration-count:infinite;}
    @keyframes qfloat{0%{transform:translateY(0) rotate(0deg);}100%{transform:translateY(-115vh) rotate(360deg);}}
    .atom{position:fixed;right:22px;bottom:22px;width:96px;height:96px;pointer-events:none;z-index:0;opacity:.7;}
    .atom .nuc{position:absolute;left:50%;top:50%;width:12px;height:12px;margin:-6px;border-radius:50%;
        background:#22D3EE;box-shadow:0 0 18px #22D3EE, 0 0 40px #8B5CF6;}
    .atom .orb{position:absolute;border:1px solid rgba(34,211,238,.45);border-radius:50%;
        animation:qspin linear infinite;}
    .atom .orb::after{content:"";position:absolute;top:-4px;left:50%;width:8px;height:8px;margin-left:-4px;
        border-radius:50%;background:#8B5CF6;box-shadow:0 0 10px #8B5CF6;}
    .atom .o1{inset:0;animation-duration:3s;}
    .atom .o2{inset:14px;animation-duration:2s;animation-direction:reverse;}
    .atom .o3{inset:28px;animation-duration:1.3s;}
    @keyframes qspin{to{transform:rotate(360deg);}}
    </style>
    """
    atom = ('<div class="atom"><div class="orb o1"></div><div class="orb o2"></div>'
            '<div class="orb o3"></div><div class="nuc"></div></div>')
    html = css + f'<div class="qbg">{items}</div>' + atom
    # Remove indentation so Streamlit doesn't treat the HTML as a code block
    html = " ".join(line.strip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


quantum_theme()

PAIRS = [(0, 0), (0, 1), (1, 0), (1, 1)]

st.title("⚛️ Beat the Quantum")
st.caption("Can you out-strategize entanglement?")
st.write("Alice and Bob can't talk. Each gets a secret bit (0 or 1) and answers with a bit. "
         "They win if their answers **differ only when both inputs are 1**.")

mode = st.radio("Mode", ["classical", "quantum"], horizontal=True)


@st.cache_resource
def get_pool():
    with open("pool.json") as f:
        raw = json.load(f)
    return {(int(k[0]), int(k[1])): [tuple(p) for p in v] for k, v in raw.items()}


def reset():
    st.session_state.wins = 0
    st.session_state.rounds = 0
    st.session_state.history = []
    st.session_state.pair_wins = {p: 0 for p in PAIRS}
    st.session_state.pair_rounds = {p: 0 for p in PAIRS}


if "wins" not in st.session_state:
    reset()

if st.session_state.get("last_mode") != mode:
    reset()
    st.session_state.last_mode = mode

a0 = a1 = b0 = b1 = 0
if mode == "classical":
    st.write("**Design the best classical strategy you can.** Each player answers using only their own input.")
    c = st.columns(4)
    a0 = c[0].selectbox("Alice, input 0", [0, 1], key="a0")
    a1 = c[1].selectbox("Alice, input 1", [0, 1], key="a1")
    b0 = c[2].selectbox("Bob, input 0", [0, 1], key="b0")
    b1 = c[3].selectbox("Bob, input 1", [0, 1], key="b1")
else:
    st.info("Alice and Bob now share an **entangled Bell pair**. Each measures their qubit "
            "at an angle set by their input.")
    st.code("q0: ─ H ─■─ Ry(Alice's angle) ─ Measure\n"
            "q1: ───── X ─ Ry(Bob's angle)   ─ Measure", language=None)


def get_round(x, y):
    if mode == "quantum":
        return random.choice(get_pool()[(x, y)])
    return (a0, a1)[x], (b0, b1)[y]


def record(x, y, a, b):
    win = int((a ^ b) == (x & y))
    st.session_state.rounds += 1
    st.session_state.wins += win
    st.session_state.pair_rounds[(x, y)] += 1
    st.session_state.pair_wins[(x, y)] += win
    st.session_state.history.append(st.session_state.wins / st.session_state.rounds)
    return win


col1, col2, col3 = st.columns(3)
one = col1.button("Play 1 round")
many = col2.button("Auto-play 200")
col3.button("Reset", on_click=reset)

if one:
    x, y = random.randint(0, 1), random.randint(0, 1)
    a, b = get_round(x, y)
    win = record(x, y, a, b)
    st.write(f"Alice got **{x}** and answered **{a}**. Bob got **{y}** and answered **{b}**. "
             f"{'✅ Win' if win else '❌ Loss'}")

if many:
    for _ in range(200):
        x, y = random.randint(0, 1), random.randint(0, 1)
        a, b = get_round(x, y)
        record(x, y, a, b)

if st.session_state.rounds:
    rate = st.session_state.wins / st.session_state.rounds
    st.metric("Win rate", f"{rate:.1%}", f"{(rate - 0.75):+.1%} vs classical limit")

    if mode == "quantum" and st.session_state.rounds >= 200 and rate > 0.78:
        st.success("Past the classical limit. No pre-agreed strategy can do this. That's entanglement.")
        if many:
            st.balloons()

    df = pd.DataFrame({
        "Your win rate": st.session_state.history,
        "Classical limit (75%)": 0.75,
        "Quantum max (85.4%)": 0.854,
    })
    st.line_chart(df)

    st.write("**Win rate by input pair**")
    pr, pw = st.session_state.pair_rounds, st.session_state.pair_wins
    bars = pd.DataFrame({
        "Input pair": [f"x={x}, y={y}" for x, y in PAIRS],
        "Win rate": [pw[p] / pr[p] if pr[p] else 0 for p in PAIRS],
    }).set_index("Input pair")
    st.bar_chart(bars)

with st.expander("Why can't classical beat 75%?"):
    st.write("Any pre-agreed strategy has to lose at least one of the four input pairs, "
             "so the best it can do is win 3 out of 4. Entangled qubits give correlations "
             "that no pre-agreed strategy can reproduce, which pushes the win rate to about 85.4%.")