from PIL import Image
import os

# 假设你的图片存放在data_dir目录下
data_dir = r'D:\图片分类\data'
broken_files = []

# 设置一个合理的像素限制，例如允许最大5000万像素的图像
Image.MAX_IMAGE_PIXELS = 50000000

# 遍历目录及子目录中的所有文件
for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):  # 确保处理PNG和JPEG文件
            file_path = os.path.join(subdir, file)
            try:
                with Image.open(file_path) as img:
                    img.verify()  # 验证文件完整性
            except (IOError, SyntaxError, Image.DecompressionBombError) as e:
                print('Bad file or too large:', file_path)  # 打印损坏的文件路径或文件过大
                broken_files.append(file_path)

# 如果你想自动删除损坏的文件，可以取消注释下面的代码
for broken_file in broken_files:
    os.remove(broken_file)

# 打印损坏或者过大的文件列表
print("List of broken or too large files:", broken_files)
