"""
未分类的函数存放与此
other functions
"""
import os
import pygame


def load_all_images(directory: str, accept_suffixs: tuple = ('.bmp',), color_key: tuple = (255, 0, 255)) -> dict:
    """
    :param directory:要读取的路径
    :param accept_suffixs要读取的格式
    :param color_key:设定为透明色的颜色，如果图片本身有alpha通道，则使用alpha通道
    :return:包含所有图片的字典
    """
    images = dict()
    for pic in os.listdir(directory):
        name, suffix = os.path.splitext(pic)
        if suffix.lower() in accept_suffixs:
            pic_path = os.path.join(directory, pic)
            img = pygame.image.load(pic_path)
            if img.get_alpha():
                img = img.convert_alpha()  # 转换为最快的格式，下同
            else:
                img = img.convert()
                img.set_colorkey(color_key)
            images[name] = img
    return images
