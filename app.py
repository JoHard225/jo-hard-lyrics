import streamlit as st
import json
import os
import requests
from fpdf import FPDF

# --- CONFIGURATION ---
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

st.set_page_config(page_title="Jo Hard Lyric Manager Pro", page_icon="🎵", layout="centered")

# --- TITRE ---
st.title("🎵 Jo Hard Lyric Manager Pro")
st.markdown("---")

# --- NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Ajouter Manuellement", "Recherche Web", "Mon Répertoire", "Playlist Rapide"])

# --- LISTE DES GENRES ---
GENRES = sorted(["Blues", "Gospel", "Jazz", "Autre", "Pop", "Reggae", "Rock", "Soul", "Variété"])

# --- SECTION 1 : AJOUT MANUEL ---
if menu == "Ajouter Manuellement":
    st.subheader("📝 Ajouter une nouvelle chanson")
    titre = st.text_input("Titre")
    artiste = st.text_input("Artiste")
    genre = st.selectbox("Genre musical :", GENRES)
    paroles = st.text_area("Paroles", height=300)
    
    if st.button("Enregistrer"):
        if titre and artiste:
            data = {"titre": titre, "artiste": artiste, "genre": genre, "paroles": paroles}
            with open(os.path.join(DATA_DIR, f"{titre}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            st.success(f"Bravo ! {titre} a été enregistré.")
        else:
            st.error("Le titre et l'artiste sont obligatoires.")

# --- SECTION 2 : RECHERCHE WEB ---
elif menu == "Recherche Web":
    st.subheader("🌐 Rechercher des paroles")
    artist = st.text_input("Artiste")
    title = st.text_input("Titre")
    genre = st.selectbox("Genre musical :", GENRES)
    
    if 'lyrics_found' not in st.session_state:
        st.session_state.lyrics_found = None

    if st.button("Chercher"):
        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        response = requests.get(url)
        if response.status_code == 200:
            st.session_state.lyrics_found = response.json().get('lyrics')
            st.session_state.current_title = title
            st.session_state.current_artist = artist
            st.session_state.current_genre = genre
        else:
            st.error("Paroles non trouvées.")
            st.session_state.lyrics_found = None

    if st.session_state.lyrics_found:
        st.text_area("Paroles trouvées :", value=st.session_state.lyrics_found, height=300)
        if st.button("Sauvegarder cette chanson"):
            data = {
                "titre": st.session_state.current_title, 
                "artiste": st.session_state.current_artist, 
                "genre": st.session_state.current_genre, 
                "paroles": st.session_state.lyrics_found
            }
            with open(os.path.join(DATA_DIR, f"{st.session_state.current_title}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            st.success("Enregistré dans le répertoire !")
            st.session_state.lyrics_found = None

# --- SECTION 3 : RÉPERTOIRE ---
elif menu == "Mon Répertoire":
    fichiers = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    st.metric("Total de chansons", len(fichiers))
    st.subheader("📂 Mes Lyrics")
    
    if fichiers:
        toutes_les_chansons = [json.load(open(os.path.join(DATA_DIR, f), "r", encoding="utf-8")) for f in fichiers]
        
        filtre_genre = st.selectbox("Filtrer par Genre :", ["Tous"] + GENRES)
        if filtre_genre != "Tous":
            toutes_les_chansons = [s for s in toutes_les_chansons if s.get('genre') == filtre_genre]
            
        query = st.text_input("🔍 Rechercher :")
        if query:
            toutes_les_chansons = [s for s in toutes_les_chansons if query.lower() in s['titre'].lower() or query.lower() in s['artiste'].lower()]
        
        if toutes_les_chansons:
            choix = st.selectbox("Choisir une chanson :", [s['titre'] for s in toutes_les_chansons])
            chanson = next(s for s in toutes_les_chansons if s['titre'] == choix)
            
            if st.checkbox("✨ Activer le Mode Performance"):
                st.markdown(f"## {chanson['titre']}")
                st.markdown(f"### {chanson['artiste']}")
                
                if st.button("📄 Exporter en PDF"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 16)
                    pdf.cell(0, 10, txt=chanson['titre'], ln=True, align='C')
                    pdf.set_font("Arial", size=12)
                    pdf.ln(10)
                    pdf.multi_cell(0, 10, txt=chanson['paroles'])
                    pdf.output(f"{chanson['titre']}.pdf")
                    st.success(f"PDF généré : {chanson['titre']}.pdf")
                
                st.markdown("---")
                st.markdown(f"<div style='font-size: 20px;'>{chanson['paroles'].replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            else:
                st.write(f"### {chanson['titre']} - {chanson['artiste']}")
                st.write(f"**Genre :** {chanson.get('genre', 'Non défini')}")
                st.markdown("---")
                st.write(chanson['paroles'])
                if st.button("Supprimer cette chanson"):
                    os.remove(os.path.join(DATA_DIR, f"{chanson['titre']}.json"))
                    st.rerun()
        else:
            st.warning("Aucune chanson trouvée.")
    else:
        st.info("Le dossier est vide.")

# --- SECTION 4 : PLAYLIST RAPIDE ---
elif menu == "Playlist Rapide":
    st.subheader("🎸 Créer une Setlist")
    fichiers = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    toutes_les_chansons = [json.load(open(os.path.join(DATA_DIR, f), "r", encoding="utf-8")) for f in fichiers]
    
    noms_chansons = [s['titre'] for s in toutes_les_chansons]
    selection = st.multiselect("Sélectionne les chansons pour ton concert :", noms_chansons)
    nom_setlist = st.text_input("Nom de la Setlist :")
    
    if st.button("Sauvegarder la Setlist"):
        if nom_setlist and selection:
            data = {"nom": nom_setlist, "chansons": selection}
            with open(os.path.join(DATA_DIR, f"setlist_{nom_setlist}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            st.success(f"Setlist '{nom_setlist}' sauvegardée !")
        else:
            st.error("Donne un nom et choisis des chansons.")

    st.subheader("Mes Setlists")
    setlists = [f for f in os.listdir(DATA_DIR) if f.startswith("setlist_")]
    for s in setlists:
        with open(os.path.join(DATA_DIR, s), "r", encoding="utf-8") as f:
            data = json.load(f)
            if st.expander(data['nom']):
                st.write("Chansons :", ", ".join(data['chansons']))