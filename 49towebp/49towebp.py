import os  # 导入操作系统模块，用于文件路径操作
import argparse  # 导入命令行参数解析模块
from PIL import Image  # 从PIL库导入Image模块，用于图像处理
import concurrent.futures  # 导入并发模块，用于多线程处理


def convert_image_to_webp(input_image_path, output_folder, quality):
    try:
        image = Image.open(input_image_path)  # 打开输入图像
        # 如果图像尺寸超过5000像素，则进行缩放
        if max(image.width, image.height) > 5000:
            ratio = 5000 / max(image.width, image.height)  # 计算缩放比例
            new_size = (int(image.width * ratio),
                        int(image.height * ratio))  # 计算新尺寸
            image = image.resize(new_size, Image.ANTIALIAS)  # 缩放图像
        # 保存图像为WEBP格式
        output_image_path = os.path.join(
            output_folder, os.path.basename(input_image_path) + '.webp')
        image.save(output_image_path, 'WEBP', quality=quality)  # 设置图像质量和保存路径
        # 打印转换成功信息
        print(f"Converted {input_image_path} to {output_image_path}")
    except Exception as e:
        print(f"Error converting {input_image_path}: {e}")  # 打印转换错误信息


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='Convert images to WEBP.')
    parser.add_argument(
        'input_folder', help='Input folder containing images.')  # 输入文件夹路径
    parser.add_argument(
        'output_folder', help='Output folder for WEBP images.')  # 输出文件夹路径
    parser.add_argument('quality', type=int,
                        help='Quality of WEBP images (0-100).')  # WEBP图像质量
    args = parser.parse_args()

    # 如果输出文件夹不存在，则创建
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    # 查找输入文件夹中的所有图像文件
    images = [os.path.join(args.input_folder, f) for f in os.listdir(
        args.input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    # 使用多线程将图像转换为WEBP格式
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        for image_path in images:
            executor.submit(convert_image_to_webp, image_path,
                            args.output_folder, args.quality)


if __name__ == '__main__':
    main()
