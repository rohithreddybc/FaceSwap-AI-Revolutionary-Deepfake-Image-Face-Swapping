import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Dropout

# Set the path to the preprocessed dataset
dataset_dir = 'preprocessed_dataset'

# Set the desired image size for input to the model
image_size = (256, 256)

# Set the batch size and number of epochs
batch_size = 32
num_epochs = 10

# Use data augmentation for training set
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=10,
                                   width_shift_range=0.1,
                                   height_shift_range=0.1,
                                   shear_range=0.1,
                                   zoom_range=0.1,
                                   horizontal_flip=True,
                                   validation_split=0.2)

# Load the pre-trained VGG16 model without the top layers
base_model = VGG16(weights='imagenet',
                   include_top=False,
                   input_shape=(image_size[0], image_size[1], 3))

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

# Create the model architecture
model = Sequential()
model.add(base_model)
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Prepare the training and validation data
train_generator = train_datagen.flow_from_directory(dataset_dir,
                                                    target_size=image_size,
                                                    batch_size=batch_size,
                                                    class_mode='binary',
                                                    subset='training',
                                                    shuffle=True,
                                                    follow_links=True)

validation_generator = train_datagen.flow_from_directory(dataset_dir,
                                                         target_size=image_size,
                                                         batch_size=batch_size,
                                                         class_mode='binary',
                                                         subset='validation',
                                                         shuffle=True,
                                                         follow_links=True)

# Train the model
model.fit(train_generator,
          steps_per_epoch=train_generator.samples // batch_size,
          epochs=num_epochs,
          validation_data=validation_generator,
          validation_steps=validation_generator.samples // batch_size)

# Save the trained model
model.save('face_swap_model.h5')

print("Model training complete!")
