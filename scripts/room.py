"""
生成随机的房间
generate random rooms
"""
import pygame
from . import setting
from pygame.sprite import Group
from .enemy import Slime


class Room:
    def __init__(self):
        self.rect = pygame.rect.Rect(0, 0, *setting.room_size)
        self.done = False

    def generate(self, enemies: Group):
        """
        生成一波新的敌人
        :param enemies:
        :return:
        """
        enemy1 = Slime()
        enemy1.x = 100
        enemy1.y = 100
        enemy2 = Slime()
        enemy2.x = 200
        enemy2.y = 200
        enemy3 = Slime()
        enemy3.x = 300
        enemy3.y = 300
        enemies.add(enemy1, enemy2, enemy3)
