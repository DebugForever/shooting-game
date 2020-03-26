"""
所有敌人的类都放在这里
contains all enemy class
"""

import pygame
from .entity import Entity
from . import image_dict


class Enemy(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)


class Slime(Enemy):
    def __init__(self):
        super().__init__(image_dict['enemy1'])
