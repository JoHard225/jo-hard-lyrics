import streamlit as st
import pandas as pd

# --- CONFIGURATION ---
# Ton lien CSV publié est bien intégré ici avec les guillemets nécessaires
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRoUm3iLuD9tdwMcrux7VsAsND4svsqREL3F2RAGbgSFQMYtHe4OOi7vzB3y6cVQkg3UG-k9RDL7-96/pub?gid=0&single=true&output=csv"

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Jo Hard Lyric Manager Pro", layout="centered")
st.title("🎵 Jo Hard Lyric Manager Pro")

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data(ttl=60)
def charger_donnees():
    return pd.read_csv(SHEET_URL)

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Mon Répertoire"])

if menu == "Mon Répertoire":
    try:
        df = charger_donnees()
        st.metric("Total de chansons", len(df))
        
        # Barre de recherche
        query = st.text_input("🔍 Rechercher par titre ou artiste :")
        
        # Filtrage
        if query:
            filtre = df[df['Titre'].str.contains(query, case=False, na=False) | 
                         df['Artiste'].str.contains(query, case=False, na=False)]
        else:
            filtre = df
        
        if not filtre.empty:
            choix = st.selectbox("Choisir une chanson :", filtre['Titre'].tolist())
            chanson = filtre[filtre['Titre'] == choix].iloc[0]
            
            st.markdown(f"## {chanson['Titre']}")
            st.write(f"**Artiste :** {chanson['Artiste']}")
            st.write(f"**Genre :** {chanson['Genre']}")
            st.markdown("---")
            st.write(chanson['Paroles'])
        else:
            st.warning("Aucune chanson trouvée.")
            
    except Exception as e:
        st.error("Erreur de chargement. Vérifie que ton Google Sheet est bien publié en format CSV.")
