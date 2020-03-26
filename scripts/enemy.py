"""
所有敌人的类都放在这里
contains all enemy class
"""

import pygame
from .entity import Entity
from . import image_dict
from . import setting
from . import dbgscreen


class Enemy(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        # 战斗有关的属性，以下为默认值，没有什么用，因为你一定要覆盖这些值
        self.maxhp = 1
        self.hp = 1
        self.atk = 1
        self.gold = 1

    def draw(self, screen: pygame.Surface):
        super().draw(screen)  # 先画出图像
        hp_bar_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, setting.enemy_hpbar_height))
        pygame.draw.rect(screen, setting.enemy_hpbar_color, hp_bar_rect)  # 画血条
        pygame.draw.rect(screen, setting.enemy_hpbar_line_color, hp_bar_rect, setting.enemy_hpbar_line_width)  # 画边框


class Slime(Enemy):
    def __init__(self):
        super().__init__(image_dict['enemy1'])
        self.maxhp = 100
        self.hp = 100
        self.atk = 10
        self.gold = 1
