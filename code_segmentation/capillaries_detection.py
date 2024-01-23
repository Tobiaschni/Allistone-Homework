#ces fonctions sont définies pour analyser des images, en extraire des formes blanches
#et regrouper les formes blanches suffisement proches, on parle de cluster de forme
#ces fonctions sont appelés dans prédictions, on peut voir ce script comme un module




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






class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Compression de chemin
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x != root_y:
            # Union par rang
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y
                if self.rank[root_x] == self.rank[root_y]:
                    self.rank[root_y] += 1






def cluster_objects(binary_image, threshold, threshold_area):

    labeled_image, num_labels = label(binary_image, connectivity=2, return_num=True)


    # Filter labeled images based on area
    Area = []
    valid_labels = []
    for label_value in range(1, num_labels + 1):
        area = np.sum(labeled_image == label_value)
        Area.append(area)
        if area > threshold_area:
            valid_labels.append(label_value)

    # Create a mapping from old labels to new labels
    label_mapping = {label_value: new_label for new_label, label_value in enumerate(valid_labels, start=1)}

    N = len(label_mapping)
    # Update labeled image with new labels
    labeled_image_filtered = np.vectorize(lambda x: label_mapping.get(x, 0))(labeled_image)

    distances_matrix = np.zeros((N, N))
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if j != i:
                coords_i = np.column_stack(np.where(labeled_image_filtered == i))
                coords_j = np.column_stack(np.where(labeled_image_filtered == j))
                distances = cdist(coords_i, coords_j, 'euclidean')
                distances_matrix[i - 1, j - 1] = distances.min()

    uf = UnionFind(len(valid_labels))

    for i in range(len(valid_labels)):
        for j in range(i + 1, len(valid_labels)):
            if distances_matrix[i][j] < threshold:
                uf.union(i, j)

    clusters = {}
    for i in range(len(valid_labels)):
        root = uf.find(i)
        if root not in clusters:
            clusters[root] = [i]
        else:
            clusters[root].append(i)

    result = [tuple(label_mapping[valid_labels[cluster]] for cluster in clusters[root]) for root in clusters]
    result_list = []
    for indices in result:
      valid_indices = [i - 1 for i in indices if 0 <= i - 1 < len(valid_labels)]
      result_list.append(tuple(valid_labels[i] for i in valid_indices))
    return result_list,Area




def concat_labels(labeled_image, label_tuples_to_concat):
    new_labeled_image = labeled_image.copy()

    # Créez un dictionnaire pour mapper les anciens labels aux nouveaux labels ordonnés
    label_mapping = {}
    new_label_count = 1

    for label_tuple in label_tuples_to_concat:
        concatenated_label = new_label_count
        for label_number in label_tuple:
            label_mapping[label_number] = concatenated_label
        new_label_count += 1

    # Utilisez le dictionnaire pour mettre à jour les labels dans la nouvelle image étiquetée
    for old_label, new_label in label_mapping.items():
        new_labeled_image[labeled_image == old_label] = new_label

    return new_labeled_image



def split_tuples_gros(tuple_list, area_list, threshold):
    marked_for_splitting = set()

    for idx, tup in enumerate(tuple_list):
        areas_above_threshold = [area_list[i - 1] for i in tup if area_list[i - 1] > threshold]
        if len(areas_above_threshold) >= 2:
            marked_for_splitting.add(idx)


    result_list = []

    for idx, tup in enumerate(tuple_list):
        if idx in marked_for_splitting:
          for i in tup:
            result_list.append((i,))
        else:
            result_list.append(tup)


    return result_list
