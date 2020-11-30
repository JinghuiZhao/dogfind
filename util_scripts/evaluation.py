import os.path
import os
import sys
import pandas as pd
import numpy as np
from tensorflow.keras.models import Model
from keras.models import load_model
from keras.preprocessing import image


def embedding_generator(model_name, img_database_folder):
    emb_matrix = []

    if model_name == 'inception':
        from tensorflow.keras.applications.inception_v3 import InceptionV3
        from tensorflow.keras.applications.inception_v3 import preprocess_input  as preprocess_input_a
        base_model = InceptionV3(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('avg_pool').output)

        target_size = (299, 299)
        
        
    elif model_name == 'resnet':
        from tensorflow.keras.applications import ResNet50V2
        from tensorflow.keras.applications.resnet_v2 import preprocess_input  as preprocess_input_a
        base_model = ResNet50V2()
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('avg_pool').output)
    
        target_size = (224, 224)
        
    elif model_name == 'vgg':
        from tensorflow.keras.applications.vgg19 import VGG19
        from tensorflow.keras.applications.vgg19 import preprocess_input  as preprocess_input_a
        base_model = VGG19(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('fc2').output)
        
        target_size = (224, 224)
        
    elif model_name == 'efficientnet':
        import efficientnet.tfkeras as efn
        from efficientnet.tfkeras import preprocess_input as preprocess_input_a
        base_model = efn.EfficientNetB7(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('top_dropout').output)

        target_size = (600, 600)
        
    elif model_name == 'efficientnetb0':
        import efficientnet.tfkeras as efn 
        from efficientnet.tfkeras import preprocess_input as preprocess_input_a
        base_model = efn.EfficientNetB0(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('top_dropout').output)

        target_size = (224, 224)
        
        
    elif model_name == 'efficientnetb3':
        import efficientnet.tfkeras as efn 
        from efficientnet.tfkeras import preprocess_input as preprocess_input_a
        base_model = efn.EfficientNetB3(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('top_dropout').output)

        target_size = (300, 300)
    

    for name in os.listdir(img_database_folder):
        full_file_path = os.path.join(img_database_folder, name)
        try:
            img = image.load_img(full_file_path, target_size=target_size)
        except:
            emb_matrix.append([999.0000] * len(emb_matrix[0]))
            continue
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input_a(img_data)
        emb_matrix.append(list(np.around(model.predict(img_data)[0],
                                         decimals=4)))

        
    df = pd.DataFrame(list(zip(os.listdir(img_database_folder), emb_matrix)),
                       columns =['img_name', 'featue_vector']) 

    return df


def evaluate(model_name, test_imgs_path):
    def cos_d(v1, v2):
        v1 = np.array(v1)
        v2 = np.array(v2)
        return 1 - v1.dot(v2.T) / np.linalg.norm(v1) / np.linalg.norm(v2)
                    
    vector_table = embedding_generator(model_name, test_imgs_path)
    # print(vector_table)
    test_imgs_path = [os.path.join(test_imgs_path, p) for p in os.listdir(test_imgs_path)]
    
    if model_name == 'inception':   
        from tensorflow.keras.applications.inception_v3 import InceptionV3
        from tensorflow.keras.applications.inception_v3 import preprocess_input  as preprocess_input_b     
        base_model = InceptionV3(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('avg_pool').output)
        img_list = [(single_image.split('/')[-1].split('.')[0][:-2],
                     image.load_img(single_image, target_size=(299, 299))) for single_image in test_imgs_path]
    
    elif model_name == 'resnet':
        from tensorflow.keras.applications import ResNet50V2
        from tensorflow.keras.applications.resnet_v2 import preprocess_input  as preprocess_input_b

        base_model = ResNet50V2()
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('avg_pool').output)
        img_list = [(single_image.split('/')[-1].split('.')[0][:-2],
                     image.load_img(single_image, target_size=(224, 224))) for single_image in test_imgs_path]
    
    
    elif model_name == 'vgg':
        from tensorflow.keras.applications.vgg19 import VGG19
        from tensorflow.keras.applications.vgg19 import preprocess_input  as preprocess_input_b
        base_model = VGG19(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('fc2').output)
        
        img_list = [(single_image.split('/')[-1].split('.')[0][:-2],
                     image.load_img(single_image, target_size=(224, 224))) for single_image in test_imgs_path]
    
    elif model_name == 'efficientnetb7':
        import efficientnet.tfkeras as efn 
        from efficientnet.tfkeras import preprocess_input as preprocess_input_b
        base_model = efn.EfficientNetB7(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('top_dropout').output)
        img_list = [(single_image.split('/')[-1].split('.')[0][:-2],
                     image.load_img(single_image, target_size=(600, 600))) for single_image in test_imgs_path]
        
        
    elif model_name == 'efficientnetb0':
        import efficientnet.tfkeras as efn 
        from efficientnet.tfkeras import preprocess_input as preprocess_input_b
        base_model = efn.EfficientNetB0(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('top_dropout').output)
        img_list = [(single_image.split('/')[-1].split('.')[0][:-2],
                     image.load_img(single_image, target_size=(224, 224))) for single_image in test_imgs_path]
    
    
    elif model_name == 'efficientnetb3':
        import efficientnet.tfkeras as efn 
        from efficientnet.tfkeras import preprocess_input as preprocess_input_b
        base_model = efn.EfficientNetB3(weights='imagenet')
        model = Model(inputs=base_model.input,
                      outputs=base_model.get_layer('top_dropout').output)
        img_list = [(single_image.split('/')[-1].split('.')[0][:-2],
                     image.load_img(single_image, target_size=(300, 300))) for single_image in test_imgs_path]
    
    
    
    correct = 0

    for img_name, img in img_list:
        img_data = image.img_to_array(img)
        img_data = np.expand_dims(img_data, axis=0)
        img_data = preprocess_input_b(img_data)
        emb_input = model.predict(img_data)[0]

        scores = []
        for i in range(len(vector_table)):
            scores.append(cos_d(emb_input, list(vector_table.featue_vector[i])))

        ranks = [[index, vector_table.img_name[index], score] for index,
                 score in enumerate(scores, 0)]
        ranks.sort(key=lambda x: x[-1])

        if ranks[1][1].split('.')[0][:-2] == img_name:
             correct += 1

    accuracy = correct/len([s[:-6] for s in vector_table.img_name])
    return accuracy


    

def main():
    model = str(sys.argv[1])
    folder_path = str(sys.argv[2])
    accuracy = evaluate(model, folder_path)
    return accuracy

if __name__ == "__main__":
    main()

