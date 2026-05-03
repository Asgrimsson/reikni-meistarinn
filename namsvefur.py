import streamlit as st
import random
import time

# --- UPPSETNING ---
st.set_page_config(page_title="Talna-Bardaginn", page_icon="⚔️", layout="wide")

# CSS stíll til að gera þetta flottara
st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E1E;
        color: white;
    }
    .big-font {
        font-size: 100px !important;
        font-weight: bold;
        text-align: center;
        color: #00FFCC;
        text-shadow: 2px 2px 10px #00FFCC;
        margin-bottom: 0px;
    }
    .score-box {
        background-color: #333333;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #00FFCC;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Geyma gögn
if 'stig' not in st.session_state: st.session_state.stig = 0
if 'combo' not in st.session_state: st.session_state.combo = 0
if 'num1' not in st.session_state:
    st.session_state.num1 = random.randint(2, 10)
    st.session_state.num2 = random.randint(2, 10)

# --- LEIKJA-KERFIÐ ---
def fa_mynd_og_titil(stig):
    if stig < 10:
        return "🌱 Byrjandi", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3A1dGV4Ymd6NWg5Nms3Z3R4ZzRxeGZ6ZzRxeGZ6ZzRxeGZ6ZzRxeGZ6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKSjP6S7FhC3E64/giphy.gif"
    elif stig < 30:
        return "⚔️ Riddari", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXF4ZzRyeGZ6ZzRxeGZ6ZzRxeGZ6ZzRxeGZ6ZzRxeGZ6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l41lTfuxmQY2P5sZO/giphy.gif"
    else:
        return "🧙 Galdramaður", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueXF4ZzRyeGZ6ZzRxeGZ6ZzRxeGZ6ZzRxeGZ6ZzRxeGZ6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpx6v4H6H5Sw/giphy.gif"

titill, mynd_url = fa_mynd_og_titil(st.session_state.stig)

# --- HLIÐARSTIKA (Stillingar) ---
with st.sidebar:
    st.title("⚙️ Stillingar")
    aogerð_val = st.selectbox("Veldu reikniaðgerð:", ["×", "÷", "+", "-"])
    
    # Hér er sleðinn þinn!
    max_tala = st.select_slider(
        "Hversu þung dæmi?", 
        options=[10, 20, 50, 100], 
        value=10,
        help="Þetta stillir hæstu mögulegu tölu í dæmunum."
    )
    
    st.divider()
    if st.button("Endurræsa stig"):
        st.session_state.stig = 0
        st.session_state.combo = 0
        st.rerun()

# --- VIÐMÓT ---
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown(f"<div class='score-box'><h3>{titill}</h3><img src='{mynd_url}' width='100%'></div>", unsafe_allow_html=True)
    st.metric("Heildarstig", st.session_state.stig)

with col2:
    n1, n2 = st.session_state.num1, st.session_state.num2
    st.markdown(f"<p class='big-font'>{n1} {aogerð_val} {n2}</p>", unsafe_allow_html=True)

    with st.form(key='leikja_form', clear_on_submit=True):
        svar = st.number_input("Svarið þitt:", value=None, step=1)
        submit = st.form_submit_button("SENDA SVAR! 🚀")

    if submit:
        # Reikna rétt svar sem heiltölu
        if aogerð_val == "×": rett = n1 * n2
        elif aogerð_val == "÷": rett = n1 // n2
        elif aogerð_val == "+": rett = n1 + n2
        elif aogerð_val == "-": rett = n1 - n2

        if svar == rett:
            st.session_state.stig += (1 + st.session_state.combo)
            st.session_state.combo += 1
            st.toast("RÉTT! 🔥", icon="✅")
            
            # Búa til nýjar tölur miðað við stillingu á sleða
            if aogerð_val == "÷":
                st.session_state.num2 = random.randint(2, max_tala // 2 if max_tala > 4 else 2)
                st.session_state.num1 = st.session_state.num2 * random.randint(1, 10)
            elif aogerð_val == "-":
                st.session_state.num1 = random.randint(2, max_tala)
                st.session_state.num2 = random.randint(2, st.session_state.num1) # Forðast mínustölur
            else:
                st.session_state.num1 = random.randint(2, max_tala)
                st.session_state.num2 = random.randint(2, max_tala)
            
            time.sleep(0.3)
            st.rerun()
        else:
            st.error(f"Vitlaust! Rétt svar var {rett}")
            st.session_state.combo = 0
            time.sleep(1.2)
            st.rerun()

with col3:
    if st.session_state.combo > 0:
        st.markdown(f"<div style='text-align:center;'><h2>COMBO</h2><h1 style='color:orange; font-size:60px;'>{st.session_state.combo}x</h1></div>", unsafe_allow_html=True)
        if st.session_state.combo % 5 == 0:
            st.balloons()

# --- FRAMVINDAN ---
progress_val = min((st.session_state.stig % 20) / 20, 1.0)
st.progress(progress_val, text=f"Framvinda á næsta stig: {int(progress_val*100)}%")
