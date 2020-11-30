import pandas as pd
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras import backend
# from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
import efficientnet.tfkeras as efn 
from efficientnet.tfkeras import preprocess_input
from keras.models import load_model
from keras.preprocessing import image
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class PetProfile:
    """Class for a pet profile"""
    def __init__(self, website, photo):
        self.website = website
        self.photo = photo


def cos_d(v1, v2):
    """Compute cosine distance between two vectors"""
    v1 = np.array(v1)
    v2 = np.array(v2)
    return 1 - v1.dot(v2.T) / np.linalg.norm(v1) / np.linalg.norm(v2)


def matching_dog(model, img_input_path, embedding_path, merged_path, target_size, top_n=15):
    """Returns list of top_n similar dog objects"""
    img = image.load_img(img_input_path, target_size=target_size)

    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    emb_input = model.predict(img_data)[0]

    merged = pd.read_csv(merged_path)

    emb_matrix = np.loadtxt(embedding_path)

    scores = []
    for i in range(len(emb_matrix)):
        scores.append(cos_d(emb_input, list(emb_matrix[i])))

    ranks = [[index, merged.photo_url[index], merged.links[index],
              merged.titles[index], score] for index,
             score in enumerate(scores, 0)]
    ranks.sort(key=lambda x: x[-1])

    dogs = []

    seen = set()
    ind = 0
    while len(dogs) < top_n:
        instance = ranks[ind]
        if instance[1] not in seen:
            seen.add(instance[1])
        else:
            ind += 1
            continue
        profile = PetProfile(instance[2],instance[1])
        dogs.append(profile)
        ind += 1
    return dogs

