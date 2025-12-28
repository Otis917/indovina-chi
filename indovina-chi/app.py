import streamlit as st
from PIL import Image, ImageEnhance
import random
import os

# 1. Configurazione minima per stabilità
st.set_page_config(page_title="Indovina Chi?", layout="wide")

# 2. Percorsi e Verifica Cartella
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMMAGINI_DIR = os.path.join(BASE_DIR, "immagini")

# Se la cartella immagini non esiste, la crea (evita il crash)
if not os.path.exists(IMMAGINI_DIR):
    os.makedirs(IMMAGINI_DIR)

# 3. Dati
PERSONAGGI = ["Ai Hayasaka", "Amo", "Nagi Arato", "Ouguri Cup"]

# 4. Inizializzazione Sessione
if 'segreto' not in st.session_state:
    st.session_state.segreto = random.choice(PERSONAGGI)
if 'oscurati' not in st.session_state:
    st.session_state.oscurati = {n: False for n in PERSONAGGI}

# 5. Funzione Caricamento
def ottieni_immagine(nome, oscurato):
    img = None
    estensioni = [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]
    
    for ext in estensioni:
        path = os.path.join(IMMAGINI_DIR, f"{nome}{ext}")
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                break
            except:
                continue
    
    if img is None:
        # Crea un quadrato grigio se la foto manca
        img = Image.new('RGB', (300, 300), color=(70, 70, 70))
    
    img = img.resize((300, 300))
    
    if oscurato:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.2)
    return img

# 6. Interfaccia
st.title("🕵️ Indovina Chi?")
st.write(f"Il tuo personaggio: **{st.session_state.segreto}**")

# Griglia a 4 colonne
cols = st.columns(4)

for i, nome in enumerate(PERSONAGGI):
    with cols[i % 4]:
        is_dark = st.session_state.oscurati[nome]
        img = ottieni_immagine(nome, is_dark)
        
        # Mostra immagine
        st.image(img, use_container_width=True)
        
        # Bottone (Nome o X se escluso)
        label = nome if not is_dark else f"❌ {nome}"
        if st.button(label, key=f"btn_{nome}"):
            st.session_state.oscurati[nome] = not st.session_state.oscurati[nome]
            st.rerun()

st.divider()
if st.button("RESET"):
    st.session_state.segreto = random.choice(PERSONAGGI)
    st.session_state.oscurati = {n: False for n in PERSONAGGI}
    st.rerun()
