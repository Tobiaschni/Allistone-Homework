# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:36:39 2024

@author: tobia
"""

from fastapi.testclient import TestClient
from api_3 import app
from PIL import Image
from io import BytesIO
import json


client = TestClient(app)

def test_predict_with_custom_image():
    # Lire le contenu de l'image de test depuis le fichier
    with open("Test_images\\18488_011.png", "rb") as file:
        image_data = BytesIO(file.read())

    # Envoie une requête POST à l'endpoint /predict avec le fichier image
    response = client.post("/predict", files={"file": ("test_image.png", image_data, "image/png")})

    # Assurez-vous que la réponse a un code HTTP 200 (OK)
    assert response.status_code == 200

    # Analysez la réponse JSON
    result = response.json()

    # Assurez-vous que les clés attendues sont présentes dans la réponse
    assert "plot_base64_pred" in result
    assert "plot_base64_countour" in result
    assert "resultat" in result

    # Vous pouvez également effectuer des assertions spécifiques sur les valeurs retournées
    # par exemple, assurez-vous que le nombre de capillaires comptés est un entier positif
    assert isinstance(result["resultat"], int)
    assert result["resultat"] >= 0
    
test_predict_with_custom_image()
