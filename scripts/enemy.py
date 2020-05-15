"""
所有敌人的类都放在这里
contains all enemy class
"""
from math import atan2
from typing import Union, List, Tuple, Optional

import pygame
from pygame.sprite import Group

from . import constants as c, dbgscreen
from . import image_dict
from . import setting
from .bullet import Bullet
from .creature import Creature
from .entity import Entity


class Enemy(Creature):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        self.can_fire = True
        """标志这种怪物能否开火"""

        # 怪物ai有关的属性，或许[状态设计模式]可能有用？
        self.status = c.STATUS_IDLE
        """当前状态"""
        self.status_queue: List[Tuple[c.STATUS_TYPE, int, List]] = []
        """
        状态队列，用于一次性添加很多状态，实现一些复杂的操作，比如闲逛转圈啥的。
        tuple[0]表示状态，tuple[1]表示持续时间，tuple[2]表示参数，我不知道加入参数是不是很抠脚的思路
        另外，这个list里的元素可以打包成一个类
        """
        self.status_time = 0
        """当前状态剩余时间"""
        self.target: Optional[Entity] = None
        """子弹发射时会对准的目标"""
        self.bullet_group: Optional[Group] = None
        """子弹发射需要的群组，没有则不能发射子弹，或许开火可以做成一个mixin？"""

    def set_fireable(self, target: Entity, bullet_group: Group):
        """
        注册开火所需的外部变量，这个设计和名字感觉好抠脚，（或许应该套一层娃？写个Enemy_fire子类？）
        """
        self.target = target
        self.bullet_group = bullet_group

    def idle(self):
        """
        当前状态为待机
        :return:None
        """
        self.speed = 0

    def moveto(self, x: Union[int, float], y):
        """
        当前状态为移动中
        :param x:目标点的x坐标
        :param y:目标点的y坐标
        :return:None
        """
        self.speed = self.max_speed
        direction = atan2(y - self.y, x - self.x)
        self.set_dir_v(direction, self.speed)

    def fire_to_xy(self, bullets: Group, x: float, y: float):
        """
        向指定方向射出子弹
        """
        direction = atan2(y - self.y, x - self.x)
        bullet = Bullet(image_dict[c.ENEMY_BULLET_NAME])
        bullet.set_dir_v(direction, self.bullet_speed)
        bullet.set_xy(self.x, self.y)
        bullet.damage = self.atk
        bullets.add(bullet)

    def fire_to_target(self, bullets: Group):
        """
        向自身锁定的目标射出子弹
        """
        if self.target is None:  # 没有锁定目标则不发射子弹
            return
        self.fire_to_xy(bullets, self.target.x, self.target.y)

    def ai(self):
        """
        敌人的ai，控制敌人的行为
        这个基类的ai是默认的行为（静止），在子类覆盖它以实现不同的行为
        :return:
        """
        self.idle()

    def handle_status(self, status: c.STATUS_TYPE, *args):
        """
        处理状态队列的头元素，在handle_status_queue()里使用，不单独调用。
        :param status:
        :param args:
        :return:
        """
        if status == c.STATUS_IDLE:
            self.idle()
        elif status == c.STATUS_MOVE:
            self.moveto(*args)
        elif status == c.STATUS_FIRE:
            self.fire_to_target(*args)

    def handle_status_queue(self):
        """
        用于处理状态队列
        :return:
        """
        # if 改成while可以处理连续的瞬时（持续时间为0）的事件，比如开火
        while self.status_time <= 0 and len(self.status_queue) > 0:
            self.status, self.status_time, args = self.status_queue.pop(0)
            self.handle_status(self.status, *args)
        self.status_time -= 1


# todo 给下面的怪物改一个适合的名字
class Slime(Enemy):
    """
    普通怪物
    """
    def __init__(self):
        super().__init__(image_dict['slime'])
        self.maxhp = 100
        self.hp = 100
        self.atk = 10
        self.gold = 1
        self.speed = 2
        self.max_speed = 2

    def ai(self):
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 30, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()


class Slime2(Enemy):
    """
    普通怪物，血少速度快
    """
    def __init__(self):
        super().__init__(image_dict['slime2'])
        self.maxhp = 50
        self.hp = 50
        self.atk = 10
        self.gold = 1
        self.speed = 5
        self.max_speed = 10

    def ai(self):
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()


class Slime3(Enemy):
    """
    普通怪物，加高血量
    """
    def __init__(self):
        super().__init__(image_dict['slime3'])
        self.maxhp = 200
        self.hp = 200
        self.atk = 10
        self.gold = 1
        self.speed = 2
        self.max_speed = 2

    def ai(self):
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 30, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()


class Slime4(Enemy):
    """
    slime2的升级版本，速度飞快
    """
    def __init__(self):
        super().__init__(image_dict['slime2'])
        """血少速度快"""
        self.maxhp = 50
        self.hp = 50
        self.atk = 10
        self.gold = 1
        self.speed = 10
        self.max_speed = 15

    def ai(self):
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_MOVE, 10, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()


class Slime5(Enemy):
    """
    固定炮台型怪物，生成后就不移动，但是打一下很疼
    """
    def __init__(self):
        super().__init__(image_dict['slime3'])
        """血少速度快"""
        self.maxhp = 300
        self.hp = 300
        self.atk = 20
        self.gold = 2
        self.speed = 0
        self.max_speed = 0

    def ai(self):
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()


class Orangutan(Enemy):
    """猩猩"""

    def __init__(self):
        super().__init__(image_dict['orangutan'])
        """猩猩更耐揍"""
        self.maxhp = 300
        self.hp = 300
        self.atk = 10
        self.gold = 1
        """动作比较迟缓"""
        self.speed = 1
        self.max_speed = 1

    def ai(self):
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()


class Boss(Enemy):
    """因为是boss所以长得比较大只
    终极boss
    """

    def __init__(self):
        super().__init__(image_dict['boss'])
        self.maxhp = 500
        self.hp = 500
        self.atk = 10
        self.gold = 1
        """速度也很快"""
        self.speed = 5
        self.max_speed = 5

    def ai(self):
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 20, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 20, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()
