#Dans ce code 3 fonctions sont définines 

#get_segments : cette fonction prend en entrée une image et  un model et effectue sa prédiction
#en la faisant passer par le model. Cette prediction passe par une série de foncion
#définies dans le module capillaries_detection pour detecter les capillaires sanguins 
#et les rassembler en cluster en fonction de leur proximité spatiale. 
#La fonction renvoie le nombre de capillaire compté, l'image segmentée, les clusters trouvés,...
#ces output utiles pour la fonction plot_counted_capillaires

#plot_counted_capillaires prend une serie d'elements en entrée dont l'image segmentée et les clusters
# et dessinent sur l'image segmentée des boîtes autour des clusters


#get_segmentator load le model keras

import numpy as np
import cv2
from skimage import measure, draw
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import base64
import io
from PIL import Image
from skimage.morphology import label
import tensorflow as tf
from tensorflow.keras.models import load_model
from .capillaries_detection import *




def get_segments(image,model):
    


  #preprocessing de l'image
  img_original = image
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  image = image/255
  
  # Dimensions initiales de l'image
  original_height, original_width = image.shape
  
  #Dimensions de l'image souhaitées pour la prédictions
  target_height = 960
  target_width = 1280

  # Calcul du rembourrage nécessaire pour ajuster la dimension des images pour le model
  pad_height = max(0, target_height - original_height)
  pad_width = max(0, target_width - original_width)

  # Ajout du rembourrage avec des pixels noirs
  image = np.pad(image, ((0, pad_height), (0, pad_width)), mode='constant', constant_values=0)
  
  #predictions du modèle
  image = np.expand_dims(image, axis=0)
  predictions = model.predict(image,verbose=0)
  
  #conversion en binaire de la prédiction
  thresholds = 0.5
  binary_map_test = (predictions >= thresholds).astype(np.uint8)
  
  segmented_image = binary_map_test[0, :, :]
  
      

  #Paramètres utilisés pour compter les capillaires sanguins avec une méthode de clustering
  threshold_distance = 23
  threshold_Area = 340
  threshold_splitting = 1500
  
  #fonction de clustering definies dans le modules capillaries detection
  cluster_raw,area = cluster_objects(segmented_image, threshold_distance , threshold_Area)
  cluster = split_tuples_gros(cluster_raw,area, threshold_splitting)
  Count = len(cluster)
  
  
  return Count, segmented_image,image, threshold_Area, cluster,original_height, original_width







def plot_counted_capillaries(binary_image, test_images, threshold_area, label_tuples_to_outline, original_height, original_width):
    
    
    labeled_image, num_labels = label(binary_image, connectivity=2, return_num=True)

    #filtrer les formes blanches selon leur taille
    Area = []
    valid_labels = []
    for label_value in range(1, num_labels + 1):
        area = np.sum(labeled_image == label_value)
        Area.append(area)
        if area > threshold_area:
            valid_labels.append(label_value)



    labeled_image, num_labels = label(binary_image, connectivity=2, return_num=True)


    # Créer une nouvelle image étiquetée filtrée
    labeled_image_filtered = np.where(np.isin(labeled_image, list(valid_labels)), labeled_image, 0)

    # Concatenate labels
    new_labeled_image = concat_labels(labeled_image_filtered, label_tuples_to_outline)


    # Remove singleton dimensions if present
    new_labeled_image = np.squeeze(new_labeled_image)

    # Créer la première figure
    dpi = 100
    fig1, ax1 = plt.subplots(figsize=(original_width/dpi,original_height/dpi), dpi=dpi)
    ax1.imshow(binary_image[0:original_height-1, 0:original_width-1, 0], cmap='gray')
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax1.axis('off')
    
    #plt.show()

    # Sauvegarder la première figure en base64
    plot_bytes_1 = io.BytesIO()
    plt.savefig(plot_bytes_1, format='png')
    plt.close(fig1)
    plot_base64_1 = base64.b64encode(plot_bytes_1.getvalue()).decode('utf-8')

    # Créer la deuxième figure
    fig2, ax2 = plt.subplots(figsize=(original_width/dpi,original_height/dpi), dpi=dpi)
    ax2.imshow(binary_image[0:original_height-1, 0:original_width-1, 0], cmap='gray')

    # ajouter les contours des capillaires sur la deuxième figure
    for region in measure.regionprops(new_labeled_image):
        # Filtrer les objets en fonction de leur aire
        if region.area > threshold_area:
            min_row, min_col, max_row, max_col = region.bbox
            rr, cc = draw.polygon_perimeter([min_row, max_row, max_row, min_row, min_row],
                                            [min_col, min_col, max_col, max_col, min_col],
                                            shape=binary_image.shape, clip=True)
            binary_image[rr, cc] = 0  # Effacer la région dans l'image résultante
            ax2.plot(cc, rr, color='red', linewidth=2)

    #ax2.set_title(f'Counted Capillaries')
    plt.tight_layout()
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax2.axis('off')
    
    #plt.show()

    # Sauvegarder la deuxième figure en base64
    plot_bytes_2 = io.BytesIO()
    plt.savefig(plot_bytes_2, format='png')
    plt.close(fig2)
    plot_base64_2 = base64.b64encode(plot_bytes_2.getvalue()).decode('utf-8')

    # Retourner les deux images en base64
    return plot_base64_1, plot_base64_2

  





def get_segmentator():

    model_path = 'segm_model_final.h5'
    my_model = tf.keras.models.load_model(model_path, compile=False)

    return my_model







# #inference    


# my_model = get_segmentator()


# image_path = r"C:\Users\tobia\OneDrive\Bureau\API_fin\Test_images\18514_005.png"
# img = cv2.imread(image_path)
# img = np.array(img)


# Count,predictions,image,th_Area,cluster,orig_height,orig_width = get_segments(img,model=my_model)
# plot_counted_capillaries(predictions,image,th_Area,cluster,orig_height,orig_width)




  
