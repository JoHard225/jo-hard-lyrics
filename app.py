import streamlit as st
import pandas as pd
import requests

# --- CONFIGURATION ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRoUm3iLuD9tdwMcrux7VsAsND4svsqREL3F2RAGbgSFQMYtHe4OOi7vzB3y6cVQkg3UG-k9RDL7-96/pub?gid=0&single=true&output=csv"

st.set_page_config(page_title="Jo Hard Lyric Manager Pro", layout="centered")
st.title("🎵 Jo Hard Lyric Manager Pro")

# --- CHARGEMENT DONNÉES ---
@st.cache_data(ttl=60)
def charger_donnees():
    return pd.read_csv(SHEET_URL)

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Mon Répertoire", "Playlist Perso", "Recherche Web"])

# --- SECTION : RÉPERTOIRE ---
if menu == "Mon Répertoire":
    df = charger_donnees()
    st.metric("Chansons disponibles", len(df))
    query = st.text_input("🔍 Rechercher :")
    if query:
        df = df[df['Titre'].str.contains(query, case=False, na=False) | df['Artiste'].str.contains(query, case=False, na=False)]
    
    if not df.empty:
        choix = st.selectbox("Choisir une chanson :", df['Titre'].tolist())
        chanson = df[df['Titre'] == choix].iloc[0]
        st.write(f"## {chanson['Titre']} - {chanson['Artiste']}")
        st.write(f"**Genre :** {chanson['Genre']}")
        st.markdown("---")
        st.write(chanson['Paroles'])
    else:
        st.warning("Aucune chanson trouvée.")

# --- SECTION : PLAYLIST PERSO ---
elif menu == "Playlist Perso":
    st.subheader("🎸 Ma Setlist de concert")
    df = charger_donnees()
    selection = st.multiselect("Ajoute tes titres pour le concert :", df['Titre'].tolist())
    
    if selection:
        st.write("### Ordre de passage :")
        for i, titre in enumerate(selection, 1):
            st.write(f"{i}. {titre}")
        if st.button("Afficher les paroles du set"):
            for titre in selection:
                chanson = df[df['Titre'] == titre].iloc[0]
                st.markdown(f"---")
                st.write(f"### {chanson['Titre']}")
                st.write(chanson['Paroles'])

# --- SECTION : RECHERCHE WEB ---
elif menu == "Recherche Web":
    st.subheader("🌐 Recherche externe")
    artist = st.text_input("Artiste")
    title = st.text_input("Titre")
    if st.button("Chercher"):
        response = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{title}")
        if response.status_code == 200:
            st.text_area("Résultat :", value=response.json().get('lyrics'), height=300)
            st.success("Copie ces paroles dans ton Google Sheet pour les enregistrer !")
        else:
            st.error("Paroles non trouvées.")
