import streamlit as st
from PIL import Image, ImageEnhance
import random
import os
from functools import lru_cache
import time

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
if 'ultimo_click' not in st.session_state:  # Per rate limiter
    st.session_state.ultimo_click = 0

# 5. Cache per le immagini
@st.cache_data(ttl=3600)  # Cache per 1 ora
def ottieni_immagine_cached(nome, oscurato, cartella):
    """Versione cached della funzione per ottenere immagini"""
    img = None
    estensioni = [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]
    percorso_cartella = os.path.join(BASE_DIR, cartella)
    
    # Prima prova con il nome esatto
    for ext in estensioni:
        path = os.path.join(percorso_cartella, f"{nome}{ext}")
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                break
            except:
                continue
    
    # Fallback: immagine grigia
    if img is None:
        img = Image.new('RGB', (300, 300), color=(70, 70, 70))
    
    img = img.resize((300, 300))
    
    if oscurato:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.2)
    
    return img

# 6. Pre-caricamento delle immagini
@st.cache_resource
def preload_all_images():
    """Pre-carica tutte le immagini possibili"""
    cartelle = ["immagini_1", "immagini_2"]
    tutte_immagini = {}
    
    for cartella in cartelle:
        percorso_cartella = os.path.join(BASE_DIR, cartella)
        if not os.path.exists(percorso_cartella):
            continue
            
        # Determina quale lista di personaggi usare
        lista_personaggi = PERSONAGGI_1 if cartella == "immagini_1" else PERSONAGGI_2
        
        for nome in lista_personaggi:
            # Carica versione chiara e scura
            try:
                img_chiara = ottieni_immagine_cached(nome, False, cartella)
                img_scura = ottieni_immagine_cached(nome, True, cartella)
                tutte_immagini[f"{cartella}/{nome}/chiara"] = img_chiara
                tutte_immagini[f"{cartella}/{nome}/scura"] = img_scura
            except Exception as e:
                continue
                
    return tutte_immagini

# 7. Callback per toggle personaggio con rate limiter
def toggle_personaggio(nome):
    """Callback per alternare oscuramento personaggio con rate limiting"""
    tempo_attuale = time.time()
    
    # Rate limiter: 0.5 secondi tra i click
    if tempo_attuale - st.session_state.ultimo_click < 0.5:
        st.warning("⏳ Troppi click rapidi! Aspetta un attimo.")
        return
    
    st.session_state.ultimo_click = tempo_attuale
    st.session_state.oscurati[nome] = not st.session_state.oscurati.get(nome, False)

# 8. Funzione per ottenere immagine (usa cache e preload)
def ottieni_immagine(nome, oscurato, cartella):
    """Funzione principale per ottenere immagini (usa cache)"""
    return ottieni_immagine_cached(nome, oscurato, cartella)

# Pre-carica le immagini all'avvio (viene eseguito una volta)
preload_all_images()

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
            st.session_state.ultimo_click = 0
            st.rerun()
            
    with col_b:
        if st.button("📂 GIOCA CON TABELLA 2", use_container_width=True):
            st.session_state.tabella_selezionata = "immagini_2"
            st.session_state.lista_attuale = PERSONAGGI_2
            st.session_state.segreto = random.choice(PERSONAGGI_2)
            st.session_state.oscurati = {n: False for n in PERSONAGGI_2}
            st.session_state.ultimo_click = 0
            st.rerun()

# SCHERMATA DI GIOCO
else:
    st.title(f"🕵️ Indovina Chi?")
    st.caption(f"Stai usando la cartella: {st.session_state.tabella_selezionata}")
    
    st.write(f"Il tuo personaggio segreto: **{st.session_state.segreto}**")
    
    # Contatore personaggi oscurati
    oscurati_count = sum(st.session_state.oscurati.values())
    st.write(f"Personaggi oscurati: {oscurati_count}/{len(st.session_state.lista_attuale)}")

    # --- Griglia a 3 colonne ---
    N_COLONNE = 3 
    rows = [st.session_state.lista_attuale[i:i + N_COLONNE] for i in range(0, len(st.session_state.lista_attuale), N_COLONNE)]
    
    for row in rows:
        cols = st.columns(N_COLONNE)
        for i, nome in enumerate(row):
            with cols[i]:
                is_dark = st.session_state.oscurati.get(nome, False)
                img = ottieni_immagine(nome, is_dark, st.session_state.tabella_selezionata)
                
                st.image(img, use_container_width=True)
                
                label = nome if not is_dark else f"❌ {nome}"
                
                # Bottone con callback e rate limiter integrato
                st.button(
                    label, 
                    key=f"btn_{nome}", 
                    use_container_width=True,
                    on_click=toggle_personaggio,
                    args=(nome,),
                    type="secondary" if is_dark else "primary"
                )

    st.divider()
    
    col_reset, col_back = st.columns(2)
    with col_reset:
        if st.button("🔄 RESET PARTITA (Cambia Segreto)", use_container_width=True):
            st.session_state.segreto = random.choice(st.session_state.lista_attuale)
            st.session_state.oscurati = {n: False for n in st.session_state.lista_attuale}
            st.session_state.ultimo_click = 0
            st.rerun()
            
    with col_back:
        if st.button("⬅️ TORNA AL MENU", use_container_width=True):
            # Reset totale per tornare alla scelta iniziale
            st.session_state.tabella_selezionata = None
            st.session_state.lista_attuale = []
            st.session_state.ultimo_click = 0
            st.rerun()
