from PIL import Image
import streamlit as st
import requests
import base64
import io

def main():
    # Titre de l'application
    st.title("Segmentation des capillaires sanguins - Allistone Homework")
    
    # Description de l'application
    st.write(
        """ Cette API permet d'obtenir la segmentation d'image de capillaires sanguins
        et de compter leurs nombres"""
    )

    # Zone de chargement de l'image
    upload = st.file_uploader("Chargez l'image de votre objet", type=['png', 'jpeg', 'jpg'])

    if upload:
        # Préparation de l'image pour l'envoi à l'API
        files = {"file": upload.getvalue()}
        req = requests.post("http://fastapi:8000/predict", files=files)
        resultat = req.json()
        
        # Récupération des images encodées en base64 depuis l'API
        plot_base_pred = resultat["plot_base64_pred"]
        plot_bytes_pred = base64.b64decode(plot_base_pred)
        plot_base_countour = resultat["plot_base64_countour"]
        plot_bytes_countour = base64.b64decode(plot_base_countour)
        
        # Section pour afficher l'image originale
        st.subheader("Image originale")
        st.image(Image.open(upload))
        
        # Section pour afficher la segmentation
        st.subheader("Segmentation")
        st.image(Image.open(io.BytesIO(plot_bytes_pred)))
        
        # Section pour afficher la détection des capillaires
        st.subheader("Detection des capillaires")
        st.image(Image.open(io.BytesIO(plot_bytes_countour)))

        # Afficher le nombre de capillaires détectés
        st.write(f"Le nombre de capillaires comptés est : {resultat['resultat']}")

if __name__ == "__main__":
    main()
