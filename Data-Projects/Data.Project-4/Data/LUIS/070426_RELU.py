import pandas as pd
import os
import pydicom
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.activations import relu

def load_data(train_csv_path, train_dir, new_size):
    train_df = pd.read_csv(train_csv_path)
    images = []
    labels = []
    for index, row in train_df.iterrows():
        image_path = os.path.join(train_dir, row['SOPInstanceUID'] + '.dcm')
        image = pydicom.dcmread(image_path).pixel_array
        # Redimensionar la imagen
        resized_image = cv2.resize(image, new_size)
        label = row['Target']
        images.append(resized_image)
        labels.append(label)
    return np.array(images), np.array(labels)

# Definir el nuevo tamaño de las imágenes
new_size = (256, 256)

# Rutas de los archivos
train_csv_path = 'C:\\Users\\EDEM\\Downloads\\DATAPROJECT4\\train.csv'
train_dir = 'C:\\Users\\EDEM\\Downloads\\DATAPROJECT4\\train'
sample_submission_path = 'C:\\Users\\EDEM\\Downloads\\DATAPROJECT4\\sample_submission.csv'
output_csv_path = 'C:\\Users\\EDEM\\Downloads\\DATAPROJECT4\\intentorelu2.csv'

# Cargar datos de entrenamiento
train_images, train_labels = load_data(train_csv_path, train_dir, new_size)

# Dividir los datos en conjuntos de entrenamiento y validación
train_images, val_images, train_labels, val_labels = train_test_split(train_images, train_labels, test_size=0.2, random_state=42)

# Normalizar las imágenes y convertir las etiquetas a one-hot encoding
train_images = train_images / 255.0
val_images = val_images / 255.0
num_classes = len(np.unique(train_labels))
train_labels = to_categorical(train_labels, num_classes=num_classes)
val_labels = to_categorical(val_labels, num_classes=num_classes)

# Construir el modelo de red neuronal
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation=relu, input_shape=(new_size[0], new_size[1], 1)),
    Conv2D(32, kernel_size=(3, 3), activation=relu),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, kernel_size=(3, 3), activation=relu),
    Conv2D(64, kernel_size=(3, 3), activation=relu),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, kernel_size=(3, 3), activation=relu),
    Conv2D(128, kernel_size=(3, 3), activation=relu),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(256, activation=relu),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

# Compilar el modelo
model.compile(optimizer=RMSprop(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(train_images, train_labels, validation_data=(val_images, val_labels), epochs=20, batch_size=64)

# Generar predicciones para el conjunto de prueba (si es necesario)
test_images, _ = load_data(sample_submission_path, 'C:\\Users\\EDEM\\Downloads\\DATAPROJECT4\\test', new_size)
test_images = test_images / 255.0
predictions = model.predict(test_images)
predicted_labels = np.argmax(predictions, axis=1)

# Crear un DataFrame con las predicciones
submission_df = pd.DataFrame({'SOPInstanceUID': pd.read_csv(sample_submission_path)['SOPInstanceUID'], 'Target': predicted_labels})

# Guardar el DataFrame como un archivo CSV
submission_df.to_csv(output_csv_path, index=False)
