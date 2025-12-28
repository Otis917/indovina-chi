import streamlit as st
from PIL import Image, ImageEnhance
import random
import os

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Indovina Chi?", layout="wide")

# CSS per avvicinare immagine e bottone e centrare tutto
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        margin-top: -10px; /* Avvicina il bottone all'immagine */
        font-weight: bold;
    }
    img {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONFIGURAZIONE DATI ---
# ATTENZIONE: I nomi qui devono essere IDENTICI ai nomi dei file (senza .jpg)
PERSONAGGI = ["Ai Hayasaka", "Amo", "Nagi Arato", "Ouguri Cup"]
COLONNE = 4  # 4 Immagini per riga
DIMENSIONE_IMG = (200, 200) # Rimpicciolite e quadrate

# --- 3. INIZIALIZZAZIONE MEMORIA ---
if 'segreto' not in st.session_state:
    st.session_state.segreto = random.choice(PERSONAGGI)
if 'oscurati' not in st.session_state:
    st.session_state.oscurati = {nome: False for nome in PERSONAGGI}

def reset_gioco():
    st.session_state.segreto = random.choice(PERSONAGGI)
    st.session_state.oscurati = {nome: False for nome in PERSONAGGI}

# --- 4. FUNZIONE CARICAMENTO IMMAGINI ---
def carica_immagine(nome, oscurato):
    # Cerca l'immagine con varie estensioni
    trovata = False
    img = None
    
    # Lista estensioni possibili
    estensioni = [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]
    
    for ext in estensioni:
        percorso = f"immagini/{nome}{ext}"
        if os.path.exists(percorso):
            try:
                img = Image.open(percorso).convert("RGB")
                trovata = True
                break
            except:
                continue
    
    # Se non trova l'immagine, crea un quadrato colorato con il nome dentro
    if not trovata:
        return None 

    # Ridimensiona per averle tutte uguali
    img = img.resize(DIMENSIONE_IMG, Image.Resampling.LANCZOS)
    
    # Se deve essere scura
    if oscurato:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.2) # Molto scura (20% luminosità)
        
    return img

# --- 5. INTERFACCIA ---
st.title("🕵️ Indovina Chi?")

# Controllo se la cartella esiste (DEBUG)
if not os.path.exists("immagini"):
    st.error("⚠️ ERRORE GRAVE: Non trovo la cartella 'immagini'. Assicurati di aver creato una cartella chiamata esattamente 'immagini' (tutto minuscolo) accanto al file app.py")
else:
    # Se la cartella c'è, controlliamo se è vuota
    files = os.listdir("immagini")
    if not files:
        st.warning("⚠️ La cartella 'immagini' è vuota!")

st.markdown(f"### Personaggio Segreto: :orange[{st.session_state.segreto}]")

# Creazione Griglia
cols = st.columns(COLONNE)

for i, nome in enumerate(PERSONAGGI):
    col_idx = i % COLONNE
    with cols[col_idx]:
        
        # Recupera stato
        is_dark = st.session_state.oscurati[nome]
        
        # Recupera Immagine
        img = carica_immagine(nome, is_dark)
        
        if img:
            st.image(img, use_container_width=True)
        else:
            # Messaggio di errore se l'immagine specifica non si trova
            st.error(f"Manca: {nome}")
        
        # IL BOTTONE FUNGE DA CLICK SULL'IMMAGINE
        # Se è normale mostra il nome, se è scuro mostra una X
        testo_bottone = nome if not is_dark else "❌ " + nome
        
        # Se clicchi il bottone, cambi lo stato
        if st.button(testo_bottone, key=nome):
            st.session_state.oscurati[nome] = not st.session_state.oscurati[nome]
            st.rerun()

st.markdown("---")
if st.button("🔄 NUOVA PARTITA", type="primary", use_container_width=True):
    reset_gioco()
    st.rerun()
