"""
生成随机的房间
generate random rooms
"""
import pygame
from . import setting
from pygame.sprite import Group
from .enemy import Slime
from .enemy import Slime2
from .enemy import Slime3
from .enemy import Orangutan
from .enemy import Boss
from .player import Player


class Room:
    bullets_e: Group
    bullets_p: Group
    enemies: Group
    player: Player

    def __init__(self):
        self.rect = pygame.rect.Rect(0, 0, *setting.room_size)
        self.done = False

    def setup(self, enemies: Group, bullets_p: Group, bullets_e: Group, player: Player):
        self.enemies = enemies
        self.bullets_e = bullets_e
        self.bullets_p = bullets_p
        self.player = player

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
        enemy3 = Boss()
        enemy3.x = 300
        enemy3.y = 300
        enemies.add(enemy1, enemy2, enemy3)
        for enemy in enemies:
            enemy.set_fireable(self.player, self.bullets_e)
