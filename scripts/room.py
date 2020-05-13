"""
生成随机的房间
generate random rooms
"""
from random import randint
from typing import Optional

import pygame
from . import setting
from pygame.sprite import Group
from .enemy import Slime, Enemy
from .enemy import Slime2
from .enemy import Slime3
from .enemy import Orangutan
from .enemy import Boss
from .entity import Entity
from .player import Player
from .block import Block


class Room:
    bullets_e: Group
    bullets_p: Group
    enemies: Group
    obstacles: Group
    player: Player
    rect: pygame.rect.Rect
    done: bool

    def __init__(self):
        self.rect = pygame.rect.Rect(0, 0, *setting.room_size)
        self.done = False

    def setup(self, enemies: Group, bullets_p: Group, bullets_e: Group, obstacles: Group, player: Player):
        self.enemies = enemies
        self.bullets_e = bullets_e
        self.bullets_p = bullets_p
        self.player = player
        self.obstacles = obstacles

    def spawn_enemy(self, enemy: Enemy, x: Optional[int] = None, y: Optional[int] = None):
        if x is not None:
            enemy.x = x
        if y is not None:
            enemy.y = y
        if enemy.can_fire:  # 以后有有自机狙之外的射击方式的时候，这里的代码会改
            enemy.set_fireable(self.player, self.bullets_e)
        self.enemies.add(enemy)

    def spawn_obstacle(self, obstacle: Block, x: int, y: int):
        obstacle.x = x
        obstacle.y = y
        self.obstacles.add(obstacle)

    def generate(self):
        """
        生成一波新的敌人，基类room的generate方法需要子类覆盖，
        基类不实现这个方法。
        """
        pass


class BattleRoom(Room):
    """战斗房间，会生成一些敌人"""

    def generate(self):
        max_enemy_num = 8
        enemy_num_static = 4
        """固有敌人的生成数量"""

        # 生成地形（小方块）
        self.spawn_obstacle(Block(200, 80), 360, 420)

        # 先在上方和下方各生成2个
        self.spawn_enemy(Slime(), self.rect.centerx - 100, self.rect.top + 100)
        self.spawn_enemy(Slime2(), self.rect.centerx + 100, self.rect.top + 100)
        self.spawn_enemy(Slime3(), self.rect.centerx - 100, self.rect.bottom - 100)
        self.spawn_enemy(Orangutan(), self.rect.centerx + 100, self.rect.bottom - 100)

        # 之后随机生成4个，如果有重叠则放弃生成
        for i in range(max_enemy_num - enemy_num_static):
            x = randint(self.rect.left, self.rect.right)
            y = randint(self.rect.top, self.rect.bottom)
            now_enemy = Slime()
            now_enemy.x = x
            now_enemy.y = y
            if not pygame.sprite.spritecollideany(now_enemy, self.enemies) \
                    and not pygame.sprite.spritecollideany(now_enemy, self.obstacles):
                self.spawn_enemy(now_enemy)
