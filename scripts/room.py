"""
生成随机的房间
generate random rooms
"""
from random import randint
from typing import Optional

import pygame
from pygame.sprite import Group

from . import item
from . import setting
from .block import Block
from .enemy import Boss
from .enemy import Orangutan, Slime4, Slime5
from .enemy import Slime, Enemy, TestDummy
from .enemy import Slime2
from .enemy import Slime3
from .player import Player


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

    def setup(self, enemies: Group, bullets_p: Group, bullets_e: Group, obstacles: Group, items: Group, player: Player):
        self.enemies = enemies
        self.bullets_e = bullets_e
        self.bullets_p = bullets_p
        self.player = player
        self.obstacles = obstacles
        self.items = items

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

    def spawn_item(self, item_: 'item.Item', x: int, y: int):
        item_.x = x
        item_.y = y
        self.items.add(item_)

    def generate(self):
        """
        生成一波新的敌人，基类room的generate方法需要子类覆盖，
        基类不实现这个方法。
        """
        pass


class BattleRoom(Room):
    """
    战斗房间，会生成一些敌人
    普通关卡，只会生成一般般的敌人
    """

    def generate(self):
        max_enemy_num = 8
        enemy_num_static = 4
        """固有敌人的生成数量"""

        # 生成地形（小方块）
        self.spawn_obstacle(Block(100, 200), 460, 220)
        self.spawn_obstacle(Block(100, 50), 460, 720)
        self.spawn_obstacle(Block(50, 100), 310, 420)
        self.spawn_obstacle(Block(50, 100), 510, 420)

        # 先在上方和下方各生成2个
        self.spawn_enemy(Slime(), self.rect.centerx - 100, self.rect.top + 100)
        self.spawn_enemy(Slime4(), self.rect.centerx + 100, self.rect.top + 100)
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


class BattleRoom2(Room):
    """
    战斗房间，会生成一些敌人
    特殊地形关卡
    """

    def generate(self):
        max_enemy_num = 8
        enemy_num_static = 4
        """固有敌人的生成数量"""

        # 生成地形（小方块）
        self.spawn_obstacle(Block(2, 400), 460, 420)
        self.spawn_obstacle(Block(400, 2), 460, 420)

        # 先在上方和下方各生成4个
        self.spawn_enemy(Slime4(), self.rect.centerx - 300, self.rect.top + 100)
        self.spawn_enemy(Slime4(), self.rect.centerx + 100, self.rect.top + 100)
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


class BattleRoom3(Room):
    """
    生成战斗房间
    该房间全部是固定炮塔，加上两个快速移动
    """

    def generate(self):
        max_enemy_num = 6
        enemy_num_static = 2
        """固有敌人的生成数量"""

        # 生成地形（小方块）
        self.spawn_obstacle(Block(100, 80), 360, 420)
        self.spawn_obstacle(Block(200, 50), 800, 400)
        self.spawn_obstacle(Block(100, 80), 50, 40)
        self.spawn_obstacle(Block(100, 80), 150, 40)

        # 先在上方和下方各生成2个
        self.spawn_enemy(Slime4(), self.rect.centerx - 100, self.rect.top + 100)
        self.spawn_enemy(Slime2(), self.rect.centerx + 100, self.rect.top + 100)
        self.spawn_enemy(Slime2(), self.rect.centerx - 100, self.rect.bottom - 100)
        self.spawn_enemy(Slime4(), self.rect.centerx + 100, self.rect.bottom - 100)

        # 之后随机生成4个，如果有重叠则放弃生成
        for i in range(max_enemy_num - enemy_num_static):
            x = randint(self.rect.left, self.rect.right)
            y = randint(self.rect.top, self.rect.bottom)
            now_enemy = Slime5()
            now_enemy.x = x
            now_enemy.y = y
            if not pygame.sprite.spritecollideany(now_enemy, self.enemies) \
                    and not pygame.sprite.spritecollideany(now_enemy, self.obstacles):
                self.spawn_enemy(now_enemy)


class BattleRoom4(Room):
    """战斗房间，会生成一些敌人
    boss型房间
    """

    def generate(self):
        max_enemy_num = 10
        enemy_num_static = 5
        """固有敌人的生成数量"""

        # 生成地形（小方块）
        self.spawn_obstacle(Block(100, 80), 360, 420)
        self.spawn_obstacle(Block(200, 100), 800, 400)
        self.spawn_obstacle(Block(200, 100), 600, 200)
        self.spawn_obstacle(Block(200, 100), 100, 600)

        # 先在上方和下方各生成5个
        self.spawn_enemy(Slime4(), self.rect.centerx - 100, self.rect.top + 100)
        self.spawn_enemy(Slime4(), self.rect.centerx + 100, self.rect.top + 100)
        self.spawn_enemy(Slime4(), self.rect.centerx - 100, self.rect.bottom - 100)
        self.spawn_enemy(Boss(), self.rect.centerx + 100, self.rect.bottom - 100)
        self.spawn_enemy(Slime4(), self.rect.centerx - 100, self.rect.bottom - 100)

        # 之后随机生成4个，如果有重叠则放弃生成
        for i in range(max_enemy_num - enemy_num_static):
            x = randint(self.rect.left, self.rect.right)
            y = randint(self.rect.top, self.rect.bottom)
            now_enemy = Slime5()
            now_enemy.x = x
            now_enemy.y = y
            if not pygame.sprite.spritecollideany(now_enemy, self.enemies) \
                    and not pygame.sprite.spritecollideany(now_enemy, self.obstacles):
                self.spawn_enemy(now_enemy)


class DebugRoom(Room):
    """用于测试的房间，不会在随机中出现"""

    def generate(self):
        self.spawn_enemy(TestDummy(), 400, 300)
        self.spawn_enemy(TestDummy(), 300, 400)
        self.spawn_enemy(TestDummy(), 400, 400)
        self.spawn_enemy(TestDummy(), 300, 300)
        self.spawn_item(item.ItemHpRegen(), 500, 500)
