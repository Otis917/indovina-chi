import streamlit as st
from PIL import Image, ImageEnhance
import random
import os

# --- TRUCCO PER TROVARE SEMPRE LA CARTELLA ---
# Questo trova la cartella dovunque si trovi il file app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMMAGINI_DIR = os.path.join(BASE_DIR, "immagini")

# --- DEBUG ---
# Se l'errore persiste, questo ti dirà a video dove sta cercando
if not os.path.exists(IMMAGINI_DIR):
    st.error(f"❌ ERRORE: Non trovo la cartella in questo percorso: {IMMAGINI_DIR}")
    st.write("📂 Contenuto della cartella attuale:", os.listdir(BASE_DIR))
    st.stop() # Ferma tutto se manca la cartella

# --- FUNZIONE CARICAMENTO AGGIORNATA ---
def carica_immagine(nome, oscurato):
    img = None
    estensioni = [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]
    
    for ext in estensioni:
        # Usa il percorso assoluto calcolato prima
        percorso = os.path.join(IMMAGINI_DIR, f"{nome}{ext}")
        if os.path.exists(percorso):
            try:
                img = Image.open(percorso).convert("RGB")
                break
            except:
                continue
    
    if img is None:
        return Image.new('RGB', (200, 200), color=(50, 50, 50)) # Grigio se manca

    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    
    if oscurato:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.2)
        
    return img
