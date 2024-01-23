# Homework Allistone

## Description

Ce dépôt GitHub contient les éléments nécessaires pour le déploiement d'une API pour un modèle de machine learning. Le modèle de machine learning est basé sur le réseau de neurones U-Net et est utilisé pour la segmentation d'images de capillaires sanguins. L'API prend en entrée une image et renvoie l'image segmentée ainsi que le nombre de capillaires segmentés sur l'image.

**Technologies utilisées :** API FastAPI + STREAMLIT + DOCKER (application containerisée)


-La bibliothèque FastAPI pour la création du backend (plus performante et intuitive que FLASK). Ce backend consiste à définir une API FastAPI qui accepte une image en entrée, effectue des prédictions de segmentation de capillaires sanguins à l'aide d'un modèle TensorFlow/Keras, génère des représentations graphiques des résultats, et renvoie ces représentations graphiques ainsi que le nombre de capillaires segmentés en format JSON. 

-La bibliothèque streamlit s'occupe de la partie frontend. Elle est utilisée pour implémenter une interface utilisateur Web interactive qui permet aux utilisateurs de télécharger une image, d'envoyer cette image à une API FastAPI, puis d'afficher les résultats de la segmentation des capillaires sanguins fournis par l'API.

- Le logiciel Dockersimplifie le processus de développement, de déploiement et de gestion d'applications basées sur une API FastAPI et Streamlit, en offrant une solution d'encapsulation et d'isolation des composants de l'application dans des conteneurs. Cela facilite la cohérence entre les environnements de développement et de production, ainsi que la distribution et le déploiement de l'application.



## Contenu du Répertoire

- **frontend :** Contient le code Streamlit pour l'interface graphique.
- **api :** Contient le code de l'API FastAPI qui renvoie les prédictions du modèle `best_model.h5`.

## Utilisation

1. Clonez le dépôt : `git clone https://github.com/votre-utilisateur/nom-du-repo.git`
2. ...

(ajoutez ici des instructions d'utilisation, d'installation, etc.)

## Licence

[Insérez le type de licence ici, par exemple MIT, Apache, etc.]

