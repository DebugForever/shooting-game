"""
子弹类，包含所有射出的子弹
class bullet
"""

from .entity import Entity
import pygame


class Bullet(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)

    # todo 记得在子弹射出屏幕时销毁，或者设置屏幕周围的屏障，否则游戏会越跑越卡
