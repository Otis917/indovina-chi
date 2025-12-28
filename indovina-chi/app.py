import streamlit as st
from PIL import Image, ImageEnhance
import random
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Indovina Chi? 2025", layout="wide")

# CSS per rendere le scritte centrate e gestire lo stile
st.markdown("""
    <style>
    .main { background-color: #121212; }
    div.stButton > button {
        border: none;
        padding: 0px;
        background: transparent;
    }
    .nome-personaggio {
        text-align: center;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAZIONE GIOCO ---
PERSONAGGI = ["Ai Hayasaka", "Amo", "Nagi Arato", "Ouguri Cup"]
COLONNE = 4  # Almeno 4 per riga come richiesto
TARGET_SIZE = (300, 300) # Dimensione fissa per uniformità

# --- INIZIALIZZAZIONE STATO ---
if 'segreto' not in st.session_state:
    st.session_state.segreto = random.choice(PERSONAGGI)
if 'oscurati' not in st.session_state:
    st.session_state.oscurati = {nome: False for nome in PERSONAGGI}

def reset_gioco():
    st.session_state.segreto = random.choice(PERSONAGGI)
    st.session_state.oscurati = {nome: False for nome in PERSONAGGI}

# --- LOGICA IMMAGINI (CON CONTROLLO ESTENSIONI) ---
def get_immagine(nome, oscurato):
    img = None
    # Prova diverse estensioni come nel tuo codice originale
    for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG"]:
        path = f"immagini/{nome}{ext}"
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                break
            except:
                continue
    
    if img:
        # Forza la dimensione uguale per tutti
        img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        if oscurato:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.3) # Scurisce l'immagine
        return img
    else:
        # Se non trova l'immagine, crea un rettangolo grigio della stessa dimensione
        return Image.new('RGB', TARGET_SIZE, color = (50, 50, 50))

# --- UI INTERFACCIA ---
st.title("🕵️ Indovina Chi?")
st.subheader(f"Il tuo personaggio segreto è: :orange[{st.session_state.segreto.upper()}]")

# Griglia Personaggi
cols = st.columns(COLONNE)

for i, nome in enumerate(PERSONAGGI):
    col_idx = i % COLONNE
    with cols[col_idx]:
        is_dark = st.session_state.oscurati[nome]
        img_display = get_immagine(nome, is_dark)
        
        # Mostra l'immagine. In Streamlit, per rendere cliccabile 
        # l'immagine usiamo il parametro 'on_click' di un button che la contiene
        # o usiamo un button subito sotto che funge da interruttore
        st.image(img_display, use_container_width=True)
        
        # Colore del nome: se oscurato diventa grigio scuro
        nome_colore = "#444" if is_dark else "#FFF"
        st.markdown(f'<p class="nome-personaggio" style="color: {nome_colore};">{nome.upper()}</p>', unsafe_allow_html=True)
        
        # Bottone invisibile o piccolo per gestire il click
        label_btn = "RIPRISTINA" if is_dark else "ELIMINA"
        if st.button(label_btn, key=f"btn_{nome}", use_container_width=True):
            st.session_state.oscurati[nome] = not st.session_state.oscurati[nome]
            st.rerun()

st.divider()

if st.button("🔄 NUOVA PARTITA / RESET", use_container_width=True, type="primary"):
    reset_gioco()
    st.rerun()
