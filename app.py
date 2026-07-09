import streamlit as st
import pandas as pd
import requests

# --- CONFIGURATION ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRoUm3iLuD9tdwMcrux7VsAsND4svsqREL3F2RAGbgSFQMYtHe4OOi7vzB3y6cVQkg3UG-k9RDL7-96/pub?gid=0&single=true&output=csv"

st.set_page_config(page_title="Jo Hard Lyric Manager Pro", layout="centered")
st.title("🎵 Jo Hard Lyric Manager Pro")

# --- CHARGEMENT DONNÉES GOOGLE SHEET ---
@st.cache_data(ttl=60)
def charger_donnees():
    return pd.read_csv(SHEET_URL)

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Mon Répertoire", "Recherche Web"])

# --- SECTION : RÉPERTOIRE ---
if menu == "Mon Répertoire":
    try:
        df = charger_donnees()
        st.metric("Total de chansons", len(df))
        
        query = st.text_input("🔍 Rechercher :")
        if query:
            df = df[df['Titre'].str.contains(query, case=False, na=False) | 
                    df['Artiste'].str.contains(query, case=False, na=False)]
        
        if not df.empty:
            choix = st.selectbox("Choisir une chanson :", df['Titre'].tolist())
            chanson = df[df['Titre'] == choix].iloc[0]
            st.markdown(f"## {chanson['Titre']}")
            st.write(f"**Artiste :** {chanson['Artiste']}")
            st.write(f"**Genre :** {chanson['Genre']}")
            st.markdown("---")
            st.write(chanson['Paroles'])
        else:
            st.warning("Aucune chanson trouvée.")
    except Exception as e:
        st.error("Erreur de chargement. Vérifie ton lien Google Sheet.")

# --- SECTION : RECHERCHE WEB ---
elif menu == "Recherche Web":
    st.subheader("🌐 Rechercher des paroles")
    artist = st.text_input("Artiste")
    title = st.text_input("Titre")
    
    if st.button("Chercher"):
        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        response = requests.get(url)
        if response.status_code == 200:
            lyrics = response.json().get('lyrics')
            st.text_area("Paroles trouvées :", value=lyrics, height=300)
            st.info("Tu peux copier ces paroles pour les ajouter à ton Google Sheet !")
        else:
            st.error("Paroles non trouvées.")
