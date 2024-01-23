from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse 
from tensorflow.keras.models import load_model
import numpy as np
import io
from PIL import Image
from code_segmentation.predictions import get_segmentator, get_segments, plot_counted_capillaries

#load le modèle ML
model = get_segmentator()

#définir l'app
app = FastAPI()

@app.post("/predict")
async def predict(file: UploadFile):
    image_data = await file.read()

    # ouvrir l'image
    img = Image.open(io.BytesIO(image_data))
    
    # Convertir l'image en tableau NumPy
    img_array = np.array(img)
  

    # prediction de l'image
    Count,predictions,image,th_Area,cluster,orig_height,orig_width= get_segments(img_array,model)
    #plot les images segmentés et avec les clusters
    plot_base64_pred,plot_base64_countour = plot_counted_capillaries(predictions,image,th_Area,cluster,orig_height,orig_width)
    
    return JSONResponse(content={"plot_base64_pred": plot_base64_pred,"plot_base64_countour": plot_base64_countour,"resultat": Count})


