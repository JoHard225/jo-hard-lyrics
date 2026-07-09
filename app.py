import streamlit as st
import sqlite3
import pandas as pd
import requests

# --- CONNEXION BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('lyrics_db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lyrics 
                 (titre TEXT, artiste TEXT, genre TEXT, paroles TEXT)''')
    conn.commit()
    conn.close()

init_db()

st.set_page_config(page_title="Jo Hard Lyric Manager Pro", layout="centered")
st.title("🎵 Jo Hard Lyric Manager Pro")

menu = st.sidebar.radio("Navigation", ["Mon Répertoire", "Ajouter / Chercher", "Playlist Perso"])

# --- SECTION RÉPERTOIRE ---
if menu == "Mon Répertoire":
    conn = sqlite3.connect('lyrics_db.db')
    df = pd.read_sql_query("SELECT * FROM lyrics", conn)
    conn.close()
    
    st.metric("Total chansons", len(df))
    if not df.empty:
        choix = st.selectbox("Choisir une chanson :", df['titre'].tolist())
        chanson = df[df['titre'] == choix].iloc[0]
        st.write(f"## {chanson['titre']} - {chanson['artiste']}")
        st.write(f"**Genre :** {chanson['genre']}")
        st.write(chanson['paroles'])
        if st.button("Supprimer"):
            conn = sqlite3.connect('lyrics_db.db')
            conn.execute("DELETE FROM lyrics WHERE titre = ?", (chanson['titre'],))
            conn.commit()
            conn.close()
            st.rerun()

# --- SECTION AJOUT / RECHERCHE ---
elif menu == "Ajouter / Chercher":
    st.subheader("🌐 Chercher ou Ajouter")
    art = st.text_input("Artiste")
    tit = st.text_input("Titre")
    
    if st.button("Rechercher sur le Web"):
        res = requests.get(f"https://api.lyrics.ovh/v1/{art}/{tit}")
        if res.status_code == 200:
            st.session_state.temp_lyrics = res.json().get('lyrics')
        else:
            st.error("Non trouvé")

    # Formulaire d'enregistrement direct
    with st.form("ajout"):
        t = st.text_input("Titre", value=tit)
        a = st.text_input("Artiste", value=art)
        g = st.selectbox("Genre", ["Rock", "Pop", "Jazz", "Autre"])
        p = st.text_area("Paroles", value=st.session_state.get('temp_lyrics', ''))
        if st.form_submit_button("Enregistrer dans mon app"):
            conn = sqlite3.connect('lyrics_db.db')
            conn.execute("INSERT INTO lyrics VALUES (?,?,?,?)", (t, a, g, p))
            conn.commit()
            conn.close()
            st.success("Enregistré !")

# --- SECTION PLAYLIST ---
elif menu == "Playlist Perso":
    st.subheader("🎸 Ma Setlist")
    # (Logique de playlist identique à avant...)
