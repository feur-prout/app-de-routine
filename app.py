import streamlit as st
import json
import os
from datetime import date

FICHIER_JOURNAL = "journal.json"

st.set_page_config(page_title="Suivi Quotidien", layout="centered")
st.title("📋 Suivi Quotidien")

# --- Mot de passe ---
mdp_secret = os.getenv("MOT_DE_PASSE")

mdp = st.text_input("🔒 Entrez le mot de passe :", type="password")
if mdp != mdp_secret:
    st.warning("Mot de passe incorrect ou manquant.")
    st.stop()

# Le reste de ton code ici
st.write("Bienvenue dans ton application sécurisée !")
# --- Saisie des données ---
with st.form("form_suivi"):
    pas = st.number_input("👣 Nombre de pas", min_value=0, step=100)

    gourdes = st.number_input("💧 Quantité d'eau (en gourdes)", min_value=0.0, step=0.1)

    a_lu = st.checkbox("📖 As-tu lu aujourd’hui ?")
    pages = st.number_input("Nombre de pages lues", min_value=0, step=1) if a_lu else 0

    carnet_vert = st.checkbox("📗 As-tu rempli ton carnet vert ?")

    submitted = st.form_submit_button("✅ Sauvegarder")

# --- Sauvegarde ---
if submitted:
    donnee_du_jour = {
        "pas": pas,
        "objectif_pas": 8000,
        "gourdes_bues": gourdes,
        "objectif_gourdes": 3.5,
        "a_lu": a_lu,
        "pages_lues": pages,
        "carnet_vert": carnet_vert
    }

    aujourd_hui = str(date.today())

    if os.path.exists(FICHIER_JOURNAL):
        with open(FICHIER_JOURNAL, "r") as f:
            journal = json.load(f)
    else:
        journal = {}

    journal[aujourd_hui] = donnee_du_jour

    with open(FICHIER_JOURNAL, "w") as f:
        json.dump(journal, f, indent=4)

    st.success("✅ Données enregistrées pour aujourd’hui !")

# --- Affichage historique ---
st.markdown("---")
st.subheader("📅 Historique")

if os.path.exists(FICHIER_JOURNAL):
    with open(FICHIER_JOURNAL, "r") as f:
        journal = json.load(f)

    for jour in sorted(journal.keys(), reverse=True):
        entry = journal[jour]
        with st.expander(f"📆 {jour}"):
            st.markdown(f"- **Pas** : {entry['pas']} / {entry['objectif_pas']}")
            st.markdown(f"- **Eau** : {entry['gourdes_bues']} / {entry['objectif_gourdes']} gourdes")
            if entry["a_lu"]:
                st.markdown(f"- **Lecture** : oui ({entry['pages_lues']} pages)")
            else:
                st.markdown(f"- **Lecture** : non")
            st.markdown(f"- **Carnet vert** : {'oui' if entry['carnet_vert'] else 'non'}")
else:
    st.info("Aucune donnée enregistrée pour le moment.")

