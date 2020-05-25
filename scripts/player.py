"""
玩家类，玩家控制的角色
class player
"""
from .creature import Creature
from .entity import Entity
import pygame
from pygame.sprite import Group
from .bullet import Bullet
from math import atan2
from . import image_dict
from . import constants as c
from . import setting, dbgscreen


class Player(Creature):
    def __init__(self, image: pygame.Surface):
        super().__init__(image)

        self.maxhp = 100
        self.hp = self.maxhp
        self.atk = 10

        self.is_fire = False
        self.fire_control = ''
        """开火方式，键盘还是鼠标还是手柄"""
        self.fire_dir = 0.0
        """暂存的开火方向，在使用手柄时使用"""
        self.fire_cd = 0
        """距离下一次能开火的时间"""
        self.viewport = pygame.Rect(0, 0, 0, 0)
        """是外面的这个的引用(Game.viewport)，用于计算玩家在屏幕上的实际位置"""

        self.control_factor_x = 0.0
        """控制玩家在x分量上移动的速度比例，范围为-1~1"""
        self.control_factor_y = 0.0
        """控制玩家在y分量上移动的速度比例，范围为-1~1"""

        self.base_speed = 4.0
        self.speed = self.base_speed
        self.bullet_speed = 8

    def fire(self, bullets: Group):
        """
        射出子弹，方向由操控方式决定，如果在CD则不发射
        :param bullets:子弹群组
        :return:None
        """

        if self.fire_cd > 0 or not self.is_fire:
            return
        direction = 0.0
        if self.fire_control == c.CONTROL_KEYBOARD:
            direction = self.direction
        elif self.fire_control == c.CONTROL_MOUSE:
            mx, my = pygame.mouse.get_pos()
            direction = atan2(my + self.viewport.y - self.y, mx + self.viewport.x - self.x)
        elif self.fire_control == c.CONTROL_JOYSTICK:
            direction = self.fire_dir

        bullet = Bullet(image_dict[c.PLAYER_BULLET_NAME])
        bullet.setup(self.x, self.y, self.atk)
        bullet.set_dir_v(direction, self.bullet_speed)
        bullets.add(bullet)
        self.fire_cd = setting.player_fire_cd

    def update(self):
        if self.control_factor_y == 0.0 and self.control_factor_x == 0.0:
            self.speed = 0  # 没有按键按下时应停止
        else:
            self.speed = self.base_speed  # 有按键时就移动
            self.direction = atan2(self.control_factor_y, self.control_factor_x)
        self.fire_cd -= 1
        super().update()
