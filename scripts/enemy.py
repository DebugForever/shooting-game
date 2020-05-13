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
from .entity import Entity


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
        """当前速度"""
        self.max_speed = 1.0
        """最大速度"""
        self.bullet_speed = 1

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


class Slime(Enemy):
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

"""懒得取名字了"""
class Slime2(Enemy):
    def __init__(self):
        super().__init__(image_dict['slime2'])
        """血少速度快"""
        self.maxhp = 50
        self.hp = 50
        self.atk = 10
        self.gold = 1
        self.speed = 1
        self.max_speed = 1

    def ai(self):
        dbgscreen.show(self.status)
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 30, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()

class Slime3(Enemy):
    def __init__(self):
        super().__init__(image_dict['slime3'])
        """第一个高配版"""
        self.maxhp = 200
        self.hp = 200
        self.atk = 10
        self.gold = 1
        self.speed = 2
        self.max_speed = 2

    def ai(self):
        dbgscreen.show(self.status)
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 30, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()

    def ai(self):
        dbgscreen.show(self.status)
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 30, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()

"""猩猩"""
class Orangutan(Enemy):
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
        dbgscreen.show(self.status)
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 30, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()

"""因为是boss所以长得比较大只"""
class Boss(Enemy):
    def __init__(self):
        super().__init__(image_dict['boss'])
        """设定为终极boss"""
        self.maxhp = 500
        self.hp = 500
        self.atk = 10
        self.gold = 1
        """速度也很快"""
        self.speed = 5
        self.max_speed = 5

    def ai(self):
        dbgscreen.show(self.status)
        if len(self.status_queue) == 0:
            self.status_queue.append((c.STATUS_IDLE, 30, []))
            self.status_queue.append((c.STATUS_MOVE, 30, [self.target.x, self.target.y]))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
            self.status_queue.append((c.STATUS_IDLE, 10, []))
            self.status_queue.append((c.STATUS_FIRE, 0, [self.bullet_group]))
        self.handle_status_queue()



