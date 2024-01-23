# Homework Allistone

## Description

Ce dépôt GitHub contient les éléments nécessaires pour le déploiement d'une API pour un modèle de machine learning. Le modèle de machine learning est basé sur le réseau de neurones U-Net et est utilisé pour la segmentation d'images de capillaires sanguins. L'API prend en entrée une image et renvoie l'image segmentée ainsi que le nombre de capillaires segmentés sur l'image.

## Structure du projet

**Technologies utilisées :** API FastAPI/STREAMLIT/DOCKER (application containerisée)

- La bibliothèque FastAPI pour la création du backend (plus performante et intuitive que FLASK). Ce backend consiste à définir une API FastAPI qui accepte une image en entrée, effectue des prédictions de segmentation de capillaires sanguins à l'aide du modèle `segm_model_final.h5`. La prédiction (segmentation + le compte des capillaires) et la représentation graphique de la segmentation sont réalisées par trois fonctions dans le script code_segmentation/predictions.py. Ces trois fonctions utlisent d'autres fonctions définies dans le script ode_segmentation/capillaries_detection.py. Ces résultats sont ensuite renvoyer en format JSON. Le code est concu pour n'accepter en entrée que des files de format png ou jpeg.

- La bibliothèque streamlit s'occupe de la partie frontend. Cette bibliothèque est facile à déployer et rapide et interactive, elle est une référence en data science. Elle est utilisée pour implémenter une interface utilisateur Web interactive qui permet aux utilisateurs de télécharger une image, d'envoyer cette image à une API FastAPI, puis d'afficher les résultats de la segmentation des capillaires sanguins fournis par l'API et le compte de ces capillaires.

- Le logiciel Docker simplifie le processus de développement, de déploiement et de gestion d'applications basées sur une API FastAPI et Streamlit, en offrant une solution d'encapsulation et d'isolation des composants de l'application dans des conteneurs. Cela facilite la cohérence entre les environnements de développement et de production, ainsi que la distribution et le déploiement de l'application.


## Contenu du Répertoire

- **Test_images :** Contient des images de capillaires sanguins pour tester l'API
- **code_segmentation:** Contient les scripts predictions.py et capillaries_detections.py. Les fonctions de capillaires_detections.py sont appellées dans predictions.py. Les fonctions de predictions.py sont utilisées dans le backend.py pour prédire la segmentation, compter le nombre de capillaire et dessiner les capillaires sur la segmentations.
- **backend:** Consiste à définir une API FastAPI qui accepte une image en entrée, effectue des prédictions de segmentation de capillaires sanguins à l'aide du modèle `segm_model_final.h5`. La prédiction (segmentation + le compte des capillaires) et la représentation graphique de la segmentation sont réalisées par trois fonctions dans le script code_segmentation/predictions.py
- **frontend:** Utilisée pour implémenter une interface utilisateur Web interactive qui permet aux utilisateurs de télécharger une image, d'envoyer cette image à une API FastAPI, puis d'afficher les résultats de la segmentation des capillaires sanguins fournis par l'API et le compte de ces capillaires
- **requirements_backend:** toutes les bibliothèques nécessaires pour exécuter le backend
- **Dockerfile_backend:** Ce dockerfile configure un conteneur Docker pour exécuter une application Python basée sur FastAPI en utilisant Uvicorn comme serveur, avec les dépendances installées à partir du fichier requirements_backend.txt. Le conteneur écoute sur le port 8000 et utilise une variable d'environnement NAME.
- **requirements_frontend:**  toutes les bibliothèques nécessaires pour exécuter le frontend
- **Dockerfile_backend:** Ce dockerfile configure un conteneur Docker pour exécuter une application basée sur Streamlit. Il installe les dépendances à partir du fichier requirements_frontend.txt, expose le port 8501, puis lance automatiquement l'application Streamlit en exécutant le script frontend.py lorsque le conteneur est démarré.
- **Docker_compose:** Ce fichier Docker Compose configure deux services, l'un pour FastAPI et l'autre pour Streamlit, en spécifiant comment construire les images Docker, quels ports exposer et comment les services dépendent les uns des autres.
- **unit_test_backend:** contient un unitest pour tester le backend. S'assure que les output sont dans le format attendus

## Utilisation

1. Clonez le dépôt : `git clone https://github.com/votre-utilisateur/nom-du-repo.git`
2. ...

(ajoutez ici des instructions d'utilisation, d'installation, etc.)

## Test 

## Licence

[Insérez le type de licence ici, par exemple MIT, Apache, etc.]

