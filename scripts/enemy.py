"""
所有敌人的类都放在这里
contains all enemy class
"""

import pygame
from .entity import Entity


class Enemy(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
