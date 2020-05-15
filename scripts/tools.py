"""
未分类的函数存放与此
other functions
"""
import math
import os
from math import tan
from typing import Dict
import pygame

from .entity import Entity


def load_all_images(directory: str, accept_suffixs: tuple = ('.bmp', '.png'), color_key: tuple = (255, 0, 255)) \
    -> Dict[str, pygame.Surface]:
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

def load_music(name):
    """
    由于背景音乐用load加载，音效用sound加载，所以编写一个返回音乐路径的函数
    后续背景音乐和音效根据具体情况而定
    就三行代码不需要重构（假装很理直气壮
    """
    path = os.path.join('resources', 'cd',name)
    return path

def fix_entity_collision(mobile_entity: Entity, static_entity: Entity):
    """
    弹开两个碰撞的实体，使他们不重叠
    :param mobile_entity:可以移动的实体
    :param static_entity:必须静止的实体
    """
    x1 = static_entity.rect.centerx
    x2 = mobile_entity.rect.centerx
    y1 = static_entity.rect.centery
    y2 = mobile_entity.rect.centery
    xlen1 = static_entity.rect.width / 2
    xlen2 = mobile_entity.rect.width / 2
    ylen1 = static_entity.rect.height / 2
    ylen2 = mobile_entity.rect.height / 2

    dx = xlen1 + xlen2 - abs(x2 - x1)
    if x2 < x1:
        dx = -dx
    dy = ylen1 + ylen2 - abs(y2 - y1)
    if y2 < y1:
        dy = -dy
    if abs(dx) < abs(dy):
        dy = tan(-mobile_entity.direction) * dx
    else:
        if tan(-mobile_entity.direction) == 0:
            dx = 0
        else:
            dx = dy / tan(-mobile_entity.direction)

    mobile_entity.rect.move_ip(dx, dy)
    mobile_entity.sync_xy_rect()
