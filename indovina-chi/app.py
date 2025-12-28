import streamlit as st
from PIL import Image, ImageEnhance
import random

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Indovina Chi? 2025", layout="wide")

# Personalizzazione CSS per il tema scuro e lo stile dei box
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .stButton>button { width: 100%; border-radius: 10px; border: none; }
    .char-label { text-align: center; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAZIONE GIOCO ---
PERSONAGGI = ["Ai Hayasaka", "Amo", "Nagi Arato", "Ouguri Cup"]
COLONNE = 2  # Su cellulare 2 colonne sono meglio di 4

# --- INIZIALIZZAZIONE STATO ---
if 'segreto' not in st.session_state:
    st.session_state.segreto = random.choice(PERSONAGGI)
if 'oscurati' not in st.session_state:
    st.session_state.oscurati = {nome: False for nome in PERSONAGGI}

def reset_gioco():
    st.session_state.segreto = random.choice(PERSONAGGI)
    st.session_state.oscurati = {nome: False for nome in PERSONAGGI}

# --- LOGICA IMMAGINI ---
def get_immagine(nome, oscurato):
    path = f"immagini/{nome}.jpg" # Assicurati che le estensioni coincidano
    try:
        img = Image.open(path).convert("RGB")
        if oscurato:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.2) # Molto scuro
        return img
    except:
        # Placeholder se l'immagine manca
        return Image.new('RGB', (300, 300), color = (100, 100, 100))

# --- UI INTERFACCIA ---
st.title("🕵️ Indovina Chi?")
st.subheader(f"Il tuo personaggio segreto è: :blue[{st.session_state.segreto.upper()}]")

# Griglia Personaggi
cols = st.columns(COLONNE)

for i, nome in enumerate(PERSONAGGI):
    col_idx = i % COLONNE
    with cols[col_idx]:
        # Carica l'immagine in base allo stato
        is_dark = st.session_state.oscurati[nome]
        img_display = get_immagine(nome, is_dark)
        
        st.image(img_display, use_container_width=True)
        
        # Bottone per alternare lo stato
        label = f"✅ Attivo: {nome}" if not is_dark else f"❌ Escluso: {nome}"
        if st.button(label, key=nome):
            st.session_state.oscurati[nome] = not st.session_state.oscurati[nome]
            st.rerun()

st.divider()

# Bottone Reset
if st.button("🔄 NUOVA PARTITA / RESET", use_container_width=True, type="primary"):
    reset_gioco()
    st.rerun()