"""
所有敌人的类都放在这里
contains all enemy class
"""
from typing import Union, Any, List, Tuple

import pygame
from .entity import Entity
from . import image_dict
from . import setting
from . import dbgscreen
from . import constants as c
from math import sin, cos, atan2


class Enemy(Entity):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        # 战斗有关的属性，以下为默认值，没有什么用（还不是因为python没有变量声明），一定要覆盖这些值
        # 这里写上这些值主要是为了方便IDE提示
        self.maxhp = 1
        self.hp = 1
        self.atk = 1
        self.gold = 1
        self.speed = 1.0

        # 怪物ai有关的属性，或许[状态设计模式]可能有用？
        self.status = c.STATUS_IDLE
        """当前状态"""

        self.status_queue: List[Tuple[c.STATUS_TYPE, int, List]] = []
        """
        状态队列，用于一次性添加很多状态，实现一些复杂的操作，比如闲逛转圈啥的。
        tuple[0]表示状态，tuple[1]表示持续时间，tuple[2]表示参数，我不知道加入参数是不是很抠脚的思路
        """
        self.status_time = 0
        """当前状态剩余时间"""

    def update(self):
        self.velocity = self.speed  # 先同步速度属性，这样可以处理加减速的buff效果
        super().update()  # 其他代码不变

    def draw(self, screen: pygame.Surface):
        super().draw(screen)  # 先画出图像
        hp_bar_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, setting.enemy_hpbar_height))
        hp_rect = hp_bar_rect.copy()
        hp_rect.width = hp_rect.width * (self.hp / self.maxhp)
        pygame.draw.rect(screen, setting.enemy_hpbar_color, hp_rect)  # 画血条
        pygame.draw.rect(screen, setting.enemy_hpbar_line_color, hp_bar_rect, setting.enemy_hpbar_line_width)  # 画边框

    def idle(self):
        """
        把当前状态转换为待机
        :return:None
        """
        self.status = c.STATUS_IDLE
        self.velocity = 0

    def moveto(self, x: Union[int, float], y):
        """
        把当前状态转换为移动中
        :param x:目标点的x坐标
        :param y:目标点的y坐标
        :return:None
        """
        self.status = c.STATUS_MOVE
        direction = atan2(y - self.y, x - self.x)
        self.set_dir_v(direction, self.speed)

    def ai(self):
        """
        敌人的ai，控制敌人的行为
        :return:
        """
        # todo 处理状态和敌人ai的代码还没有写完，下次再写
        pass

    def handle_status(self, status: c.STATUS_TYPE, *args):
        if status == c.STATUS_IDLE:
            self.idle()
        elif status == c.STATUS_MOVE:
            self.moveto(*args)

    def handle_status_queue(self):
        """
        用于处理状态队列
        :return:
        """
        if self.status_time <= 0 and len(self.status_queue) > 0:
            self.status, self.status_time, args = self.status_queue.pop(0)
            self.handle_status(self.status, *args)


class Slime(Enemy):
    def __init__(self):
        super().__init__(image_dict['slime'])
        self.maxhp = 100
        self.hp = 100
        self.atk = 10
        self.gold = 1
        self.speed = 2
