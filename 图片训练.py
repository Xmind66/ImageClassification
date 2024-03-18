import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam

import time
start_time = time.time()

# 假设您想使用第一个 GPU，其编号为1
os.environ["CUDA_VISIBLE_DEVICES"] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


img_width, img_height = 150, 150  # 图片尺寸
train_data_dir = 'data/train'  # 训练集数据目录
validation_data_dir = 'data/validation'  # 验证集数据目录
nb_train_samples = 2000  # 训练样本数
nb_validation_samples = 800  # 验证样本数
epochs = 50  # 训练轮数
batch_size = 16  # 批量大小

if tf.keras.backend.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

# 构建模型
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              #optimizer=Adam(lr=0.0001),
              optimizer = Adam(learning_rate=0.0001),
              metrics=['accuracy'])

# 数据预处理
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

# 训练模型
model.fit(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

# 保存模型
model.save('screenshot_classifier.keras')

# 绘制训练 & 验证的准确率值
plt.figure(figsize=(8, 4))
plt.subplot(1, 2, 1)
plt.plot(model.history.history['accuracy'], label='Training Accuracy')
plt.plot(model.history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()

# 绘制训练 & 验证的损失值
plt.subplot(1, 2, 2)
plt.plot(model.history.history['loss'], label='Training Loss')
plt.plot(model.history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()

plt.show()


end_time = time.time()
# 计算运行时间
total_time = end_time - start_time
# 打印总运行时间
print(f"总运行时间: {total_time} 秒")
