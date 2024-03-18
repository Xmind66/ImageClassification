import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from shutil import copy2


# 加载模型
model = load_model('screenshot_classifier.keras')

# 待检测的文件夹路径
# source_folder = r'Data\test'
source_folder = r'data\test'

# 结果保存的文件夹路径
result_folder = r'Data\test2'

# 定义两个类别的文件夹名称
class_a_folder = 'class_a'
class_b_folder = 'class_b'

# 确保结果文件夹存在
os.makedirs(os.path.join(result_folder, class_a_folder), exist_ok=True)
os.makedirs(os.path.join(result_folder, class_b_folder), exist_ok=True)

# 遍历文件夹
for subdir, dirs, files in os.walk(source_folder):
    for file in files:
        # 检查文件是否为图片（这里只检查了几种常见的图片格式）
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(subdir, file)

            # 加载和预处理图片
            img = image.load_img(img_path, target_size=(150, 150))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0

            # 预测图片
            prediction = model.predict(img_array)

            # 根据预测结果保存图片
            if prediction[0][0] > 0.5:
                # 图片属于 class_b
                destination = os.path.join(result_folder, class_b_folder, file)
            else:
                # 图片属于 class_a
                destination = os.path.join(result_folder, class_a_folder, file)

            # 复制文件到新的目录
            copy2(img_path, destination)
            print(f"Copied {file} to {destination}")

print("Classification and copying of images is complete.")
