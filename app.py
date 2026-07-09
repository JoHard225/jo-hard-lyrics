import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fpdf import FPDF
import requests

# --- CONFIGURATION (À MODIFIER) ---
SHEET_URL = https://docs.google.com/spreadsheets/d/1vK-7F-meD-OK0ejFORCi-YOhdJ3KdIosAG9BDXetEPE/edit?gid=0#gid=0

# --- CONFIGURATION DES PAGES ---
st.set_page_config(page_title="Jo Hard Lyric Manager Pro", layout="centered")
st.title("🎵 Jo Hard Lyric Manager Pro")

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Recherche Web", "Mon Répertoire"])

# --- FONCTION POUR LIRE/ÉCRIRE ---
# (Note : Pour une utilisation réelle sur Streamlit Cloud, il faut charger tes identifiants via 'Secrets' dans Streamlit)
# Pour simplifier, nous allons utiliser Pandas pour lire les données du CSV publié
def charger_donnees():
    # Astuce : publie ton Google Sheet en CSV (Fichier > Partager > Publier sur le Web > CSV)
    csv_url = SHEET_URL.replace('/edit#gid=', '/export?format=csv&gid=')
    return pd.read_csv(csv_url)

# --- SECTION RÉPERTOIRE ---
if menu == "Mon Répertoire":
    df = charger_donnees()
    st.metric("Total", len(df))
    
    query = st.text_input("🔍 Rechercher :")
    if query:
        df = df[df['Titre'].str.contains(query, case=False) | df['Artiste'].str.contains(query, case=False)]
    
    choix = st.selectbox("Choisir une chanson :", df['Titre'].tolist())
    chanson = df[df['Titre'] == choix].iloc[0]
    
    st.write(f"## {chanson['Titre']}")
    st.write(f"**Artiste :** {chanson['Artiste']}")
    st.write(chanson['Paroles'])
               
