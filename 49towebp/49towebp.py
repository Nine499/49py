import os
import shutil
from PIL import Image
import concurrent.futures

def resize_and_convert(image_path, output_folder, quality):
    try:
        # 打开图片
        with Image.open(image_path) as img:
            # 获取图片尺寸
            width, height = img.size

            # 判断是否需要缩小图片
            if width > 5000 or height > 5000:
                # 计算等比例缩小的尺寸
                ratio = 5000 / max(width, height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # 保存为WEBP格式
            output_path = os.path.join(output_folder, os.path.basename(image_path) + '.webp')
            img.save(output_path, 'WEBP', quality=quality)

        print(f"Converted and saved: {output_path}")
    except Exception as e:
        print(f"Error converting {image_path}: {e}")

def convert_images(source_folder, output_folder, quality):
    # 创建输出文件夹，如果不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历源文件夹及其子目录中的所有图片
    image_paths = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))

    # 使用一个线程池处理所有图片
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(resize_and_convert, image_path, output_folder, quality) for image_path in image_paths]
        for future in concurrent.futures.as_completed(futures):
            future.result()  # 确保无异常


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python script.py <source_folder> <output_folder> <quality>")
        sys.exit(1)

    source_folder = sys.argv[1]
    output_folder = sys.argv[2]
    quality = int(sys.argv[3])

    convert_images(source_folder, output_folder, quality)
