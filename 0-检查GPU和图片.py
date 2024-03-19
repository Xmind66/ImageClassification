import os,send2trash
import tensorflow as tf
from PIL import Image

print("检查到可用GPU数量：", len(tf.config.experimental.list_physical_devices('GPU')))
input('回车继续检查图片签名...')
# 假设你的图片存放在data_dir目录下
data_dir = r'data'
broken_files = []

# 设置一个合理的像素限制，例如允许最大5000万像素的图像
Image.MAX_IMAGE_PIXELS = 50000000

# 遍历目录及子目录中的所有文件
for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # 确保处理PNG和JPEG文件  
            file_path = os.path.join(subdir, file)
            if os.path.getsize(file_path) == 0:
                broken_files.append(file_path)
                continue
            try:
                with Image.open(file_path) as img:
                    img.verify()    #检查图像头部签名信息
                    print(f'验证图片:{file_path}')
            except (IOError, SyntaxError, Image.DecompressionBombError) as e:
                print('检测到坏图片:', file_path)  # 打印损坏的文件路径或文件过大
                broken_files.append(file_path)

# 如果你想自动删除损坏的文件，可以取消注释下面的代码
for broken_file in broken_files:
    send2trash.send2trash(file_path)
    print(f'删除不合格文件{broken_file}')
