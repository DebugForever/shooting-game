"""
子弹类，包含所有射出的子弹
class bullet
"""

from .entity import Entity
import pygame


class Bullet(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        self.damage = 0

    def setup(self, x: float, y: float, dmg: int):
        self.x = x
        self.y = y
        self.damage = dmg
