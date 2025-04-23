from keras import Model
from keras.optimizers import Adam
from keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import load_model
from keras.applications import ResNet50
from keras.layers import Dense, Dropout, Flatten
import os
import numpy as n
from tensorflow.keras.preprocessing import image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_model(input_shape, n_classes, optimizer='rmsprop', fine_tune=0):

    # Pretrained convolutional layers are loaded using the Imagenet weights.
    # Include_top is set to False, in order to exclude the model's fully-connected layers.
    conv_base = ResNet50(
    include_top=False,
    weights=None,
    input_tensor=None,
    input_shape=input_shape,
    pooling=None,
    classes=n_classes,
    classifier_activation="softmax",
)

    # Create a new 'top' of the model (i.e. fully-connected layers).
    # This is 'bootstrapping' a new top_model onto the pretrained layers.
    top_model = conv_base.output
    top_model = Flatten(name="flatten")(top_model)
    top_model = Dense(4096, activation='relu')(top_model)
    top_model = Dense(1072, activation='relu')(top_model)
    top_model = Dropout(0.2)(top_model)
    output_layer = Dense(n_classes, activation='softmax')(top_model)

    # Group the convolutional base and new fully-connected layers into a Model object.
    model = Model(inputs=conv_base.input, outputs=output_layer)


    # Compiles the model fo training.
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    model_path = os.path.join(BASE_DIR, "IA", 'peso', 'teste.weights.h5')

    print(model_path)
    model.load_weights(model_path)


    return model

def inferencia(file):
    input_shape = (224, 224, 3)
    n_classes = 16
    # classes = [1]
    classes = ['P-01', 'Lobeira', 'Muriçi', 'Muriçi macho', 'Ypê Amarelo', 'Algodãozinho do Cerrado', 'Caliandra', 'Ouratia', 'Cajuzinho', 'Muriçi Rosa', 'Fabaccia', 'Cipó Uva', 'P-62', 'P-69_', 'P-70', 'Pequi']

    model = create_model(input_shape, n_classes)

    file = os.path.join(BASE_DIR, "media",  file)

    print(file)

    img = image.load_img(file, target_size=input_shape)
    img_array = image.img_to_array(img)
    img_array = n.expand_dims(img_array, axis=0)

    preds_ft = model.predict(img_array)

    pred_classes_ft = n.argmax(preds_ft, axis=1)

    print(pred_classes_ft[0])

    return classes[pred_classes_ft[0]]


