"""
生成随机的房间
generate random rooms
"""
import random
from typing import Optional

import pygame
from pygame.sprite import Group

from . import item
from . import setting
from .block import Block
from .enemy import Boss, Orangutan, Slime4, Slime, Enemy, TestDummy, Slime2, Slime3
from .entity import Entity
from .player import Player


class Room:
    bullets_e: Group
    bullets_p: Group
    enemies: Group
    obstacles: Group
    items: Group
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
        """
        在指定位置生成敌人
        :param enemy:要生成的敌人
        :param x:生成的x坐标，留空则使用enemy自身的x
        :param y:生成的y坐标，留空则使用enemy自身的y
        :return:None
        """
        if x is not None:
            enemy.x = x
        if y is not None:
            enemy.y = y
        if enemy.can_fire:  # 以后有有自机狙之外的射击方式的时候，这里的代码会改
            enemy.set_fireable(self.player, self.bullets_e)
        self.enemies.add(enemy)

    def check_overlap(self, entity: Entity) -> bool:
        """检查该实体与其他生物实体(Creature)和障碍物是否有重叠"""
        # 这一句代码可能会有些难懂
        return not any(
            map(
                lambda group: pygame.sprite.spritecollideany(entity, group) is not None,
                (self.obstacles, self.enemies)
            )
        )

    def spawn_enemy_randompos(self, enemy: Enemy, spawn_rect: Optional[pygame.Rect] = None, no_overlap=True) -> bool:
        """
        在指定范围内的随机位置生成一个敌人，
        可选选项：随机生成的范围，不重叠生成。
        注意生成可能失败，失败会返回False
        :param enemy:要生成的敌人
        :param spawn_rect:要生成的目标范围，这里没有检测范围，可能会生成到房间外面，默认为整个房间
        :param no_overlap:不重叠生成，如果生成位置不是空位，则会生成失败
        :return:生成是否成功
        """
        if spawn_rect is None:
            spawn_rect = self.rect

        enemy.x = random.uniform(spawn_rect.left, spawn_rect.right)
        enemy.y = random.uniform(spawn_rect.top, spawn_rect.bottom)

        try_times = 5
        if no_overlap:
            for i in range(try_times):
                enemy.x = random.uniform(spawn_rect.left, spawn_rect.right)
                enemy.y = random.uniform(spawn_rect.top, spawn_rect.bottom)
                if self.check_overlap(enemy):
                    self.spawn_enemy(enemy)
                    return True
            return False
        else:
            self.spawn_enemy(enemy)
            return True

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


class DebugRoom(Room):
    """用于测试的房间，不会在随机中出现"""

    def generate(self):
        self.spawn_enemy(TestDummy(), 400, 300)
        self.spawn_enemy(TestDummy(), 300, 400)
        self.spawn_enemy(TestDummy(), 400, 400)
        self.spawn_enemy(TestDummy(), 300, 300)
        self.spawn_enemy_randompos(Orangutan(), no_overlap=True)
        self.spawn_item(item.ItemHpRegen(), 500, 500)
