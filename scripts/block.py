"""
方块类，不可通过的障碍物
"""
import pygame

from .entity import Entity
from . import image_dict


class Block(Entity):
    def __init__(self, width: int, height: int):
        # 因为要缩放，所以图片的质地应该均匀，以免缩放出来奇奇怪怪
        image: pygame.Surface = image_dict['block']
        if width <= image.get_width() and height <= image.get_height():
            # 这里用了一张纹理的大图，截取中间一部分即可
            image_final = pygame.Surface((width, height))
            image_final.blit(image, (0, 0))
        else:
            # 需求过大就缩放一下（可能会很糊）
            image_final = pygame.transform.scale(image, (width, height))
        super().__init__(image_final)
