from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping  # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore


def tensorflow_init() -> Any:
  train_datagen = ImageDataGenerator(rescale=1/255)
  validation_datagen = ImageDataGenerator(rescale=1/255)

  train_generator = train_datagen.flow_from_directory(
    './data/train/', 
    classes = ['bear', 'human'],
    target_size=(200, 200),
    batch_size=7,
    class_mode='binary'
  )

  validation_generator = validation_datagen.flow_from_directory(
    './data/valid/', 
    classes = ['bear', 'human'],
    target_size=(200, 200),
    batch_size=17,
    class_mode='binary',
    shuffle=False
  )
  
  callback = EarlyStopping(
    monitor="loss",
    mode="min",
    restore_best_weights=True,
    patience=4,
    start_from_epoch=10,
    verbose=1
  )

  model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_shape = (200,200,3)),
                                      tf.keras.layers.Dense(128, activation=tf.nn.relu),
                                      tf.keras.layers.Dense(1, activation=tf.nn.sigmoid)])

  model.summary()

  model.compile(optimizer = tf.keras.optimizers.Adam(),
                loss = 'binary_crossentropy',
                metrics=['accuracy'])

  history = model.fit(
    train_generator,
    steps_per_epoch=10,
    epochs=15,
    verbose=1,
    validation_data = validation_generator,
    validation_steps=10,
    callbacks=[callback]
  )
  
  return model


def recognize_picture(filename: str, model: Any):
  img = image.load_img(filename, target_size=(200, 200))
  x = image.img_to_array(img)
  plt.imshow(x / 255.)
  x = np.expand_dims(x, axis=0)
  images = np.vstack([x])
  classes = model.predict(images, batch_size=10)
  
  if classes[0] < 0.5:
      return (0, classes[0][0]) # bear
  else:
      return (1, classes[0][0]) # human