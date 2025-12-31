import streamlit as st
from PIL import Image, ImageEnhance
import random
import os

# 1. Configurazione
st.set_page_config(page_title="Indovina Chi?", layout="wide")

# 2. Percorsi Base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 3. Definizione delle due liste separate
PERSONAGGI_1 = ["Anya Forger", "Trap Davi Goth Culone", "Clara (disabile nemica della Greta)", 
    "Tette Nami", "Oikawa Tooru", "AlexCelsus", "Corgi", "Tette Alya", 
    "Ciuchino", "Ouguri Cup", "François", "Tom the Blowjob Fish", 
    "Donna Sborra", "Rathalos", "Lilo, Stitch e Romolo", "Kafka", 
    "Tette Marin", "Onizuka", "Bulma", "Donna Bocchino", "Rigby", 
    "Pumpkin Muffin", "Nico Gattina", "Akira"]
PERSONAGGI_2 = ["Rize", "Josuke Higashikata", "Ai Hayasaka", "Parpaïa", 
    "Sheldon Cooper", "Tette Rias", "Annabeth Chase (ariana)", "Amo", 
    "Poivrons (gormiti)", "Shinji", "Chika Fujiwara", "Dee-Dee", 
    "Spider Man", "Stella", "Yoshi", "il creatore di via de guinceri", 
    "Cersei Lannister", "Kronk", "Pallino", "Appletun", 
    "Roxas", "Pickle Rick", "Piedino", "Trap Elly Cordless"]

# 4. Inizializzazione Sessione
if 'tabella_selezionata' not in st.session_state:
    st.session_state.tabella_selezionata = None
if 'lista_attuale' not in st.session_state:
    st.session_state.lista_attuale = []
if 'segreto' not in st.session_state:
    st.session_state.segreto = None
if 'oscurati' not in st.session_state:
    st.session_state.oscurati = {}

# 5. Funzione Caricamento Immagine
def ottieni_immagine(nome, oscurato, cartella):
    img = None
    estensioni = [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]
    percorso_cartella = os.path.join(BASE_DIR, cartella)
    
    for ext in estensioni:
        path = os.path.join(percorso_cartella, f"{nome}{ext}")
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                break
            except:
                continue
    
    if img is None:
        img = Image.new('RGB', (300, 300), color=(70, 70, 70))
    
    img = img.resize((300, 300))
    
    if oscurato:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.2)
    return img

# --- LOGICA DI NAVIGAZIONE ---

# SCHERMATA DI INIZIO
if st.session_state.tabella_selezionata is None:
    st.title("🕵️ Benvenuto a Indovina Chi?")
    st.subheader("Seleziona la tabella con cui vuoi giocare:")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("📂 GIOCA CON TABELLA 1", use_container_width=True):
            st.session_state.tabella_selezionata = "immagini_1"
            st.session_state.lista_attuale = PERSONAGGI_1
            st.session_state.segreto = random.choice(PERSONAGGI_1)
            st.session_state.oscurati = {n: False for n in PERSONAGGI_1}
            st.rerun()
            
    with col_b:
        if st.button("📂 GIOCA CON TABELLA 2", use_container_width=True):
            st.session_state.tabella_selezionata = "immagini_2"
            st.session_state.lista_attuale = PERSONAGGI_2
            st.session_state.segreto = random.choice(PERSONAGGI_2)
            st.session_state.oscurati = {n: False for n in PERSONAGGI_2}
            st.rerun()

# SCHERMATA DI GIOCO
else:
    st.title(f"🕵️ Indovina Chi?")
    st.caption(f"Stai usando la cartella: {st.session_state.tabella_selezionata}")
    
    st.write(f"Il tuo personaggio segreto: **{st.session_state.segreto}**")

    # --- MODIFICA PER MOBILE: Griglia a 3 colonne (o 2 se preferisci più grandi) ---
    N_COLONNE = 3 
    rows = [st.session_state.lista_attuale[i:i + N_COLONNE] for i in range(0, len(st.session_state.lista_attuale), N_COLONNE)]
    
    for row in rows:
        cols = st.columns(N_COLONNE)
        for i, nome in enumerate(row):
            with cols[i]:
                is_dark = st.session_state.oscurati.get(nome, False)
                img = ottieni_immagine(nome, is_dark, st.session_state.tabella_selezionata)
                
                st.image(img, use_container_width=True)
                
                label = nome if not is_dark else f"❌" # Testo corto per non rompere il layout
                if st.button(label, key=f"btn_{nome}", use_container_width=True):
                    st.session_state.oscurati[nome] = not st.session_state.oscurati[nome]
                    st.rerun()

    st.divider()
    
    col_reset, col_back = st.columns(2)
    with col_reset:
        if st.button("🔄 RESET PARTITA (Cambia Segreto)", use_container_width=True):
            st.session_state.segreto = random.choice(st.session_state.lista_attuale)
            st.session_state.oscurati = {n: False for n in st.session_state.lista_attuale}
            st.rerun()
            
    with col_back:
        if st.button("⬅️ TORNA AL MENU", use_container_width=True):
            # Reset totale per tornare alla scelta iniziale
            st.session_state.tabella_selezionata = None
            st.session_state.lista_attuale = []

            st.rerun()

