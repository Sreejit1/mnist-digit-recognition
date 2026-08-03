import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

# ---------------------------------------
# Load Dataset
# ---------------------------------------

(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Normalize
X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0

# Reshape
X_train = X_train.reshape(-1,28,28,1)
X_test = X_test.reshape(-1,28,28,1)

# ---------------------------------------
# Data Augmentation
# ---------------------------------------

datagen = ImageDataGenerator(
    rotation_range=15,
    zoom_range=0.15,
    width_shift_range=0.15,
    height_shift_range=0.15
)

datagen.fit(X_train)

# ---------------------------------------
# Build CNN
# ---------------------------------------

model = Sequential()

model.add(Conv2D(
    32,
    (3,3),
    activation='relu',
    input_shape=(28,28,1)
))

model.add(MaxPooling2D((2,2)))

model.add(Conv2D(
    64,
    (3,3),
    activation='relu'
))

model.add(MaxPooling2D((2,2)))

model.add(Flatten())

model.add(Dense(
    256,
    activation='relu'
))

model.add(Dropout(0.5))

model.add(Dense(
    10,
    activation='softmax'
))

# ---------------------------------------
# Compile
# ---------------------------------------

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ---------------------------------------
# Callbacks
# ---------------------------------------

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    "mnist_cnn.keras",
    save_best_only=True
)

# ---------------------------------------
# Train
# ---------------------------------------

history = model.fit(
    datagen.flow(X_train,y_train,batch_size=32),
    epochs=20,
    validation_data=(X_test,y_test),
    callbacks=[
        early_stop,
        checkpoint
    ]
)

# ---------------------------------------
# Evaluate
# ---------------------------------------

loss,accuracy=model.evaluate(X_test,y_test)

print("Accuracy :",accuracy)

# ---------------------------------------
# Save
# ---------------------------------------

model.save("mnist_cnn.keras")

print("Model Saved Successfully")